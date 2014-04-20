Postmon-python
==============

O postmon-python é um wrapper da API do Postmon.

As chamadas devem ser feitas para as funções do módulo, que fazem as chamadas
para o Postmon e retornam objetos com os resultados. Em caso de falha, todas as
funções retornam `None`.

Instalação
----------

O pacote está disponível no [PyPI](https://pypi.python.org/pypi/postmon),
podendo ser instalado diretamente com o `pip` ou outro gerenciador de pacotes do Python:

```bash
$ pip install postmon
```

Utilização
----------

 1. Para buscar um endereço a partir do CEP:

    ```python
    >>> import postmon
    >>> e = postmon.endereco('01419101')
    >>> print e.logradouro + ', ' + e.bairro + ' - ' + e.cidade.nome + '/' + e.estado.uf
    Alameda Santos, Cerqueira César - São Paulo/SP
    ```

 1. Para buscar os dados de uma cidade:

    ```python
    >>> import postmon
    >>> e = postmon.cidade('SP', 'São Paulo')
    >>> print e.area_km2
    1521.101
    ```

 1. Para buscar os dados de um estado:

    ```python
    >>> import postmon
    >>> e = postmon.estado('SP')
    >>> print e.area_km2
    248222.801
    ```

Documentação
------------

Você pode ler a documentação completa do projeto em http://postmon-python.readthedocs.org/.

Licença
-------

```
The MIT License (MIT)

Copyright (c) 2014 Postmon API

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
