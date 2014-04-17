import unittest
import json

import httpretty
import postmon


response = {
    "bairro": "Bairro B",
    "cidade": "Cidade C",
    "cep": "11111111",
    "logradouro": "Logradouro L",
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


class TestValidCep(unittest.TestCase):

    def setUp(self):
        httpretty.enable()
        url = '%s/cep/11111111' % postmon.BASE_URL
        httpretty.register_uri(httpretty.GET, url, body=json.dumps(response))
        self.endereco = postmon.buscar_cep('11111111')

    def tearDown(self):
        httpretty.disable()
        httpretty.reset()

    def test_cep(self):
        self.assertEqual('11111111', self.endereco.cep)

    def test_logradouro(self):
        self.assertEqual('Logradouro L', self.endereco.logradouro)

    def test_bairro(self):
        self.assertEqual('Bairro B', self.endereco.bairro)
