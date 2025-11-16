"""
MongoDB Interface - Pacote Principal

Interface simplificada e segura para consultas MongoDB Atlas.
Suporta APENAS operações de leitura (read-only).

Módulos:
    - conexao_mongodb: Gerenciamento de conexões
    - consulta_mongodb: Operações de consulta

Exemplo de uso:
    >>> from src.conexao_mongodb import conectar_mongodb, desconectar_mongodb
    >>> from src.consulta_mongodb import consultar_mongodb, listar_bancos
    >>> 
    >>> # Conectar
    >>> status, client, msg = conectar_mongodb()
    >>> 
    >>> # Consultar
    >>> resultado = consultar_mongodb(status, client, "db", "col", '{"campo": "valor"}')
    >>> 
    >>> # Desconectar
    >>> desconectar_mongodb(client)
"""

__version__ = "1.0.0"
__author__ = "MongoDB Interface Contributors"
__license__ = "MIT"

# Importações para facilitar o uso do pacote
from .conexao_mongodb import conectar_mongodb, desconectar_mongodb
from .consulta_mongodb import (
    consultar_mongodb,
    listar_bancos,
    listar_colecoes,
    analisar_schema
)

__all__ = [
    "conectar_mongodb",
    "desconectar_mongodb",
    "consultar_mongodb",
    "listar_bancos",
    "listar_colecoes",
    "analisar_schema",
]
