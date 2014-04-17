# coding: utf-8
import requests

BASE_URL = 'http://api.postmon.com.br/v1'


class Cidade(object):

    def __init__(self, nome, area_km2=None, codigo_ibge=None):
        self.nome = nome
        self.area_km2 = area_km2
        self.codigo_ibge = codigo_ibge

    def __repr__(self):
        return '<postmon.Cidade %r>' % self.nome

    def __str__(self):
        return self.nome


class Estado(object):

    def __init__(self, uf, nome=None, area_km2=None, codigo_ibge=None):
        self.uf = uf
        self.nome = nome
        self.area_km2 = area_km2
        self.codigo_ibge = codigo_ibge

    def __repr__(self):
        return '<postmon.Estado %r>' % self.uf

    def __str__(self):
        return self.uf


class Endereco(object):

    def __init__(self, **kwargs):
        self.cep = kwargs['cep']
        self.logradouro = kwargs.get('logradouro')
        self.bairro = kwargs.get('bairro')

        estado_info = kwargs.get('estado_info', {})
        self.estado = Estado(kwargs['estado'],
                             estado_info.get('nome'),
                             estado_info.get('area_km2'),
                             estado_info.get('codigo_ibge'))

        cidade_info = kwargs.get('cidade_info', {})
        self.cidade = Cidade(kwargs['cidade'],
                             cidade_info.get('area_km2'),
                             cidade_info.get('codigo_ibge'))

    def __repr__(self):
        return '<postmon.Endereco %r>' % self.cep

    def __str__(self):
        return '%s, %s - %s, %s - CEP: %s' % (self.logradouro, self.bairro,
                                              self.cidade, self.estado,
                                              self.cep)


def buscar_cep(cep):
    response = _GET('/cep/%s' % cep)
    response.raise_for_status()
    return Endereco(**response.json())


def _GET(endpoint):
    url = '%s%s' % (BASE_URL, endpoint)
    response = requests.get(url)
    return response
