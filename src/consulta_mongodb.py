"""
Script para consultas MongoDB Atlas - SOMENTE LEITURA

Interface simplificada para executar consultas MongoDB a partir de aplicações externas.

Funções disponíveis:
- consultar_mongodb(): Executa queries (find, aggregate, distinct, count, find_one, find_with_options)
- listar_bancos(): Lista todos os bancos de dados disponíveis
- listar_colecoes(): Lista todas as coleções de um banco específico
- analisar_schema(): Analisa a estrutura dos documentos de uma coleção

Suporta APENAS operações de leitura.
NÃO realiza operações de escrita (insert, update, delete) por questões de segurança.
"""

import json
from typing import Dict, List, Any
from pymongo import MongoClient, errors
from pymongo.collection import Collection
from pymongo.database import Database
from .conexao_mongodb import conectar_mongodb, desconectar_mongodb


# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def consultar_mongodb(
    status_conexao: bool,
    client: MongoClient,
    nome_banco: str,
    nome_colecao: str,
    query_json: str,
    limite_amostra: bool = False
) -> str:
    """
    Executa consultas MongoDB a partir de aplicações externas.
    
    Args:
        status_conexao: Status da conexão (True=conectado, False=desconectado)
        client: Instância do MongoClient já conectado
        nome_banco: Nome do banco de dados MongoDB
        nome_colecao: Nome da coleção a ser consultada
        query_json: Query em sintaxe MongoDB como string JSON
            - Find: '{"campo": "valor"}'
            - Aggregate: '[{"$match": {...}}, {"$group": {...}}]'
            - Distinct: '{"_distinct": "campo", "_query": {...}}'
            - Count: '{"_count": true, "_query": {...}}'
            - Find One: '{"_find_one": true, "_query": {...}, "_projection": {...}}'
            - Find com Opções: '{"_find_with_options": true, "_query": {...}, "_sort": {...}, "_limit": N, "_skip": N, "_projection": {...}}'
        limite_amostra: Se True, retorna apenas os primeiros 20 documentos
            - False: Retorna todos os documentos (padrão)
            - True: Retorna apenas 20 documentos
            - Não se aplica a operações distinct, count e find_one
    
    Returns:
        String JSON contendo:
        - Sucesso: {"sucesso": true, "dados": [...]} ou {"sucesso": true, "contagem": N}
        - Erro: {"sucesso": false, "erro": {...}}
    
    Examples:
        >>> from conexao_mongodb import conectar_mongodb, desconectar_mongodb
        >>> 
        >>> # Estabelecer conexão
        >>> status_conexao, client, msg = conectar_mongodb()
        >>> if not status_conexao:
        >>>     print(f"Erro: {msg}")
        >>>     exit()
        >>> 
        >>> # Find: Retornar todos os dados
        >>> json_result = consultar_mongodb(status_conexao, client, "meu_banco", "noticias", '{"publicador": "G1"}')
        >>> 
        >>> # Find com amostra limitada (20 documentos)
        >>> json_result = consultar_mongodb(status_conexao, client, "meu_banco", "noticias", '{"publicador": "G1"}', limite_amostra=True)
        >>> 
        >>> # Aggregate: Pipeline de agregação
        >>> query = '[{"$match": {"publicador": "G1"}}, {"$group": {"_id": "$autor", "total": {"$sum": 1}}}]'
        >>> json_result = consultar_mongodb(status_conexao, client, "meu_banco", "noticias", query)
        >>> 
        >>> # Distinct: Valores únicos
        >>> json_result = consultar_mongodb(status_conexao, client, "meu_banco", "noticias", '{"_distinct": "publicador"}')
        >>> 
        >>> # Count: Contar documentos
        >>> json_result = consultar_mongodb(status_conexao, client, "meu_banco", "noticias", '{"_count": true, "_query": {"publicador": "G1"}}')
        >>> 
        >>> # Find One: Um único documento
        >>> json_result = consultar_mongodb(status_conexao, client, "meu_banco", "noticias", '{"_find_one": true, "_query": {"titulo": "Exemplo"}}')
        >>> 
        >>> # Find com opções: Sort, limit, skip
        >>> query = '{"_find_with_options": true, "_query": {"status": "ativo"}, "_sort": {"data": -1}, "_limit": 10, "_skip": 0}'
        >>> json_result = consultar_mongodb(status_conexao, client, "meu_banco", "noticias", query)
        >>> 
        >>> # Encerrar conexão
        >>> status_conexao, msg_disc = desconectar_mongodb(client)
        >>> print(msg_disc)
        >>> # Agora status_conexao = False (desconectado)
    """
    try:
        # Validar se a conexão está ativa
        if not status_conexao:
            return json.dumps({
                "sucesso": False,
                "erro": {
                    "tipo": "ConnectionError",
                    "mensagem": "Conexão não estabelecida. Execute conectar_mongodb() antes de realizar consultas."
                }
            }, ensure_ascii=False, indent=2)
        
        # Converter JSON string para objeto Python
        consulta = json.loads(query_json)
        
        # Selecionar banco e coleção
        db: Database = client[nome_banco]
        collection: Collection = db[nome_colecao]
        
        # Executar consulta
        if isinstance(consulta, list):
            # Aggregation Pipeline
            resultados = collection.aggregate(consulta)
        elif isinstance(consulta, dict):
            # Verificar se é uma operação especial (distinct, count_documents, etc.)
            if "_distinct" in consulta:
                # Distinct: {"_distinct": "campo", "_query": {...}}
                campo = consulta["_distinct"]
                filtro = consulta.get("_query", {})
                valores_distintos = collection.distinct(campo, filtro)
                return json.dumps({
                    "sucesso": True,
                    "dados": valores_distintos
                }, ensure_ascii=False, indent=2, default=str)
            
            elif "_count" in consulta:
                # Count: {"_count": true, "_query": {...}}
                filtro = consulta.get("_query", {})
                contagem = collection.count_documents(filtro)
                return json.dumps({
                    "sucesso": True,
                    "contagem": contagem
                }, ensure_ascii=False, indent=2)
            
            elif "_find_one" in consulta:
                # Find One: {"_find_one": true, "_query": {...}, "_projection": {...}}
                filtro = consulta.get("_query", {})
                projection = consulta.get("_projection", None)
                documento = collection.find_one(filtro, projection)
                return json.dumps({
                    "sucesso": True,
                    "dados": [documento] if documento else []
                }, ensure_ascii=False, indent=2, default=str)
            
            elif "_find_with_options" in consulta:
                # Find com opções avançadas: sort, limit, skip, projection
                # {"_find_with_options": true, "_query": {...}, "_sort": {...}, "_limit": N, "_skip": N, "_projection": {...}}
                filtro = consulta.get("_query", {})
                projection = consulta.get("_projection", None)
                sort_fields = consulta.get("_sort", None)
                limit = consulta.get("_limit", 0)
                skip = consulta.get("_skip", 0)
                
                cursor = collection.find(filtro, projection)
                
                if sort_fields:
                    # sort_fields pode ser: {"campo": 1} ou [("campo", 1), ("campo2", -1)]
                    if isinstance(sort_fields, dict):
                        cursor = cursor.sort(list(sort_fields.items()))
                    else:
                        cursor = cursor.sort(sort_fields)
                
                if skip > 0:
                    cursor = cursor.skip(skip)
                
                if limit > 0:
                    cursor = cursor.limit(limit)
                
                documentos = list(cursor)
                return json.dumps({
                    "sucesso": True,
                    "dados": documentos
                }, ensure_ascii=False, indent=2, default=str)
            
            else:
                # Find comum
                resultados = collection.find(consulta)
        else:
            raise ValueError("Query deve ser um dicionário (find) ou lista (aggregate)")
        
        # Converter para lista
        documentos: List[Dict[str, Any]] = list(resultados)
        
        # Aplicar limite se especificado
        if limite_amostra:
            documentos = documentos[:20]
        
        return json.dumps({
            "sucesso": True,
            "dados": documentos
        }, ensure_ascii=False, indent=2, default=str)
        
    except json.JSONDecodeError as e:
        return json.dumps({
            "sucesso": False,
            "erro": {
                "tipo": "JSONDecodeError",
                "mensagem": str(e),
                "posicao": e.pos,
                "linha": e.lineno,
                "coluna": e.colno
            }
        }, ensure_ascii=False, indent=2)
    
    except errors.OperationFailure as e:
        return json.dumps({
            "sucesso": False,
            "erro": {
                "tipo": "OperationFailure",
                "mensagem": f"Operação falhou: {str(e)}"
            }
        }, ensure_ascii=False, indent=2)
    
    except ValueError as e:
        return json.dumps({
            "sucesso": False,
            "erro": {
                "tipo": "ValueError",
                "mensagem": str(e)
            }
        }, ensure_ascii=False, indent=2)
        
    except Exception as e:
        return json.dumps({
            "sucesso": False,
            "erro": {
                "tipo": type(e).__name__,
                "mensagem": str(e)
            }
        }, ensure_ascii=False, indent=2)


# ============================================================================
# FUNÇÕES DE LISTAGEM DE METADADOS
# ============================================================================

def listar_bancos(
    status_conexao: bool,
    client: MongoClient
) -> str:
    """
    Lista todos os bancos de dados disponíveis no servidor MongoDB.
    
    Args:
        status_conexao: Status da conexão (True=conectado, False=desconectado)
        client: Instância do MongoClient já conectado
    
    Returns:
        String JSON contendo:
        - Sucesso: {"sucesso": true, "dados": ["banco1", "banco2", ...]}
        - Erro: {"sucesso": false, "erro": {...}}
    
    Examples:
        >>> from conexao_mongodb import conectar_mongodb, desconectar_mongodb
        >>> 
        >>> status_conexao, client, msg = conectar_mongodb()
        >>> if status_conexao:
        >>>     resultado = listar_bancos(status_conexao, client)
        >>>     dados = json.loads(resultado)
        >>>     print(dados["dados"])  # ["admin", "local", "testeAdriano", ...]
        >>>     desconectar_mongodb(client)
    """
    try:
        # Validar se a conexão está ativa
        if not status_conexao:
            return json.dumps({
                "sucesso": False,
                "erro": {
                    "tipo": "ConnectionError",
                    "mensagem": "Conexão não estabelecida. Execute conectar_mongodb() antes de listar bancos."
                }
            }, ensure_ascii=False, indent=2)
        
        # Listar todos os bancos de dados
        bancos = client.list_database_names()
        
        return json.dumps({
            "sucesso": True,
            "dados": bancos
        }, ensure_ascii=False, indent=2)
        
    except errors.OperationFailure as e:
        return json.dumps({
            "sucesso": False,
            "erro": {
                "tipo": "OperationFailure",
                "mensagem": f"Operação falhou ao listar bancos: {str(e)}"
            }
        }, ensure_ascii=False, indent=2)
    
    except Exception as e:
        return json.dumps({
            "sucesso": False,
            "erro": {
                "tipo": type(e).__name__,
                "mensagem": str(e)
            }
        }, ensure_ascii=False, indent=2)


def listar_colecoes(
    status_conexao: bool,
    client: MongoClient,
    nome_banco: str
) -> str:
    """
    Lista todas as coleções de um banco de dados específico.
    
    Args:
        status_conexao: Status da conexão (True=conectado, False=desconectado)
        client: Instância do MongoClient já conectado
        nome_banco: Nome do banco de dados para listar coleções
    
    Returns:
        String JSON contendo:
        - Sucesso: {"sucesso": true, "dados": ["colecao1", "colecao2", ...]}
        - Erro: {"sucesso": false, "erro": {...}}
    
    Examples:
        >>> from conexao_mongodb import conectar_mongodb, desconectar_mongodb
        >>> 
        >>> status_conexao, client, msg = conectar_mongodb()
        >>> if status_conexao:
        >>>     resultado = listar_colecoes(status_conexao, client, "testeAdriano")
        >>>     dados = json.loads(resultado)
        >>>     print(dados["dados"])  # ["noticias_g1", "jornalistas", ...]
        >>>     desconectar_mongodb(client)
    """
    try:
        # Validar se a conexão está ativa
        if not status_conexao:
            return json.dumps({
                "sucesso": False,
                "erro": {
                    "tipo": "ConnectionError",
                    "mensagem": "Conexão não estabelecida. Execute conectar_mongodb() antes de listar coleções."
                }
            }, ensure_ascii=False, indent=2)
        
        # Selecionar banco de dados
        db: Database = client[nome_banco]
        
        # Listar todas as coleções do banco
        colecoes = db.list_collection_names()
        
        return json.dumps({
            "sucesso": True,
            "dados": colecoes
        }, ensure_ascii=False, indent=2)
        
    except errors.OperationFailure as e:
        return json.dumps({
            "sucesso": False,
            "erro": {
                "tipo": "OperationFailure",
                "mensagem": f"Operação falhou ao listar coleções do banco '{nome_banco}': {str(e)}"
            }
        }, ensure_ascii=False, indent=2)
    
    except Exception as e:
        return json.dumps({
            "sucesso": False,
            "erro": {
                "tipo": type(e).__name__,
                "mensagem": str(e)
            }
        }, ensure_ascii=False, indent=2)


# ============================================================================
# FUNÇÃO PARA ANALISAR SCHEMA DE COLEÇÃO
# ============================================================================

def analisar_schema(
    status_conexao: bool,
    client: MongoClient,
    nome_banco: str,
    nome_colecao: str,
    amostra: int = 100
) -> str:
    """
    Analisa a estrutura (schema) dos documentos de uma coleção MongoDB.
    
    O MongoDB não tem schema fixo, mas esta função analisa uma amostra de documentos
    para identificar os campos existentes, seus tipos e frequência de aparição.
    
    Args:
        status_conexao: Status da conexão (True=conectado, False=desconectado)
        client: Instância do MongoClient já conectado
        nome_banco: Nome do banco de dados
        nome_colecao: Nome da coleção a ser analisada
        amostra: Número de documentos a analisar (padrão: 100)
    
    Returns:
        String JSON com:
        - sucesso: true
        - dados: {
            "total_documentos": int,
            "documentos_analisados": int,
            "campos": {
                "nome_campo": {
                    "tipos": ["tipo1", "tipo2"],
                    "frequencia": int (quantos docs têm este campo),
                    "percentual": float (% de docs que têm este campo),
                    "exemplo": valor de exemplo
                }
            }
        }
        
        Ou em caso de erro:
        - sucesso: false
        - erro: {"tipo": str, "mensagem": str}
    
    Exemplo de uso:
        >>> status, client, msg = conectar_mongodb()
        >>> resultado = analisar_schema(status, client, "testeAdrianodatabase", "noticias_g1", amostra=50)
        >>> print(resultado)
        {
          "sucesso": true,
          "dados": {
            "total_documentos": 3000,
            "documentos_analisados": 50,
            "campos": {
              "_id": {
                "tipos": ["ObjectId"],
                "frequencia": 50,
                "percentual": 100.0,
                "exemplo": "507f1f77bcf86cd799439011"
              },
              "titulo": {
                "tipos": ["str"],
                "frequencia": 50,
                "percentual": 100.0,
                "exemplo": "Notícia de exemplo"
              }
            }
          }
        }
    """
    
    # Validar status da conexão
    if not status_conexao:
        return json.dumps({
            "sucesso": False,
            "erro": {
                "tipo": "ConnectionError",
                "mensagem": "Cliente MongoDB não está conectado. Use conectar_mongodb() primeiro."
            }
        }, ensure_ascii=False, indent=2)
    
    try:
        # Acessar banco e coleção
        db: Database = client[nome_banco]
        collection: Collection = db[nome_colecao]
        
        # Contar total de documentos
        total_documentos = collection.count_documents({})
        
        # Determinar quantos documentos analisar
        docs_para_analisar = min(amostra, total_documentos)
        
        if total_documentos == 0:
            return json.dumps({
                "sucesso": True,
                "dados": {
                    "total_documentos": 0,
                    "documentos_analisados": 0,
                    "campos": {},
                    "mensagem": "A coleção está vazia"
                }
            }, ensure_ascii=False, indent=2)
        
        # Buscar amostra de documentos
        documentos = list(collection.find().limit(docs_para_analisar))
        
        # Analisar campos
        campos_info: Dict[str, Dict[str, Any]] = {}
        
        for doc in documentos:
            analisar_documento(doc, campos_info, prefixo="")
        
        # Calcular percentuais e formatar resultado
        for campo, info in campos_info.items():
            info["percentual"] = round((info["frequencia"] / docs_para_analisar) * 100, 2)
            info["tipos"] = list(info["tipos"])  # Converter set para list
        
        # Ordenar campos por frequência (mais comum primeiro)
        campos_ordenados = dict(
            sorted(
                campos_info.items(),
                key=lambda x: x[1]["frequencia"],
                reverse=True
            )
        )
        
        return json.dumps({
            "sucesso": True,
            "dados": {
                "total_documentos": total_documentos,
                "documentos_analisados": docs_para_analisar,
                "campos": campos_ordenados
            }
        }, ensure_ascii=False, indent=2)
    
    except errors.OperationFailure as e:
        return json.dumps({
            "sucesso": False,
            "erro": {
                "tipo": "OperationFailure",
                "mensagem": f"Operação falhou ao analisar schema da coleção '{nome_colecao}': {str(e)}"
            }
        }, ensure_ascii=False, indent=2)
    
    except Exception as e:
        return json.dumps({
            "sucesso": False,
            "erro": {
                "tipo": type(e).__name__,
                "mensagem": str(e)
            }
        }, ensure_ascii=False, indent=2)


def analisar_documento(
    doc: Dict[str, Any],
    campos_info: Dict[str, Dict[str, Any]],
    prefixo: str = ""
) -> None:
    """
    Função auxiliar recursiva para analisar campos de um documento.
    
    Analisa documentos aninhados e arrays, criando nomes de campos com notação de ponto.
    
    Args:
        doc: Documento (ou sub-documento) a ser analisado
        campos_info: Dicionário acumulador com informações dos campos
        prefixo: Prefixo para campos aninhados (ex: "endereco.")
    """
    for campo, valor in doc.items():
        nome_completo = f"{prefixo}{campo}" if prefixo else campo
        
        # Determinar tipo do valor
        tipo_valor = obter_tipo_mongodb(valor)
        
        # Inicializar info do campo se não existir
        if nome_completo not in campos_info:
            campos_info[nome_completo] = {
                "tipos": set(),
                "frequencia": 0,
                "exemplo": None
            }
        
        # Adicionar tipo
        campos_info[nome_completo]["tipos"].add(tipo_valor)
        
        # Incrementar frequência
        campos_info[nome_completo]["frequencia"] += 1
        
        # Guardar exemplo (apenas se ainda não tem)
        if campos_info[nome_completo]["exemplo"] is None:
            campos_info[nome_completo]["exemplo"] = formatar_exemplo(valor)
        
        # Se for dict, analisar recursivamente (documentos aninhados)
        if isinstance(valor, dict) and tipo_valor != "ObjectId":
            analisar_documento(valor, campos_info, f"{nome_completo}.")
        
        # Se for lista, analisar primeiro elemento
        elif isinstance(valor, list) and len(valor) > 0:
            primeiro_item = valor[0]
            if isinstance(primeiro_item, dict):
                analisar_documento(primeiro_item, campos_info, f"{nome_completo}[].")


def obter_tipo_mongodb(valor: Any) -> str:
    """
    Determina o tipo MongoDB de um valor.
    
    Args:
        valor: Valor a ser analisado
    
    Returns:
        String com o nome do tipo MongoDB
    """
    from bson import ObjectId
    from datetime import datetime
    
    if valor is None:
        return "null"
    elif isinstance(valor, ObjectId):
        return "ObjectId"
    elif isinstance(valor, bool):
        return "bool"
    elif isinstance(valor, int):
        return "int"
    elif isinstance(valor, float):
        return "double"
    elif isinstance(valor, str):
        return "string"
    elif isinstance(valor, datetime):
        return "date"
    elif isinstance(valor, dict):
        return "object"
    elif isinstance(valor, list):
        return "array"
    elif isinstance(valor, bytes):
        return "binData"
    else:
        return type(valor).__name__


def formatar_exemplo(valor: Any) -> Any:
    """
    Formata um valor para ser usado como exemplo no schema.
    
    Args:
        valor: Valor a ser formatado
    
    Returns:
        Valor formatado (strings longas são truncadas, ObjectIds convertidos)
    """
    from bson import ObjectId
    from datetime import datetime
    
    if isinstance(valor, ObjectId):
        return str(valor)
    elif isinstance(valor, datetime):
        return valor.isoformat()
    elif isinstance(valor, str):
        # Truncar strings muito longas
        if len(valor) > 100:
            return valor[:100] + "..."
        return valor
    elif isinstance(valor, (list, dict)):
        # Para arrays e objetos, mostrar estrutura simplificada
        if isinstance(valor, list):
            if len(valor) == 0:
                return []
            elif len(valor) == 1:
                return [formatar_exemplo(valor[0])]
            else:
                return [formatar_exemplo(valor[0]), "..."]
        else:
            # Para objetos, mostrar apenas as chaves
            return f"{{ {len(valor)} campos }}"
    else:
        return valor


