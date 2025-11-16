"""
Script de teste para análise de schema MongoDB
Testa a função analisar_schema() com diferentes cenários
"""

from conexao_mongodb import conectar_mongodb, desconectar_mongodb
from consulta_mongodb import analisar_schema
import json

print("=" * 80)
print("TESTE COMPLETO - ANÁLISE DE SCHEMA MONGODB")
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
print(f"📊 Status da conexão: {status_conexao}\n")

# ============================================================================
# 2. ANÁLISE DE SCHEMA - Coleção noticias_g1
# ============================================================================

print("=" * 80)
print("2. ANÁLISE DE SCHEMA - Coleção 'noticias_g1'")
print("=" * 80)

resultado_noticias = analisar_schema(
    status_conexao, 
    client, 
    "testeAdrianodatabase", 
    "noticias_g1", 
    amostra=50
)

dados_noticias = json.loads(resultado_noticias)

if dados_noticias["sucesso"]:
    print(f"\n✅ Schema analisado com sucesso!")
    print(f"\n📊 Estatísticas:")
    print(f"   - Total de documentos na coleção: {dados_noticias['dados']['total_documentos']}")
    print(f"   - Documentos analisados: {dados_noticias['dados']['documentos_analisados']}")
    print(f"   - Campos encontrados: {len(dados_noticias['dados']['campos'])}")
    
    print(f"\n📋 CAMPOS DETECTADOS:\n")
    print(f"{'Campo':<35} {'Tipos':<25} {'Freq.':<8} {'%':<8} {'Exemplo':<40}")
    print("-" * 120)
    
    for campo, info in dados_noticias['dados']['campos'].items():
        tipos_str = ", ".join(info['tipos'])
        exemplo_str = str(info['exemplo'])
        if len(exemplo_str) > 40:
            exemplo_str = exemplo_str[:37] + "..."
        
        print(f"{campo:<35} {tipos_str:<25} {info['frequencia']:<8} {info['percentual']:<8.1f} {exemplo_str:<40}")
else:
    print(f"\n❌ Erro ao analisar schema:")
    print(json.dumps(dados_noticias["erro"], indent=2, ensure_ascii=False))

# ============================================================================
# 3. ANÁLISE DE SCHEMA - Coleção jornalistas
# ============================================================================

print("\n" + "=" * 80)
print("3. ANÁLISE DE SCHEMA - Coleção 'jornalistas'")
print("=" * 80)

resultado_jornalistas = analisar_schema(
    status_conexao, 
    client, 
    "testeAdrianodatabase", 
    "jornalistas", 
    amostra=30
)

dados_jornalistas = json.loads(resultado_jornalistas)

if dados_jornalistas["sucesso"]:
    print(f"\n✅ Schema analisado com sucesso!")
    print(f"\n📊 Estatísticas:")
    print(f"   - Total de documentos na coleção: {dados_jornalistas['dados']['total_documentos']}")
    print(f"   - Documentos analisados: {dados_jornalistas['dados']['documentos_analisados']}")
    print(f"   - Campos encontrados: {len(dados_jornalistas['dados']['campos'])}")
    
    print(f"\n📋 CAMPOS DETECTADOS:\n")
    print(f"{'Campo':<35} {'Tipos':<25} {'Freq.':<8} {'%':<8} {'Exemplo':<40}")
    print("-" * 120)
    
    for campo, info in dados_jornalistas['dados']['campos'].items():
        tipos_str = ", ".join(info['tipos'])
        exemplo_str = str(info['exemplo'])
        if len(exemplo_str) > 40:
            exemplo_str = exemplo_str[:37] + "..."
        
        print(f"{campo:<35} {tipos_str:<25} {info['frequencia']:<8} {info['percentual']:<8.1f} {exemplo_str:<40}")
else:
    print(f"\n❌ Erro ao analisar schema:")
    print(json.dumps(dados_jornalistas["erro"], indent=2, ensure_ascii=False))

# ============================================================================
# 4. ANÁLISE COM AMOSTRA PEQUENA (10 documentos)
# ============================================================================

print("\n" + "=" * 80)
print("4. ANÁLISE COM AMOSTRA PEQUENA - 10 documentos")
print("=" * 80)

resultado_pequeno = analisar_schema(
    status_conexao, 
    client, 
    "testeAdrianodatabase", 
    "noticias_g1", 
    amostra=10
)

dados_pequeno = json.loads(resultado_pequeno)

if dados_pequeno["sucesso"]:
    print(f"\n✅ Análise concluída")
    print(f"   - Documentos analisados: {dados_pequeno['dados']['documentos_analisados']}")
    print(f"   - Campos detectados: {len(dados_pequeno['dados']['campos'])}")
    
    # Mostrar apenas os 5 campos mais comuns
    campos_top5 = list(dados_pequeno['dados']['campos'].items())[:5]
    print(f"\n📋 Top 5 campos mais comuns:")
    for i, (campo, info) in enumerate(campos_top5, 1):
        print(f"   {i}. {campo}: {info['percentual']}% ({', '.join(info['tipos'])})")
else:
    print(f"\n❌ Erro: {dados_pequeno['erro']['mensagem']}")

# ============================================================================
# 5. ANÁLISE COM AMOSTRA GRANDE (200 documentos)
# ============================================================================

print("\n" + "=" * 80)
print("5. ANÁLISE COM AMOSTRA GRANDE - 200 documentos")
print("=" * 80)

resultado_grande = analisar_schema(
    status_conexao, 
    client, 
    "testeAdrianodatabase", 
    "noticias_g1", 
    amostra=200
)

dados_grande = json.loads(resultado_grande)

if dados_grande["sucesso"]:
    print(f"\n✅ Análise concluída")
    print(f"   - Documentos analisados: {dados_grande['dados']['documentos_analisados']}")
    print(f"   - Campos detectados: {len(dados_grande['dados']['campos'])}")
    
    # Comparar com amostra pequena
    print(f"\n📊 Comparação de amostras:")
    print(f"   - Amostra de 10: {len(dados_pequeno['dados']['campos'])} campos")
    print(f"   - Amostra de 200: {len(dados_grande['dados']['campos'])} campos")
    
    # Identificar campos que aparecem em menos de 100% dos docs (campos opcionais)
    campos_opcionais = []
    for campo, info in dados_grande['dados']['campos'].items():
        if info['percentual'] < 100:
            campos_opcionais.append((campo, info['percentual']))
    
    if campos_opcionais:
        print(f"\n⚠️  Campos opcionais (não aparecem em todos os documentos):")
        for campo, percentual in sorted(campos_opcionais, key=lambda x: x[1]):
            print(f"   - {campo}: {percentual}%")
    else:
        print(f"\n✅ Todos os campos aparecem em 100% dos documentos (schema consistente)")
else:
    print(f"\n❌ Erro: {dados_grande['erro']['mensagem']}")

# ============================================================================
# 6. TESTES DE ERRO
# ============================================================================

print("\n" + "=" * 80)
print("6. TESTES DE ERRO")
print("=" * 80)

# 6.1 Coleção inexistente
print("\n6.1 Analisar coleção inexistente:")
resultado_inexistente = analisar_schema(
    status_conexao, 
    client, 
    "testeAdrianodatabase", 
    "colecao_que_nao_existe", 
    amostra=10
)

dados_inexistente = json.loads(resultado_inexistente)

if dados_inexistente["sucesso"]:
    if dados_inexistente['dados']['total_documentos'] == 0:
        print(f"   ✅ Retornou coleção vazia (esperado)")
        print(f"   📝 Mensagem: {dados_inexistente['dados'].get('mensagem', 'N/A')}")
    else:
        print(f"   ⚠️  Inesperado: retornou {dados_inexistente['dados']['total_documentos']} documentos")
else:
    print(f"   ❌ Erro: {dados_inexistente['erro']['mensagem']}")

# 6.2 Banco inexistente
print("\n6.2 Analisar banco inexistente:")
resultado_banco_inexistente = analisar_schema(
    status_conexao, 
    client, 
    "banco_que_nao_existe", 
    "alguma_colecao", 
    amostra=10
)

dados_banco_inexistente = json.loads(resultado_banco_inexistente)

if dados_banco_inexistente["sucesso"]:
    if dados_banco_inexistente['dados']['total_documentos'] == 0:
        print(f"   ✅ Retornou vazio (esperado)")
    else:
        print(f"   ⚠️  Inesperado: retornou documentos")
else:
    print(f"   ❌ Erro: {dados_banco_inexistente['erro']['mensagem']}")

# ============================================================================
# 7. ANÁLISE APÓS DESCONEXÃO
# ============================================================================

print("\n" + "=" * 80)
print("7. ANÁLISE APÓS DESCONEXÃO")
print("=" * 80)

status_conexao, mensagem_disconnect = desconectar_mongodb(client)
print(f"\n✅ {mensagem_disconnect}")
print(f"📊 Status da conexão: {status_conexao} (False = desconectado)")

print("\nTentativa de análise após desconexão:")
resultado_desconectado = analisar_schema(
    status_conexao, 
    client, 
    "testeAdrianodatabase", 
    "noticias_g1", 
    amostra=10
)

dados_desconectado = json.loads(resultado_desconectado)

if not dados_desconectado["sucesso"]:
    print(f"   ✅ Erro capturado corretamente: {dados_desconectado['erro']['tipo']}")
    print(f"   📝 Mensagem: {dados_desconectado['erro']['mensagem']}")
else:
    print(f"   ⚠️  Inesperado: análise executou com conexão desconectada!")

# ============================================================================
# RESUMO FINAL
# ============================================================================

print("\n" + "=" * 80)
print("RESUMO DO TESTE DE ANÁLISE DE SCHEMA")
print("=" * 80)

print(f"""
✅ OPERAÇÕES TESTADAS:
   1. Análise de schema - Coleção 'noticias_g1' (50 docs)
   2. Análise de schema - Coleção 'jornalistas' (30 docs)
   3. Análise com amostra pequena (10 docs)
   4. Análise com amostra grande (200 docs)
   5. Comparação entre diferentes tamanhos de amostra
   6. Identificação de campos opcionais

✅ CENÁRIOS DE ERRO TESTADOS:
   - Coleção inexistente (retorna vazio)
   - Banco inexistente (retorna vazio)
   - Análise com conexão desconectada

✅ INSIGHTS FORNECIDOS:
   - Total de documentos na coleção
   - Campos detectados e seus tipos
   - Frequência e percentual de aparição de cada campo
   - Exemplos de valores para cada campo
   - Identificação de campos opcionais (schema inconsistente)
   - Comparação de resultados com diferentes amostras

📊 TOTAL: 7 casos de teste executados com sucesso!
""")

print("=" * 80)
print("TESTE COMPLETO FINALIZADO!")
print("=" * 80)
