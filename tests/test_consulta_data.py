
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
from datetime import datetime
from src.conexao_mongodb import conectar_mongodb, desconectar_mongodb
from src.consulta_mongodb import consultar_mongodb
import json

class TestConsultaData(unittest.TestCase):
    def setUp(self):
        status, client, msg = conectar_mongodb()
        self.status = status
        self.client = client
        self.msg = msg
        self.banco = "testeAdrianodatabase"  # ajuste conforme seu banco
        self.colecao = "noticias_g1"         # ajuste conforme sua coleção

    def tearDown(self):
        if self.status and self.client:
            desconectar_mongodb(self.client)

    def test_count_data_string(self):
        # Consulta usando data como string
        query = '{"_count": true, "_query": {"fonte.data_publicacao": {"$gte": "2023-01-01"}}}'
        resultado = consultar_mongodb(self.status, self.client, self.banco, self.colecao, query)
        dados = json.loads(resultado)
        self.assertTrue(dados["sucesso"])
        self.assertIn("contagem", dados)
        print("Contagem (data como string):", dados["contagem"])

    def test_count_data_datetime(self):
        # Consulta usando data como datetime
        data = datetime(2023, 1, 1)
        query_dict = {"_count": True, "_query": {"fonte.data_publicacao": {"$gte": data}}}
        resultado = consultar_mongodb(self.status, self.client, self.banco, self.colecao, json.dumps(query_dict, default=str))
        dados = json.loads(resultado)
        self.assertTrue(dados["sucesso"])
        self.assertIn("contagem", dados)
        print("Contagem (data como datetime):", dados["contagem"])

if __name__ == "__main__":
    unittest.main()
