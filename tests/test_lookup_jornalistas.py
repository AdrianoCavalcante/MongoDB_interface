
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import unittest
import json
from src.conexao_mongodb import conectar_mongodb, desconectar_mongodb
from src.consulta_mongodb import consultar_mongodb


class TestConsultaJornalistasAggregate(unittest.TestCase):
    """
    Testes para consultas de agregação que fazem lookup entre noticias_g1 e jornalistas
    para retornar o nome do jornalista em vez do ID.
    """

    def setUp(self):
        """Conecta ao MongoDB antes de cada teste"""
        status, client, msg = conectar_mongodb()
        self.status = status
        self.client = client
        self.msg = msg
        self.banco = "trabalho_banco_dados"
        self.colecao = "noticias_g1"
        
        if not self.status:
            self.fail(f"Falha na conexão: {msg}")

    def tearDown(self):
        """Desconecta do MongoDB após cada teste"""
        if self.status and self.client:
            desconectar_mongodb(self.client)

    def test_lookup_jornalista_objectid_compativel(self):
        """
        Testa agregação com $lookup quando jornalista_id e _id em jornalistas 
        são do mesmo tipo (ambos ObjectId).
        """
        query = json.dumps([
            {"$lookup": {
                "from": "jornalistas",
                "localField": "jornalista_id",
                "foreignField": "_id",
                "as": "jornalista"
            }},
            {"$unwind": "$jornalista"},
            {"$group": {
                "_id": "$jornalista.nome",
                "total_noticias": {"$sum": 1}
            }},
            {"$sort": {"total_noticias": -1}},
            {"$project": {"_id": 0, "jornalista": "$_id", "total_noticias": 1}}
        ])

        resultado = consultar_mongodb(
            self.status,
            self.client,
            self.banco,
            self.colecao,
            query
        )

        dados = json.loads(resultado)
        
        # Verificações
        self.assertTrue(dados["sucesso"], f"Consulta falhou: {dados.get('erro', {}).get('mensagem', 'erro desconhecido')}")
        self.assertIn("dados", dados)
        self.assertIsInstance(dados["dados"], list)
        self.assertGreater(len(dados["dados"]), 0, "Nenhum resultado retornado")
        
        # Verifica se os campos esperados existem
        primeiro_item = dados["dados"][0]
        self.assertIn("jornalista", primeiro_item)
        self.assertIn("total_noticias", primeiro_item)
        
        # Verifica que os totais estão ordenados decrescentemente
        totais = [item["total_noticias"] for item in dados["dados"]]
        self.assertEqual(totais, sorted(totais, reverse=True))
        
        print(f"\n✅ Lookup com ObjectId compatível - {len(dados['dados'])} jornalistas encontrados")
        print(f"   Top 3: {dados['dados'][:3]}")

    def test_lookup_jornalista_string_to_objectid(self):
        """
        Testa agregação com $lookup quando jornalista_id é string e precisa ser 
        convertido para ObjectId antes do join.
        """
        query = json.dumps([
            {"$addFields": {"jornalista_oid": {"$toObjectId": "$jornalista_id"}}},
            {"$lookup": {
                "from": "jornalistas",
                "localField": "jornalista_oid",
                "foreignField": "_id",
                "as": "jornalista"
            }},
            {"$unwind": "$jornalista"},
            {"$group": {
                "_id": "$jornalista.nome",
                "total_noticias": {"$sum": 1}
            }},
            {"$sort": {"total_noticias": -1}},
            {"$project": {"_id": 0, "jornalista": "$_id", "total_noticias": 1}}
        ])

        resultado = consultar_mongodb(
            self.status,
            self.client,
            self.banco,
            self.colecao,
            query
        )

        dados = json.loads(resultado)
        
        # Verificações
        self.assertTrue(dados["sucesso"], f"Consulta falhou: {dados.get('erro', {}).get('mensagem', 'erro desconhecido')}")
        self.assertIn("dados", dados)
        self.assertIsInstance(dados["dados"], list)
        
        # Se retornar vazio, significa que jornalista_id não é string (é ObjectId direto)
        # Neste caso, o teste anterior deve ter funcionado
        if len(dados["dados"]) == 0:
            print("\n⚠️  Lookup com conversão String→ObjectId retornou vazio")
            print("   Isso é esperado se jornalista_id já é ObjectId (use o teste anterior)")
        else:
            # Se retornou dados, verifica estrutura
            primeiro_item = dados["dados"][0]
            self.assertIn("jornalista", primeiro_item)
            self.assertIn("total_noticias", primeiro_item)
            
            print(f"\n✅ Lookup com String→ObjectId - {len(dados['dados'])} jornalistas encontrados")
            print(f"   Top 3: {dados['dados'][:3]}")

    def test_comparacao_lookup_vs_group_simples(self):
        """
        Compara o total de notícias agrupado por jornalista_id (simples)
        com o total após lookup pelo nome (deve ser igual).
        """
        # Query simples: agrupa por jornalista_id
        query_simples = json.dumps([
            {"$group": {"_id": "$jornalista_id", "total": {"$sum": 1}}}
        ])
        
        resultado_simples = consultar_mongodb(
            self.status,
            self.client,
            self.banco,
            self.colecao,
            query_simples
        )
        
        dados_simples = json.loads(resultado_simples)
        total_jornalistas_simples = len(dados_simples["dados"])
        
        # Query com lookup: agrupa por nome do jornalista
        query_lookup = json.dumps([
            {"$lookup": {
                "from": "jornalistas",
                "localField": "jornalista_id",
                "foreignField": "_id",
                "as": "jornalista"
            }},
            {"$unwind": "$jornalista"},
            {"$group": {
                "_id": "$jornalista.nome",
                "total_noticias": {"$sum": 1}
            }}
        ])
        
        resultado_lookup = consultar_mongodb(
            self.status,
            self.client,
            self.banco,
            self.colecao,
            query_lookup
        )
        
        dados_lookup = json.loads(resultado_lookup)
        total_jornalistas_lookup = len(dados_lookup["dados"])
        
        # Os totais devem ser iguais (mesmo número de jornalistas distintos)
        self.assertEqual(
            total_jornalistas_simples,
            total_jornalistas_lookup,
            f"Número de jornalistas difere: {total_jornalistas_simples} (ID) vs {total_jornalistas_lookup} (lookup)"
        )
        
        print(f"\n✅ Consistência verificada: {total_jornalistas_simples} jornalistas distintos")


if __name__ == "__main__":
    # Executa os testes com output verboso
    unittest.main(verbosity=2)
