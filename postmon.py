# coding: utf-8
"""
O postmon-python é um wrapper da API do Postmon.

As chamadas devem ser feitas para as funções do módulo, que fazem as chamadas
para o Postmon e retornam objetos com os resultados. Em caso de falha, todas as
funções retornam `None`.
"""

__title__ = 'postmon'
__version__ = '0.2'
__author__ = 'Iuri de Silvio'
__license__ = 'MIT'

from decimal import Decimal
import logging

import requests

logger = logging.getLogger(__name__)


class PostmonModel(object):
    """Objeto base para os modelos do Postmon."""

    base_url = 'http://api.postmon.com.br/v1'
    base_user_agent = '/'.join([__title__, __version__])
    _user_agent = None

    @property
    def user_agent(self):
        """
        User-Agent para as requisições feitas para o Postmon.

        Retorna o ``base_user_agent`` concatenado com o ``User-Agent`` padrão
        do requests.
        """
        if not self._user_agent:
            session = requests.Session()
            user_agent = session.headers['User-Agent']
            self._user_agent = '%s %s' % (self.base_user_agent, user_agent)
        return self._user_agent

    def buscar(self):
        """Faz a busca das informações do objeto no Postmon.

        Retorna um ``bool`` indicando se a busca foi bem sucedida.
        """
        headers = {'User-Agent': self.user_agent}
        try:
            self._response = requests.get(self.url, headers=headers)
        except requests.RequestException:
            logger.exception("%s.buscar() falhou: GET %s" %
                             (self.__class__.__name__, self.url))
            return False

        if self._response.ok:
            self.atualizar(**self._response.json())
        return self._response.ok

    @property
    def url(self):
        """Retorna a URL chamada pelo objeto.

        >>> e = Endereco('11111111')
        >>> e.url
        'http://api.postmon.com.br/v1/cep/11111111'
        """
        return self.base_url + (self.endpoint % self._params)

    @property
    def status(self):
        """Status da resposta recebida do Postmon.

        Os status previstos pelo Postmon são:

         * ``200 OK``
         * ``404 CEP NAO ENCONTRADO``
         * ``503 SERVICO INDISPONIVEL``

        Além dos status listados, outros status HTTP podem ocorrer, como
        em qualquer chamada HTTP.

        O único caso de sucesso é o ``200 OK``, caso em que o resultado no
        objeto é válido e pode ser utilizado.
        """
        try:
            r = self._response
        except AttributeError:
            return None
        else:
            return r.status_code, r.reason

    @property
    def _ok(self):
        """Retorna ``True`` ou ``False``, indicando se a busca funcionou
        corretamente.

        Retorna ``None`` caso o ``buscar`` ainda não tenha sido chamado.
        """
        try:
            r = self._response
        except AttributeError:
            return None
        else:
            return r.ok


class Cidade(PostmonModel):
    """
    Objeto que representa uma cidade do Postmon.
    """
    endpoint = '/cidade/%s/%s'

    def __init__(self, uf, nome, area_km2=None, codigo_ibge=None, **kwargs):
        self.uf = uf.upper()
        self.nome = nome
        self._params = (uf, nome)
        self.atualizar(area_km2, codigo_ibge, **kwargs)

    def atualizar(self, area_km2, codigo_ibge, **kwargs):
        self.area_km2 = area_km2
        self.codigo_ibge = codigo_ibge

    @property
    def area_km2(self):
        return self._area_km2

    @area_km2.setter
    def area_km2(self, value):
        self._area_km2 = _parse_area_km2(value)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.nome)

    def __str__(self):
        return '%s - %s' % (self.nome, self.uf)


class Estado(PostmonModel):
    """
    Objeto que representa um estado do Postmon.
    """
    endpoint = '/uf/%s'

    def __init__(self, uf, nome=None, area_km2=None, codigo_ibge=None,
                 **kwargs):
        self.uf = uf.upper()
        self._params = uf
        self.atualizar(nome, area_km2, codigo_ibge, **kwargs)

    def atualizar(self, nome, area_km2, codigo_ibge, **kwargs):
        self.nome = nome
        self.area_km2 = area_km2
        self.codigo_ibge = codigo_ibge

    @property
    def area_km2(self):
        return self._area_km2

    @area_km2.setter
    def area_km2(self, value):
        self._area_km2 = _parse_area_km2(value)

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.uf)

    def __str__(self):
        return self.uf


class Endereco(PostmonModel):
    """
    Objeto que representa um endereço do Postmon.

    O ``Endereco`` pode ser criado apenas com o CEP para posteriormente
    ser buscado.

        >>> import postmon
        >>> e = postmon.Endereco('30110-012')
        >>> if e.buscar():
        ...     print("Bairro: %s" % e.bairro)
        ... else:
        ...     print("Busca falhou: %s" % e.status)
        Bairro: Floresta
    """
    endpoint = '/cep/%s'

    def __init__(self, cep, logradouro=None, complemento=None, bairro=None,
                 cidade=None, estado=None, cidade_info=None, estado_info=None,
                 **kwargs):
        self.cep = cep
        self._params = cep
        self.atualizar(logradouro=logradouro, complemento=complemento,
                       bairro=bairro, cidade=cidade, estado=estado,
                       cidade_info=cidade_info, estado_info=estado_info,
                       **kwargs)

    def atualizar(self, logradouro=None, complemento=None, bairro=None,
                  cidade=None, estado=None, cidade_info=None, estado_info=None,
                  **kwargs):
        self.logradouro = logradouro
        self.complemento = complemento
        self.bairro = bairro

        if estado:
            if not estado_info:
                estado_info = {}
            self.estado = Estado(estado,
                                 estado_info.get('nome'),
                                 estado_info.get('area_km2'),
                                 estado_info.get('codigo_ibge'))

            if cidade:
                if not cidade_info:
                    cidade_info = {}
                self.cidade = Cidade(estado, cidade,
                                     cidade_info.get('area_km2'),
                                     cidade_info.get('codigo_ibge'))

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.cep)

    def __str__(self):
        # a busca ainda não foi feita
        if self._ok is None:
            return 'CEP %s' % self.cep

        # juntando complemento e logradouro
        p1 = None
        if self.logradouro:
            p1 = self.logradouro
        if self.complemento:
            p1 = '%s - %s' % (p1, self.complemento)

        # juntando bairro e cidade
        p2 = self.cidade.nome
        if self.bairro:
            p2 = '%s - %s' % (self.bairro, p2)

        # juntando estado e cep
        p3 = '%s - CEP %s' % (self.estado, self.cep)

        return ', '.join(p for p in (p1, p2, p3) if p)


def cidade(uf, nome):
    """Busca a cidade no Postmon e retorna um objeto ``Cidade``.

    Retorna ``None`` caso a cidade não exista ou caso ocorra algum erro de
    comunicação.

        >>> import postmon
        >>> postmon.cidade('MG', 'Belo Horizonte')
        <Cidade 'Belo Horizonte'>
    """
    return _make_object(Cidade, uf, nome)


def estado(uf):
    """Busca o estado no Postmon e retorna um objeto ``Estado``.

    Retorna ``None`` caso o estado não exista ou caso ocorra algum erro de
    comunicação.

        >>> import postmon
        >>> postmon.estado('MG')
        <Estado 'MG'>
    """
    return _make_object(Estado, uf)


def endereco(cep):
    """Busca o CEP no Postmon e retorna um objeto ``Endereco``.

    Retorna ``None`` caso o CEP não exista ou caso ocorra algum erro de
    comunicação.

        >>> import postmon
        >>> postmon.endereco('01001-000')
        <Endereco '01001-000'>
    """
    return _make_object(Endereco, cep)


def _make_object(cls, *args):
    obj = cls(*args)
    return obj if obj.buscar() else None


def _parse_area_km2(valor):
    """O campo ``area_km2`` é uma string com um número em formato pt-br, com
    casas decimais que representam m2.

    Exemplos: "331,401", "248.222,801"
    """
    if valor is None:
        return None
    elif isinstance(valor, Decimal):
        return valor
    try:
        int_, dec = valor.split(',', 1)
    except ValueError:
        # valor não tem separador decimal
        int_, dec = valor, '000'

    # remove os separadores de milhar
    int_ = int_.replace('.', '')

    return Decimal('%s.%s' % (int_, dec))
