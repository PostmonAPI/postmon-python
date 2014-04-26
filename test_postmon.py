import unittest
import json
from decimal import Decimal

import mock
import httpretty
import requests

import postmon

BASE_URL = postmon.PostmonModel.base_url


class TestCepCompleto(unittest.TestCase):

    url = '%s/cep/11111111' % BASE_URL
    response = {
        "bairro": "Bairro B",
        "cidade": "Cidade C",
        "cep": "11111111",
        "logradouro": "Logradouro L",
        "complemento": "Complemento C",
        "estado_info": {
            "area_km2": "999.999,001",
            "codigo_ibge": "35",
            "nome": "Estado E"
        },
        "cidade_info": {
            "area_km2": "1099,409",
            "codigo_ibge": "3549904"
        },
        "estado": "SP"
    }

    @classmethod
    def setUpClass(cls):
        httpretty.enable()
        httpretty.register_uri(httpretty.GET, cls.url,
                               body=json.dumps(cls.response))

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()

    def setUp(self):
        self.endereco = postmon.endereco('11111111')

    def test_cep(self):
        self.assertEqual('11111111', self.endereco.cep)

    def test_logradouro(self):
        self.assertEqual('Logradouro L', self.endereco.logradouro)

    def test_complemento(self):
        self.assertEqual('Complemento C', self.endereco.complemento)

    def test_bairro(self):
        self.assertEqual('Bairro B', self.endereco.bairro)

    def test_url(self):
        self.assertEqual(self.url, self.endereco.url)

    def test_str(self):
        self.assertEqual('Logradouro L - Complemento C, Bairro B - Cidade C, '
                         'SP - CEP 11111111', str(self.endereco))


class TestCepIncompleto(unittest.TestCase):

    response = {
        "cidade": "Cidade C",
        "cep": "22222222",
        "estado": "SP"
    }

    @classmethod
    def setUpClass(cls):
        httpretty.enable()
        url = '%s/cep/22222222' % BASE_URL
        httpretty.register_uri(httpretty.GET, url,
                               body=json.dumps(cls.response))

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()

    def setUp(self):
        self.endereco = postmon.endereco('22222222')

    def test_cep(self):
        self.assertEqual('22222222', self.endereco.cep)

    def test_cidade(self):
        self.assertEqual('Cidade C', self.endereco.cidade.nome)

    def test_estado(self):
        self.assertEqual('SP', self.endereco.estado.uf)

    def test_bairro_eh_nulo(self):
        self.assertTrue(self.endereco.bairro is None)

    def test_str(self):
        self.assertEqual('Cidade C, SP - CEP 22222222',
                         str(self.endereco))


class TestCidade(unittest.TestCase):

    url = '%s/cidade/mg/Belo Horizonte' % BASE_URL
    response = {
        "area_km2": "331,401",
        "codigo_ibge": "3106200"
    }

    @classmethod
    def setUpClass(cls):
        httpretty.enable()
        httpretty.register_uri(httpretty.GET, cls.url,
                               body=json.dumps(cls.response))

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()

    def setUp(self):
        self.cidade = postmon.cidade('mg', 'Belo Horizonte')

    def test_area_km2(self):
        self.assertEqual(Decimal('331.401'), self.cidade.area_km2)

    def test_codigo_ibge(self):
        self.assertEqual('3106200', self.cidade.codigo_ibge)

    def test_url(self):
        self.assertEqual(self.url, self.cidade.url)


class TestEstado(unittest.TestCase):

    url = '%s/uf/mg' % BASE_URL
    response = {
        "area_km2": "586.522,122",
        "codigo_ibge": "31",
        "nome": "Minas Gerais"
    }

    @classmethod
    def setUpClass(cls):
        httpretty.enable()
        httpretty.register_uri(httpretty.GET, cls.url,
                               body=json.dumps(cls.response))

    @classmethod
    def tearDownClass(cls):
        httpretty.disable()
        httpretty.reset()

    def setUp(self):
        self.estado = postmon.estado('mg')

    def test_area_km2(self):
        self.assertEqual(Decimal('586522.122'), self.estado.area_km2)

    def test_codigo_ibge(self):
        self.assertEqual('31', self.estado.codigo_ibge)

    def test_url(self):
        self.assertEqual(self.url, self.estado.url)


class TestErrosEndereco(unittest.TestCase):

    @httpretty.activate
    def test_404(self):
        url = '%s/cep/11111111' % BASE_URL
        httpretty.register_uri(httpretty.GET, url, status=404)
        r = postmon.endereco('11111111')
        self.assertTrue(r is None)

    @httpretty.activate
    def test_503(self):
        url = '%s/cep/22222222' % BASE_URL
        httpretty.register_uri(httpretty.GET, url, status=503)
        r = postmon.endereco('22222222')
        self.assertTrue(r is None)

    @mock.patch('postmon.requests.get')
    def test_request_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException
        r = postmon.endereco('11111111')
        self.assertTrue(r is None)


class TestErrosEstado(unittest.TestCase):

    @httpretty.activate
    def test_404(self):
        url = '%s/uf/xx' % BASE_URL
        httpretty.register_uri(httpretty.GET, url, status=404)
        r = postmon.estado('xx')
        self.assertTrue(r is None)

    @httpretty.activate
    def test_503(self):
        url = '%s/uf/yy' % BASE_URL
        httpretty.register_uri(httpretty.GET, url, status=503)
        r = postmon.estado('yy')
        self.assertTrue(r is None)

    @mock.patch('postmon.requests.get')
    def test_request_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException
        r = postmon.estado('xx')
        self.assertTrue(r is None)


class TestErrosCidade(unittest.TestCase):

    @httpretty.activate
    def test_404(self):
        url = '%s/cidade/xx/yy' % BASE_URL
        httpretty.register_uri(httpretty.GET, url, status=404)
        r = postmon.cidade('xx', 'yy')
        self.assertTrue(r is None)

    @httpretty.activate
    def test_503(self):
        url = '%s/cidade/yy/zz' % BASE_URL
        httpretty.register_uri(httpretty.GET, url, status=503)
        r = postmon.cidade('yy', 'zz')
        self.assertTrue(r is None)

    @mock.patch('postmon.requests.get')
    def test_request_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException
        r = postmon.cidade('xx', 'yy')
        self.assertTrue(r is None)


class TestParseAreaKm2(unittest.TestCase):

    def f(self, value):
        return postmon._parse_area_km2(value)

    def assert_f(self, expected, value):
        self.assertEqual(expected, self.f(value))

    def test_int_value(self):
        self.assert_f(Decimal('331.000'), '331')

    def test_km2_exact(self):
        self.assert_f(Decimal('331.000'), '331,000')

    def test_grouping_separators(self):
        self.assert_f(Decimal('1331.101'), '1.331,101')

    def test_decimal_value(self):
        self.assert_f(Decimal('1331.101'), Decimal('1331.101'))

    def test_none_value(self):
        self.assertTrue(self.f(None) is None)
