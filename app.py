"""
Interface Streamlit para MongoDB Interface

Aplicação web interativa para consultas MongoDB Atlas.
"""

import streamlit as st
import json
import sys
from pathlib import Path

# Adicionar o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent))

from src.conexao_mongodb import conectar_mongodb, desconectar_mongodb
from src.consulta_mongodb import (
    consultar_mongodb,
    listar_bancos,
    listar_colecoes,
    analisar_schema
)

# Configuração da página
st.set_page_config(
    page_title="MongoDB Interface",
    page_icon="🍃",
    layout="wide"
)

# Título
st.title("🍃 MongoDB Interface")
st.markdown("Interface interativa para consultas MongoDB Atlas (Read-Only)")

# Sidebar para conexão
with st.sidebar:
    st.header("🔌 Conexão")
    
    if st.button("Conectar ao MongoDB", type="primary"):
        with st.spinner("Conectando..."):
            status, client, msg = conectar_mongodb()
            
            if status:
                st.session_state['connected'] = True
                st.session_state['client'] = client
                st.session_state['status'] = status
                st.success(msg)
            else:
                st.error(msg)
    
    if 'connected' in st.session_state and st.session_state['connected']:
        st.success("✅ Conectado")
        
        if st.button("Desconectar"):
            status, msg = desconectar_mongodb(st.session_state['client'])
            st.session_state['connected'] = False
            st.info(msg)
            st.rerun()

# Verificar se está conectado
if 'connected' not in st.session_state or not st.session_state['connected']:
    st.info("👈 Clique em 'Conectar ao MongoDB' na barra lateral para começar")
    st.stop()

# Tabs principais
tab1, tab2, tab3, tab4 = st.tabs(["📊 Consultar", "📁 Explorar", "🔍 Analisar Schema", "📖 Ajuda"])

with tab1:
    st.header("Executar Consulta")
    
    col1, col2 = st.columns(2)
    
    with col1:
        banco = st.text_input("Nome do Banco", placeholder="ex: meu_banco")
    
    with col2:
        colecao = st.text_input("Nome da Coleção", placeholder="ex: usuarios")
    
    tipo_query = st.selectbox(
        "Tipo de Consulta",
        ["Find", "Aggregate", "Distinct", "Count", "Find One", "Find com Opções"]
    )
    
    # Exemplos baseados no tipo
    exemplos = {
        "Find": '{"status": "ativo"}',
        "Aggregate": '[{"$match": {"status": "ativo"}}, {"$group": {"_id": "$categoria", "total": {"$sum": 1}}}]',
        "Distinct": '{"_distinct": "categoria", "_query": {"status": "ativo"}}',
        "Count": '{"_count": true, "_query": {"status": "ativo"}}',
        "Find One": '{"_find_one": true, "_query": {"_id": "123"}}',
        "Find com Opções": '{"_find_with_options": true, "_query": {"status": "ativo"}, "_sort": {"data": -1}, "_limit": 10}'
    }
    
    query = st.text_area(
        "Query JSON",
        value=exemplos[tipo_query],
        height=150,
        help="Digite sua query em formato JSON"
    )
    
    limite_amostra = st.checkbox("Limitar a 20 documentos", value=True)
    
    if st.button("🚀 Executar Consulta", type="primary"):
        if not banco or not colecao:
            st.warning("Por favor, preencha o nome do banco e da coleção")
        else:
            with st.spinner("Executando consulta..."):
                resultado = consultar_mongodb(
                    st.session_state['status'],
                    st.session_state['client'],
                    banco,
                    colecao,
                    query,
                    limite_amostra=limite_amostra
                )
                
                dados = json.loads(resultado)
                
                if dados["sucesso"]:
                    st.success(f"✅ Consulta executada com sucesso!")
                    st.metric("Documentos retornados", len(dados["dados"]))
                    
                    # Mostrar dados
                    st.json(dados["dados"])
                    
                    # Botão de download
                    st.download_button(
                        "📥 Baixar JSON",
                        data=json.dumps(dados["dados"], indent=2, ensure_ascii=False),
                        file_name=f"{banco}_{colecao}_resultado.json",
                        mime="application/json"
                    )
                else:
                    st.error(f"❌ Erro: {dados['erro']['mensagem']}")

with tab2:
    st.header("Explorar Bancos e Coleções")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📦 Bancos de Dados")
        
        if st.button("🔄 Listar Bancos"):
            with st.spinner("Buscando bancos..."):
                resultado = listar_bancos(
                    st.session_state['status'],
                    st.session_state['client']
                )
                dados = json.loads(resultado)
                
                if dados["sucesso"]:
                    st.session_state['bancos'] = dados["dados"]
                    st.success(f"✅ {len(dados['dados'])} bancos encontrados")
                else:
                    st.error(f"❌ Erro: {dados['erro']['mensagem']}")
        
        if 'bancos' in st.session_state:
            for banco in st.session_state['bancos']:
                if st.button(f"📁 {banco}", key=f"banco_{banco}"):
                    st.session_state['banco_selecionado'] = banco
    
    with col2:
        st.subheader("📄 Coleções")
        
        if 'banco_selecionado' in st.session_state:
            banco_sel = st.session_state['banco_selecionado']
            st.info(f"Banco: **{banco_sel}**")
            
            if st.button("🔄 Listar Coleções"):
                with st.spinner("Buscando coleções..."):
                    resultado = listar_colecoes(
                        st.session_state['status'],
                        st.session_state['client'],
                        banco_sel
                    )
                    dados = json.loads(resultado)
                    
                    if dados["sucesso"]:
                        st.session_state['colecoes'] = dados["dados"]
                        st.success(f"✅ {len(dados['dados'])} coleções encontradas")
                    else:
                        st.error(f"❌ Erro: {dados['erro']['mensagem']}")
            
            if 'colecoes' in st.session_state:
                for col in st.session_state['colecoes']:
                    st.write(f"• {col}")

with tab3:
    st.header("Analisar Schema de Coleção")
    
    col1, col2 = st.columns(2)
    
    with col1:
        banco_schema = st.text_input("Banco", key="banco_schema")
    
    with col2:
        colecao_schema = st.text_input("Coleção", key="colecao_schema")
    
    amostra = st.slider("Tamanho da Amostra", min_value=10, max_value=1000, value=100, step=10)
    
    if st.button("🔍 Analisar", type="primary"):
        if not banco_schema or not colecao_schema:
            st.warning("Por favor, preencha o banco e a coleção")
        else:
            with st.spinner("Analisando schema..."):
                resultado = analisar_schema(
                    st.session_state['status'],
                    st.session_state['client'],
                    banco_schema,
                    colecao_schema,
                    amostra=amostra
                )
                
                dados = json.loads(resultado)
                
                if dados["sucesso"]:
                    info = dados["dados"]
                    
                    st.success("✅ Análise concluída!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Total de Documentos", info["total_documentos"])
                    with col2:
                        st.metric("Documentos Analisados", info["documentos_analisados"])
                    
                    st.subheader("Campos Encontrados")
                    
                    # Criar tabela de campos
                    campos_data = []
                    for campo, info_campo in info["campos"].items():
                        campos_data.append({
                            "Campo": campo,
                            "Tipos": ", ".join(info_campo["tipos"]),
                            "Frequência": f"{info_campo['percentual']:.1f}%",
                            "Exemplo": str(info_campo["exemplo"])[:50]
                        })
                    
                    st.dataframe(campos_data, use_container_width=True)
                else:
                    st.error(f"❌ Erro: {dados['erro']['mensagem']}")

with tab4:
    st.header("📖 Guia de Uso")
    
    st.markdown("""
    ### Como Usar
    
    1. **Conectar**: Clique em "Conectar ao MongoDB" na barra lateral
    2. **Explorar**: Use a aba "Explorar" para navegar pelos bancos e coleções
    3. **Consultar**: Execute queries personalizadas na aba "Consultar"
    4. **Analisar**: Analise a estrutura dos documentos na aba "Analisar Schema"
    
    ### Tipos de Consulta
    
    - **Find**: Busca simples com filtro
    - **Aggregate**: Pipeline de agregação complexo
    - **Distinct**: Valores únicos de um campo
    - **Count**: Contagem de documentos
    - **Find One**: Retorna um único documento
    - **Find com Opções**: Busca com sort, limit, skip e projection
    
    ### ⚠️ Importante
    
    - Este sistema é **READ-ONLY** (somente leitura)
    - Não é possível inserir, atualizar ou deletar documentos
    - Ideal para análise e exploração de dados
    
    ### 🔗 Links Úteis
    
    - [Documentação MongoDB](https://docs.mongodb.com/)
    - [GitHub do Projeto](https://github.com/AdrianoCavalcante/MongoDB_interface)
    """)

# Footer
st.markdown("---")
st.markdown("🍃 **MongoDB Interface** | Desenvolvido com Streamlit | [GitHub](https://github.com/AdrianoCavalcante/MongoDB_interface)")
