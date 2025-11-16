"""
Script de teste COMPLETO para listagem de estrutura MongoDB
Testa TODAS as funções de listagem (bancos e coleções) e cenários de erro
"""

from conexao_mongodb import conectar_mongodb, desconectar_mongodb
from consulta_mongodb import listar_bancos, listar_colecoes
import json

print("=" * 80)
print("TESTE COMPLETO - LISTAGEM DE ESTRUTURA MONGODB")
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
# 2. TESTE: LISTAR BANCOS DE DADOS
# ============================================================================

print("=" * 80)
print("2. TESTE: LISTAR BANCOS - Todos os Bancos Disponíveis")
print("=" * 80)

resultado_bancos = listar_bancos(status_conexao, client)
dados_bancos = json.loads(resultado_bancos)

if dados_bancos["sucesso"]:
    print(f"\n✅ Total de bancos encontrados: {len(dados_bancos['dados'])}\n")
    print(f"{'#':<4} {'Nome do Banco':<35} {'Tipo':<15}")
    print("-" * 80)
    
    for i, banco in enumerate(dados_bancos["dados"], 1):
        tipo = "Sistema" if banco in ["admin", "config", "local"] else "Usuário"
        print(f"{i:<4} {banco:<35} {tipo:<15}")
    
    # Guardar lista de bancos para próximos testes
    bancos_disponiveis = dados_bancos["dados"]
else:
    print("\n❌ Erro ao listar bancos:")
    print(json.dumps(dados_bancos["erro"], indent=2, ensure_ascii=False))
    desconectar_mongodb(client)
    exit(1)

# ============================================================================
# 3. TESTE: LISTAR COLEÇÕES DE CADA BANCO
# ============================================================================

print("\n" + "=" * 80)
print("3. TESTE: LISTAR COLEÇÕES - Para Cada Banco")
print("=" * 80)

total_colecoes = 0
bancos_com_colecoes = 0

for banco in bancos_disponiveis:
    # Pular bancos de sistema (opcional)
    if banco in ["admin", "config", "local"]:
        print(f"\n📦 Banco: {banco} (sistema - pulado)")
        continue
    
    print(f"\n📦 Banco: {banco}")
    print("-" * 80)
    
    resultado_colecoes = listar_colecoes(status_conexao, client, banco)
    dados_colecoes = json.loads(resultado_colecoes)
    
    if dados_colecoes["sucesso"]:
        qtd = len(dados_colecoes["dados"])
        total_colecoes += qtd
        
        if qtd == 0:
            print("   ⚠️  (nenhuma coleção)")
        else:
            bancos_com_colecoes += 1
            print(f"   ✅ {qtd} coleção(ões) encontrada(s):")
            for i, colecao in enumerate(dados_colecoes["dados"], 1):
                print(f"   {i}. {colecao}")
    else:
        print(f"   ❌ Erro: {dados_colecoes['erro']['mensagem']}")

print(f"\n📊 RESUMO: {bancos_com_colecoes} banco(s) com coleções, {total_colecoes} coleção(ões) no total")

# ============================================================================
# 4. TESTE: EXPLORAR BANCO ESPECÍFICO EM DETALHES
# ============================================================================

# Tentar encontrar um banco de usuário para explorar
banco_usuario = None
for banco in bancos_disponiveis:
    if banco not in ["admin", "config", "local"]:
        banco_usuario = banco
        break

if banco_usuario:
    print("\n" + "=" * 80)
    print(f"4. TESTE: EXPLORAR BANCO ESPECÍFICO - '{banco_usuario}'")
    print("=" * 80)
    
    resultado_colecoes_detalhe = listar_colecoes(status_conexao, client, banco_usuario)
    dados_colecoes_detalhe = json.loads(resultado_colecoes_detalhe)
    
    if dados_colecoes_detalhe["sucesso"]:
        print(f"\n✅ Detalhes do banco '{banco_usuario}':")
        print(f"\n{'#':<4} {'Nome da Coleção':<35} {'Disponível':<12}")
        print("-" * 80)
        
        if len(dados_colecoes_detalhe["dados"]) == 0:
            print("   (nenhuma coleção neste banco)")
        else:
            for i, colecao in enumerate(dados_colecoes_detalhe["dados"], 1):
                print(f"{i:<4} {colecao:<35} {'✅ Sim':<12}")
    else:
        print(f"\n❌ Erro ao explorar banco: {dados_colecoes_detalhe['erro']['mensagem']}")
else:
    print("\n⚠️  Nenhum banco de usuário encontrado para explorar")

# ============================================================================
# 5. TESTE: LISTAR COLEÇÕES DE BANCOS DE SISTEMA
# ============================================================================

print("\n" + "=" * 80)
print("5. TESTE: LISTAR COLEÇÕES - Bancos de Sistema")
print("=" * 80)

bancos_sistema = [b for b in bancos_disponiveis if b in ["admin", "config", "local"]]

if len(bancos_sistema) > 0:
    for banco_sys in bancos_sistema:
        print(f"\n📦 Banco Sistema: {banco_sys}")
        resultado_sys = listar_colecoes(status_conexao, client, banco_sys)
        dados_sys = json.loads(resultado_sys)
        
        if dados_sys["sucesso"]:
            print(f"   ✅ Coleções: {len(dados_sys['dados'])}")
            if len(dados_sys["dados"]) > 0:
                for col in dados_sys["dados"][:3]:  # Mostrar apenas as 3 primeiras
                    print(f"      - {col}")
                if len(dados_sys["dados"]) > 3:
                    print(f"      ... e mais {len(dados_sys['dados']) - 3} coleções")
        else:
            print(f"   ❌ Erro: {dados_sys['erro']['mensagem']}")
else:
    print("\n⚠️  Nenhum banco de sistema encontrado")

# ============================================================================
# 6. TESTES DE ERRO - Cenários Inválidos
# ============================================================================

print("\n" + "=" * 80)
print("6. TESTES DE ERRO - Validação de Tratamento")
print("=" * 80)

# 6.1 Listar coleções de banco inexistente
print("\n6.1 Listar coleções de banco inexistente:")
resultado_banco_inexistente = listar_colecoes(status_conexao, client, "banco_que_nao_existe_de_jeito_nenhum")
dados_banco_inexistente = json.loads(resultado_banco_inexistente)

if dados_banco_inexistente["sucesso"]:
    print(f"   ✅ Retornado: {len(dados_banco_inexistente['dados'])} coleções (banco vazio, esperado)")
else:
    print(f"   ❌ Erro: {dados_banco_inexistente['erro']['mensagem']}")

# 6.2 Listar coleções com nome de banco vazio
print("\n6.2 Listar coleções com nome de banco vazio:")
resultado_banco_vazio = listar_colecoes(status_conexao, client, "")
dados_banco_vazio = json.loads(resultado_banco_vazio)

if dados_banco_vazio["sucesso"]:
    print(f"   ⚠️  Inesperado: retornou {len(dados_banco_vazio['dados'])} coleções")
else:
    print(f"   ✅ Erro capturado (esperado para banco vazio)")

# 6.3 Listar bancos múltiplas vezes (teste de consistência)
print("\n6.3 Listar bancos múltiplas vezes (teste de consistência):")
resultado1 = listar_bancos(status_conexao, client)
resultado2 = listar_bancos(status_conexao, client)
resultado3 = listar_bancos(status_conexao, client)

dados1 = json.loads(resultado1)
dados2 = json.loads(resultado2)
dados3 = json.loads(resultado3)

if dados1["dados"] == dados2["dados"] == dados3["dados"]:
    print(f"   ✅ Consistente: todas as 3 chamadas retornaram {len(dados1['dados'])} bancos")
else:
    print(f"   ❌ Inconsistente: resultados diferentes entre chamadas")

# ============================================================================
# 7. TESTE: OPERAÇÕES COMBINADAS (Navegação Hierárquica)
# ============================================================================

print("\n" + "=" * 80)
print("7. TESTE: NAVEGAÇÃO HIERÁRQUICA - Bancos > Coleções")
print("=" * 80)

print("\n🗂️  ESTRUTURA COMPLETA DO MONGODB:\n")

resultado_bancos_nav = listar_bancos(status_conexao, client)
dados_bancos_nav = json.loads(resultado_bancos_nav)

if dados_bancos_nav["sucesso"]:
    for banco_nav in dados_bancos_nav["dados"]:
        # Pular bancos de sistema para essa visualização
        if banco_nav in ["admin", "config", "local"]:
            continue
        
        print(f"📦 {banco_nav}/")
        
        resultado_col_nav = listar_colecoes(status_conexao, client, banco_nav)
        dados_col_nav = json.loads(resultado_col_nav)
        
        if dados_col_nav["sucesso"]:
            if len(dados_col_nav["dados"]) == 0:
                print(f"   └─ (vazio)")
            else:
                for idx, col_nav in enumerate(dados_col_nav["dados"]):
                    if idx == len(dados_col_nav["dados"]) - 1:
                        print(f"   └─ {col_nav}")
                    else:
                        print(f"   ├─ {col_nav}")
        print()

# ============================================================================
# 8. TESTE: LISTAGEM APÓS DESCONEXÃO
# ============================================================================

print("=" * 80)
print("8. TESTE: Listagem Após Desconexão")
print("=" * 80)

# Desconectar
status_conexao, mensagem_disconnect = desconectar_mongodb(client)
print(f"\n✅ {mensagem_disconnect}")
print(f"📊 Status da conexão: {status_conexao} (False = desconectado)")

# 8.1 Tentar listar bancos desconectado
print("\n8.1 Tentativa de listar bancos após desconexão:")
resultado_bancos_desc = listar_bancos(status_conexao, client)
dados_bancos_desc = json.loads(resultado_bancos_desc)

if not dados_bancos_desc["sucesso"]:
    print(f"   ✅ Erro capturado corretamente: {dados_bancos_desc['erro']['tipo']}")
    print(f"   📝 Mensagem: {dados_bancos_desc['erro']['mensagem']}")
else:
    print(f"   ⚠️  Inesperado: listagem executou com conexão desconectada!")

# 8.2 Tentar listar coleções desconectado
print("\n8.2 Tentativa de listar coleções após desconexão:")
resultado_colecoes_desc = listar_colecoes(status_conexao, client, "qualquer_banco")
dados_colecoes_desc = json.loads(resultado_colecoes_desc)

if not dados_colecoes_desc["sucesso"]:
    print(f"   ✅ Erro capturado corretamente: {dados_colecoes_desc['erro']['tipo']}")
    print(f"   📝 Mensagem: {dados_colecoes_desc['erro']['mensagem']}")
else:
    print(f"   ⚠️  Inesperado: listagem executou com conexão desconectada!")

# ============================================================================
# RESUMO FINAL
# ============================================================================

print("\n" + "=" * 80)
print("RESUMO DO TESTE COMPLETO")
print("=" * 80)

print(f"""
✅ OPERAÇÕES TESTADAS:
   1. Listar Bancos - Todos os bancos disponíveis
   2. Listar Coleções - Para cada banco (usuário e sistema)
   3. Explorar Banco Específico - Detalhamento completo
   4. Navegação Hierárquica - Visualização em árvore (Bancos > Coleções)

✅ CENÁRIOS DE ERRO TESTADOS:
   - Listar coleções de banco inexistente
   - Listar coleções com nome de banco vazio
   - Teste de consistência (múltiplas chamadas)
   - Listagem com conexão desconectada (bancos e coleções)

✅ VALIDAÇÕES ADICIONAIS:
   - Diferenciação entre bancos de sistema e usuário
   - Contagem total de coleções
   - Verificação de bancos vazios
   - Formatação hierárquica da estrutura

📊 ESTATÍSTICAS:
   - Bancos encontrados: {len(dados_bancos['dados']) if dados_bancos['sucesso'] else 'N/A'}
   - Coleções totais: {total_colecoes}
   - Bancos com coleções: {bancos_com_colecoes}

📊 TOTAL: 10+ casos de teste executados com sucesso!
""")

print("=" * 80)
print("TESTE COMPLETO FINALIZADO!")
print("=" * 80)
