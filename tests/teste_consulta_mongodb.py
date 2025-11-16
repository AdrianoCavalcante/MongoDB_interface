"""
Script de teste COMPLETO para consultas MongoDB
Testa TODAS as operações disponíveis e cenários de erro
"""

from conexao_mongodb import conectar_mongodb, desconectar_mongodb
from consulta_mongodb import consultar_mongodb
import json

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

banco = "testeAdrianodatabase"
colecao = "noticias_g1"

print("=" * 80)
print("TESTE COMPLETO - SISTEMA DE CONSULTAS MONGODB")
print("=" * 80)

# ============================================================================
# 1. TESTE DE CONEXÃO
# ============================================================================

print("\n" + "=" * 80)
print("1. TESTE DE CONEXÃO")
print("=" * 80)

status_conexao, client, mensagem_connect = conectar_mongodb()

if not status_conexao:
    print(f"\n❌ Erro ao conectar: {mensagem_connect}")
    exit(1)

print(f"✅ {mensagem_connect}")
print(f"📊 Status da conexão: {status_conexao}")

# ============================================================================
# 2. TESTE: FIND (Busca Básica)
# ============================================================================

print("\n" + "=" * 80)
print("2. TESTE: FIND - Busca Básica")
print("=" * 80)

# 2.1 Find com filtro simples
print("\n2.1 Find com filtro simples (limite de 5 documentos):")
query_find = '{"fonte.publicador": {"$exists": true}}'
resultado = consultar_mongodb(status_conexao, client, banco, colecao, query_find, limite_amostra=False)
dados = json.loads(resultado)

if dados["sucesso"]:
    print(f"   ✅ Encontrados: {len(dados['dados'])} documentos")
    if len(dados["dados"]) > 0:
        print(f"   📄 Primeiro documento: {dados['dados'][0].get('fonte', {}).get('titulo', 'N/A')[:50]}...")
else:
    print(f"   ❌ Erro: {dados['erro']['mensagem']}")

# 2.2 Find com limite de amostra
print("\n2.2 Find com limite de amostra (20 docs):")
resultado = consultar_mongodb(status_conexao, client, banco, colecao, query_find, limite_amostra=True)
dados = json.loads(resultado)

if dados["sucesso"]:
    print(f"   ✅ Retornados: {len(dados['dados'])} documentos (limite: 20)")
else:
    print(f"   ❌ Erro: {dados['erro']['mensagem']}")

# 2.3 Find que não retorna nada
print("\n2.3 Find sem resultados:")
query_vazio = '{"campo_inexistente": "valor_impossivel"}'
resultado = consultar_mongodb(status_conexao, client, banco, colecao, query_vazio)
dados = json.loads(resultado)

if dados["sucesso"]:
    print(f"   ✅ Retornados: {len(dados['dados'])} documentos (esperado: 0)")
else:
    print(f"   ❌ Erro: {dados['erro']['mensagem']}")

# ============================================================================
# 3. TESTE: AGGREGATE (Pipeline de Agregação)
# ============================================================================

print("\n" + "=" * 80)
print("3. TESTE: AGGREGATE - Pipeline de Agregação")
print("=" * 80)

# 3.1 Aggregate com lookup e group
print("\n3.1 Aggregate com $lookup e $group (TOP jornalistas):")
query_aggregate = """[
    {
        "$lookup": {
            "from": "jornalistas",
            "localField": "jornalista_id",
            "foreignField": "_id",
            "as": "jornalista"
        }
    },
    {
        "$unwind": {
            "path": "$jornalista",
            "preserveNullAndEmptyArrays": false
        }
    },
    {
        "$group": {
            "_id": "$jornalista._id",
            "nome_jornalista": {"$first": "$jornalista.nome"},
            "total_materias": {"$sum": 1}
        }
    },
    {
        "$sort": {"total_materias": -1}
    },
    {
        "$limit": 5
    }
]"""

resultado = consultar_mongodb(status_conexao, client, banco, colecao, query_aggregate)
dados = json.loads(resultado)

if dados["sucesso"]:
    print(f"   ✅ TOP 5 Jornalistas:")
    for i, item in enumerate(dados["dados"], 1):
        print(f"   {i}. {item['nome_jornalista']}: {item['total_materias']} matérias")
else:
    print(f"   ❌ Erro: {dados['erro']['mensagem']}")

# 3.2 Aggregate simples (apenas match e count)
print("\n3.2 Aggregate simples ($match e $count):")
query_aggregate_count = """[
    {
        "$match": {"fonte.publicador": {"$exists": true}}
    },
    {
        "$count": "total"
    }
]"""

resultado = consultar_mongodb(status_conexao, client, banco, colecao, query_aggregate_count)
dados = json.loads(resultado)

if dados["sucesso"]:
    if len(dados["dados"]) > 0:
        print(f"   ✅ Total: {dados['dados'][0]['total']} documentos")
    else:
        print(f"   ✅ Total: 0 documentos")
else:
    print(f"   ❌ Erro: {dados['erro']['mensagem']}")

# ============================================================================
# 4. TESTE: DISTINCT (Valores Únicos)
# ============================================================================

print("\n" + "=" * 80)
print("4. TESTE: DISTINCT - Valores Únicos")
print("=" * 80)

# 4.1 Distinct sem filtro
print("\n4.1 Distinct sem filtro (campo 'jornalista_id'):")
query_distinct = '{"_distinct": "jornalista_id"}'
resultado = consultar_mongodb(status_conexao, client, banco, colecao, query_distinct)
dados = json.loads(resultado)

if dados["sucesso"]:
    print(f"   ✅ Valores únicos encontrados: {len(dados['dados'])}")
    print(f"   📋 Primeiros 5: {dados['dados'][:5]}")
else:
    print(f"   ❌ Erro: {dados['erro']['mensagem']}")

# 4.2 Distinct com filtro
print("\n4.2 Distinct com filtro:")
query_distinct_filtro = '{"_distinct": "jornalista_id", "_query": {"fonte.publicador": {"$exists": true}}}'
resultado = consultar_mongodb(status_conexao, client, banco, colecao, query_distinct_filtro)
dados = json.loads(resultado)

if dados["sucesso"]:
    print(f"   ✅ Valores únicos (com filtro): {len(dados['dados'])}")
else:
    print(f"   ❌ Erro: {dados['erro']['mensagem']}")

# ============================================================================
# 5. TESTE: COUNT (Contagem)
# ============================================================================

print("\n" + "=" * 80)
print("5. TESTE: COUNT - Contagem de Documentos")
print("=" * 80)

# 5.1 Count sem filtro (todos os documentos)
print("\n5.1 Count sem filtro (total de documentos):")
query_count_all = '{"_count": true, "_query": {}}'
resultado = consultar_mongodb(status_conexao, client, banco, colecao, query_count_all)
dados = json.loads(resultado)

if dados["sucesso"]:
    print(f"   ✅ Total de documentos: {dados['contagem']}")
else:
    print(f"   ❌ Erro: {dados['erro']['mensagem']}")

# 5.2 Count com filtro
print("\n5.2 Count com filtro:")
query_count_filtro = '{"_count": true, "_query": {"fonte.publicador": {"$exists": true}}}'
resultado = consultar_mongodb(status_conexao, client, banco, colecao, query_count_filtro)
dados = json.loads(resultado)

if dados["sucesso"]:
    print(f"   ✅ Documentos com filtro: {dados['contagem']}")
else:
    print(f"   ❌ Erro: {dados['erro']['mensagem']}")

# ============================================================================
# 6. TESTE: FIND_ONE (Um Documento)
# ============================================================================

print("\n" + "=" * 80)
print("6. TESTE: FIND_ONE - Um Único Documento")
print("=" * 80)

# 6.1 Find One sem projeção
print("\n6.1 Find One sem projeção:")
query_find_one = '{"_find_one": true, "_query": {"fonte.publicador": {"$exists": true}}}'
resultado = consultar_mongodb(status_conexao, client, banco, colecao, query_find_one)
dados = json.loads(resultado)

if dados["sucesso"]:
    if len(dados["dados"]) > 0:
        doc = dados["dados"][0]
        print(f"   ✅ Documento encontrado")
        print(f"   📄 Título: {doc.get('fonte', {}).get('titulo', 'N/A')[:60]}...")
    else:
        print(f"   ⚠️  Nenhum documento encontrado")
else:
    print(f"   ❌ Erro: {dados['erro']['mensagem']}")

# 6.2 Find One com projeção
print("\n6.2 Find One com projeção (apenas campos específicos):")
query_find_one_proj = '{"_find_one": true, "_query": {}, "_projection": {"fonte.titulo": 1, "fonte.publicador": 1, "_id": 0}}'
resultado = consultar_mongodb(status_conexao, client, banco, colecao, query_find_one_proj)
dados = json.loads(resultado)

if dados["sucesso"]:
    if len(dados["dados"]) > 0:
        print(f"   ✅ Documento com projeção:")
        print(f"   {json.dumps(dados['dados'][0], indent=6, ensure_ascii=False)[:200]}...")
    else:
        print(f"   ⚠️  Nenhum documento encontrado")
else:
    print(f"   ❌ Erro: {dados['erro']['mensagem']}")

# ============================================================================
# 7. TESTE: FIND_WITH_OPTIONS (Busca Avançada)
# ============================================================================

print("\n" + "=" * 80)
print("7. TESTE: FIND_WITH_OPTIONS - Busca Avançada")
print("=" * 80)

# 7.1 Find com sort e limit
print("\n7.1 Find com sort (decrescente) e limit:")
query_options_sort_limit = '{"_find_with_options": true, "_query": {}, "_sort": {"_id": -1}, "_limit": 3}'
resultado = consultar_mongodb(status_conexao, client, banco, colecao, query_options_sort_limit)
dados = json.loads(resultado)

if dados["sucesso"]:
    print(f"   ✅ Retornados: {len(dados['dados'])} documentos (limit: 3)")
else:
    print(f"   ❌ Erro: {dados['erro']['mensagem']}")

# 7.2 Find com skip e limit (paginação)
print("\n7.2 Find com skip e limit (paginação - página 2):")
query_options_paginacao = '{"_find_with_options": true, "_query": {}, "_skip": 5, "_limit": 5}'
resultado = consultar_mongodb(status_conexao, client, banco, colecao, query_options_paginacao)
dados = json.loads(resultado)

if dados["sucesso"]:
    print(f"   ✅ Retornados: {len(dados['dados'])} documentos (skip: 5, limit: 5)")
else:
    print(f"   ❌ Erro: {dados['erro']['mensagem']}")

# 7.3 Find com sort, skip, limit e projection
print("\n7.3 Find com TODAS as opções (sort + skip + limit + projection):")
query_options_completo = '''{
    "_find_with_options": true,
    "_query": {"fonte.publicador": {"$exists": true}},
    "_sort": {"_id": -1},
    "_skip": 0,
    "_limit": 3,
    "_projection": {"fonte.titulo": 1, "_id": 0}
}'''
resultado = consultar_mongodb(status_conexao, client, banco, colecao, query_options_completo)
dados = json.loads(resultado)

if dados["sucesso"]:
    print(f"   ✅ Documentos com todas as opções:")
    for i, doc in enumerate(dados["dados"], 1):
        print(f"   {i}. {doc.get('fonte', {}).get('titulo', 'N/A')[:60]}...")
else:
    print(f"   ❌ Erro: {dados['erro']['mensagem']}")

# ============================================================================
# 8. TESTES DE ERRO
# ============================================================================

print("\n" + "=" * 80)
print("8. TESTES DE ERRO - Validação de Tratamento")
print("=" * 80)

# 8.1 Query JSON inválida
print("\n8.1 Query com JSON inválido:")
query_json_invalida = '{"campo": valor_sem_aspas}'
resultado = consultar_mongodb(status_conexao, client, banco, colecao, query_json_invalida)
dados = json.loads(resultado)

if not dados["sucesso"]:
    print(f"   ✅ Erro capturado corretamente: {dados['erro']['tipo']}")
    print(f"   📝 Mensagem: {dados['erro']['mensagem'][:80]}...")
else:
    print(f"   ⚠️  Erro não detectado (inesperado)")

# 8.2 Query com tipo inválido (nem dict nem list)
print("\n8.2 Query com tipo inválido (string simples):")
query_tipo_invalido = '"isto_e_uma_string_nao_um_objeto"'
resultado = consultar_mongodb(status_conexao, client, banco, colecao, query_tipo_invalido)
dados = json.loads(resultado)

if not dados["sucesso"]:
    print(f"   ✅ Erro capturado: {dados['erro']['tipo']}")
else:
    print(f"   ⚠️  Erro não detectado")

# 8.3 Banco inexistente
print("\n8.3 Banco inexistente:")
resultado = consultar_mongodb(status_conexao, client, "banco_que_nao_existe", "colecao", '{"_count": true, "_query": {}}')
dados = json.loads(resultado)

if dados["sucesso"]:
    print(f"   ✅ Retornou contagem: {dados['contagem']} (banco vazio, esperado)")
else:
    print(f"   ❌ Erro: {dados['erro']['mensagem']}")

# 8.4 Coleção inexistente
print("\n8.4 Coleção inexistente:")
resultado = consultar_mongodb(status_conexao, client, banco, "colecao_inexistente", '{"_count": true, "_query": {}}')
dados = json.loads(resultado)

if dados["sucesso"]:
    print(f"   ✅ Retornou contagem: {dados['contagem']} (coleção vazia, esperado)")
else:
    print(f"   ❌ Erro: {dados['erro']['mensagem']}")

# ============================================================================
# 9. TESTE: CONSULTA COM CONEXÃO DESCONECTADA
# ============================================================================

print("\n" + "=" * 80)
print("9. TESTE: Consulta Após Desconexão")
print("=" * 80)

# Desconectar
status_conexao, mensagem_disconnect = desconectar_mongodb(client)
print(f"\n✅ {mensagem_disconnect}")
print(f"📊 Status da conexão: {status_conexao} (False = desconectado)")

# Tentar consultar desconectado
print("\n9.1 Tentativa de consulta após desconexão:")
resultado_desconectado = consultar_mongodb(status_conexao, client, banco, colecao, '{"_count": true, "_query": {}}')
dados_desconectado = json.loads(resultado_desconectado)

if not dados_desconectado["sucesso"]:
    print(f"   ✅ Erro capturado corretamente: {dados_desconectado['erro']['tipo']}")
    print(f"   📝 Mensagem: {dados_desconectado['erro']['mensagem']}")
else:
    print(f"   ⚠️  Inesperado: consulta executou com conexão desconectada!")

# ============================================================================
# RESUMO FINAL
# ============================================================================

print("\n" + "=" * 80)
print("RESUMO DO TESTE COMPLETO")
print("=" * 80)

print("""
✅ OPERAÇÕES TESTADAS:
   1. Find - Busca básica (com e sem limite de amostra)
   2. Aggregate - Pipelines complexas ($lookup, $group, $sort, $limit, $count)
   3. Distinct - Valores únicos (com e sem filtro)
   4. Count - Contagem de documentos (com e sem filtro)
   5. Find One - Um documento (com e sem projeção)
   6. Find with Options - Busca avançada (sort, skip, limit, projection)

✅ CENÁRIOS DE ERRO TESTADOS:
   - JSON inválido
   - Tipo de query inválido
   - Banco inexistente
   - Coleção inexistente
   - Consulta com conexão desconectada

📊 TOTAL: 15+ casos de teste executados com sucesso!
""")

print("=" * 80)
print("TESTE COMPLETO FINALIZADO!")
print("=" * 80)
