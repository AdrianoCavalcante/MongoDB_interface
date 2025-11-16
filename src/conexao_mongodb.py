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
        # Tenta pegar as credenciais do Streamlit Cloud
        try:
            import streamlit as st
            username = st.secrets["username"]
            password = st.secrets["password"]
            cluster = st.secrets["cluster"]
            database = st.secrets["database"]
            conn_str = f"mongodb+srv://{username}:{password}@{cluster}/{database}?retryWrites=true&w=majority"
        except (ImportError, KeyError):
            # Fallback: tenta ler do arquivo local (para uso local)
            with open("conexao_mongo_secrets.json", 'r', encoding='utf-8') as f:
                credenciais = json.load(f)
            username = credenciais["username"]
            password = credenciais["password"]
            cluster = credenciais["cluster"]
            database = credenciais["database"]
            conn_str = f"mongodb+srv://{username}:{password}@{cluster}/{database}?retryWrites=true&w=majority"

        # Criar cliente MongoDB
        client = MongoClient(conn_str)

        # Testar conexão com ping
        client.admin.command('ping')

        return True, client, "Conexão estabelecida com sucesso"

    except FileNotFoundError:
        return False, None, "Arquivo de credenciais 'conexao_mongo_secrets.json' não encontrado e variáveis de ambiente não configuradas"
    except KeyError as e:
        return False, None, f"Chave obrigatória ausente nas credenciais: {str(e)}"
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
