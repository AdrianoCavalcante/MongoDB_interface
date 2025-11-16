"""
Módulo para gerenciamento de conexões com MongoDB Atlas

Funções para conectar, desconectar e verificar status de conexão.
"""

import json
from typing import Tuple, Optional
from pymongo import MongoClient, errors


def conectar_mongodb() -> Tuple[bool, Optional[MongoClient], str]:
    """
    Estabelece conexão com MongoDB Atlas usando credenciais do arquivo JSON.
    
    Returns:
        Tupla contendo:
        - status_conexao (bool): True se conectado com sucesso, False caso contrário
        - client (MongoClient ou None): Instância do cliente MongoDB ou None em caso de erro
        - mensagem (str): Mensagem descritiva do resultado da conexão
    
    Examples:
        >>> status_conexao, client, msg = conectar_mongodb()
        >>> if status_conexao:
        >>>     print(f"Conectado: {msg}")
        >>> else:
        >>>     print(f"Erro: {msg}")
    """
    try:
        # Carregar credenciais do arquivo JSON
        with open("conexao_mongo_secrets.json", 'r', encoding='utf-8') as f:
            credenciais = json.load(f)
        
        # Montar connection string
        conn_str = f"mongodb+srv://{credenciais['username']}:{credenciais['password']}@{credenciais['cluster']}/?retryWrites=true&w=majority&appName=Cluster0"
        
        # Criar cliente MongoDB
        client = MongoClient(conn_str)
        
        # Testar conexão com ping
        client.admin.command('ping')
        
        return True, client, "Conexão estabelecida com sucesso"
        
    except FileNotFoundError:
        return False, None, "Arquivo de credenciais 'conexao_mongo_secrets.json' não encontrado"
    
    except KeyError as e:
        return False, None, f"Chave obrigatória ausente no arquivo de credenciais: {str(e)}"
    
    except errors.ConnectionFailure as e:
        return False, None, f"Falha ao conectar com MongoDB: {str(e)}"
    
    except Exception as e:
        return False, None, f"Erro inesperado ao conectar: {type(e).__name__} - {str(e)}"


def desconectar_mongodb(client: Optional[MongoClient]) -> Tuple[bool, str]:
    """
    Encerra conexão com MongoDB Atlas.
    
    Args:
        client: Instância do MongoClient a ser fechada (pode ser None)
    
    Returns:
        Tupla contendo:
        - status_conexao (bool): False após desconectar (indica que NÃO está mais conectado)
        - mensagem (str): Mensagem descritiva do resultado
    
    Examples:
        >>> status_conexao, msg = desconectar_mongodb(client)
        >>> print(msg)
        >>> # status_conexao será False após desconectar
    """
    try:
        if client is None:
            return False, "Nenhuma conexão ativa para encerrar"
        
        client.close()
        return False, "Conexão encerrada com sucesso"
        
    except Exception as e:
        return False, f"Erro ao encerrar conexão: {type(e).__name__} - {str(e)}"
