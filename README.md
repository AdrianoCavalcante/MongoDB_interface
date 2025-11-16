# MongoDB Interface

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyMongo](https://img.shields.io/badge/pymongo-4.0+-green.svg)](https://pymongo.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Interface simplificada e segura para consultas MongoDB Atlas usando Python. Projetada para operações **somente leitura** com arquitetura modular e separação de responsabilidades.

## 📋 Índice

- [Características](#-características)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Uso Rápido](#-uso-rápido)
- [Funções Disponíveis](#-funções-disponíveis)
- [Exemplos Avançados](#-exemplos-avançados)
- [Arquitetura](#-arquitetura)
- [Testes](#-testes)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

## ✨ Características

- ✅ **Somente Leitura**: Segurança por design - não realiza operações de escrita
- ✅ **Modular**: Separação clara entre conexão e consultas
- ✅ **Múltiplos Tipos de Query**: Find, Aggregate, Distinct, Count, Find One, Find com Opções
- ✅ **Análise de Schema**: Infere estrutura de coleções baseada em amostragem
- ✅ **Gestão de Conexão**: Reutilização de conexões para melhor performance
- ✅ **Tratamento de Erros**: Resposta JSON consistente para sucesso e erro
- ✅ **Type Hints**: Código totalmente tipado para melhor IDE support
- ✅ **Documentação Completa**: Docstrings detalhadas em todas as funções
- ✅ **Testes Abrangentes**: 25+ casos de teste cobrindo todos os cenários

## 🚀 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/MongoDB_interface.git
cd MongoDB_interface
```

### 2. Crie um ambiente virtual (opcional, mas recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## ⚙️ Configuração

### 1. Crie o arquivo de credenciais

Copie o arquivo de exemplo e adicione suas credenciais:

```bash
# Windows PowerShell
Copy-Item conexao_mongo_secrets.example.json conexao_mongo_secrets.json

# Linux/Mac
cp conexao_mongo_secrets.example.json conexao_mongo_secrets.json
```

### 2. Configure suas credenciais MongoDB Atlas

Edite `conexao_mongo_secrets.json` com suas informações:

```json
{
  "username": "seu_usuario",
  "password": "sua_senha",
  "cluster": "cluster0.xxxxx.mongodb.net"
}
```

### 3. Verifique a segurança

```bash
# IMPORTANTE: Confirme que o arquivo NÃO será commitado
git status
# conexao_mongo_secrets.json NÃO deve aparecer na lista!
```

> ⚠️ **IMPORTANTE**: 
> - Nunca faça commit do arquivo `conexao_mongo_secrets.json` (já protegido no .gitignore)
> - Veja [SECURITY.md](SECURITY.md) para guia completo de segurança de credenciais
> - Em caso de exposição acidental, troque a senha IMEDIATAMENTE no MongoDB Atlas

## 🎯 Uso Rápido

```python
import sys
sys.path.append('./src')  # Ajustar caminho se necessário

from conexao_mongodb import conectar_mongodb, desconectar_mongodb
from consulta_mongodb import consultar_mongodb
import json

# 1. Conectar
status_conexao, client, msg = conectar_mongodb()
if not status_conexao:
    print(f"Erro: {msg}")
    exit(1)

print(f"✅ {msg}")

# 2. Consultar
resultado = consultar_mongodb(
    status_conexao, 
    client, 
    "meu_banco", 
    "minha_colecao", 
    '{"status": "ativo"}'
)

dados = json.loads(resultado)
if dados["sucesso"]:
    print(f"Documentos encontrados: {len(dados['dados'])}")
else:
    print(f"Erro: {dados['erro']['mensagem']}")

# 3. Desconectar
status_conexao, msg = desconectar_mongodb(client)
print(f"✅ {msg}")
```

## 📚 Funções Disponíveis

### Módulo `conexao_mongodb`

#### `conectar_mongodb()`
Estabelece conexão com MongoDB Atlas.

**Retorna**: `(status_conexao: bool, client: MongoClient, mensagem: str)`

```python
status_conexao, client, msg = conectar_mongodb()
```

#### `desconectar_mongodb(client)`
Encerra conexão com MongoDB Atlas.

**Retorna**: `(status_conexao: bool, mensagem: str)`

```python
status_conexao, msg = desconectar_mongodb(client)
```

---

### Módulo `consulta_mongodb`

#### `consultar_mongodb(status_conexao, client, nome_banco, nome_colecao, query_json, limite_amostra=False)`

Executa consultas MongoDB em diferentes formatos.

**Parâmetros**:
- `status_conexao` (bool): Status da conexão
- `client` (MongoClient): Cliente MongoDB conectado
- `nome_banco` (str): Nome do banco de dados
- `nome_colecao` (str): Nome da coleção
- `query_json` (str): Query em formato JSON string
- `limite_amostra` (bool): Limitar a 20 documentos (padrão: False)

**Retorna**: JSON string com `{"sucesso": bool, "dados": [...]}` ou `{"sucesso": false, "erro": {...}}`

**Tipos de Query Suportados**:

##### 1. Find Simples
```python
query = '{"status": "ativo"}'
resultado = consultar_mongodb(status, client, "db", "col", query)
```

##### 2. Aggregate Pipeline
```python
query = '''[
    {"$match": {"status": "ativo"}},
    {"$group": {"_id": "$categoria", "total": {"$sum": 1}}},
    {"$sort": {"total": -1}}
]'''
resultado = consultar_mongodb(status, client, "db", "col", query)
```

##### 3. Distinct
```python
query = '{"_distinct": "categoria", "_query": {"status": "ativo"}}'
resultado = consultar_mongodb(status, client, "db", "col", query)
```

##### 4. Count
```python
query = '{"_count": true, "_query": {"status": "ativo"}}'
resultado = consultar_mongodb(status, client, "db", "col", query)
```

##### 5. Find One
```python
query = '{"_find_one": true, "_query": {"_id": "123"}, "_projection": {"nome": 1, "email": 1}}'
resultado = consultar_mongodb(status, client, "db", "col", query)
```

##### 6. Find com Opções
```python
query = '''{
    "_find_with_options": true,
    "_query": {"status": "ativo"},
    "_sort": {"data": -1},
    "_limit": 10,
    "_skip": 0,
    "_projection": {"nome": 1, "data": 1}
}'''
resultado = consultar_mongodb(status, client, "db", "col", query)
```

---

#### `listar_bancos(status_conexao, client)`

Lista todos os bancos de dados disponíveis.

**Retorna**: JSON string com `{"sucesso": true, "dados": ["banco1", "banco2", ...]}`

```python
resultado = listar_bancos(status_conexao, client)
dados = json.loads(resultado)
print(dados["dados"])  # ["admin", "local", "meu_banco", ...]
```

---

#### `listar_colecoes(status_conexao, client, nome_banco)`

Lista todas as coleções de um banco específico.

**Retorna**: JSON string com `{"sucesso": true, "dados": ["colecao1", "colecao2", ...]}`

```python
resultado = listar_colecoes(status_conexao, client, "meu_banco")
dados = json.loads(resultado)
print(dados["dados"])  # ["usuarios", "produtos", ...]
```

---

#### `analisar_schema(status_conexao, client, nome_banco, nome_colecao, amostra=100)`

Analisa a estrutura dos documentos de uma coleção (inferência baseada em amostragem).

**Parâmetros**:
- `amostra` (int): Número de documentos a analisar (padrão: 100)

**Retorna**: JSON string com análise detalhada dos campos

```python
resultado = analisar_schema(status, client, "meu_banco", "usuarios", amostra=50)
dados = json.loads(resultado)

# Estrutura do retorno:
{
  "sucesso": true,
  "dados": {
    "total_documentos": 1000,
    "documentos_analisados": 50,
    "campos": {
      "_id": {
        "tipos": ["ObjectId"],
        "frequencia": 50,
        "percentual": 100.0,
        "exemplo": "507f1f77bcf86cd799439011"
      },
      "nome": {
        "tipos": ["string"],
        "frequencia": 50,
        "percentual": 100.0,
        "exemplo": "João Silva"
      },
      "idade": {
        "tipos": ["int"],
        "frequencia": 48,
        "percentual": 96.0,
        "exemplo": 30
      }
    }
  }
}
```

## 💡 Exemplos Avançados

### Exemplo 1: Agregação Complexa com Join

```python
query = '''[
    {"$match": {"status": "publicado"}},
    {"$lookup": {
        "from": "autores",
        "localField": "autor_id",
        "foreignField": "_id",
        "as": "autor_info"
    }},
    {"$unwind": "$autor_info"},
    {"$group": {
        "_id": "$autor_info.nome",
        "total_artigos": {"$sum": 1},
        "visualizacoes": {"$sum": "$views"}
    }},
    {"$sort": {"total_artigos": -1}},
    {"$limit": 10}
]'''

resultado = consultar_mongodb(status, client, "blog", "artigos", query)
```

### Exemplo 2: Navegação Hierárquica (Bancos → Coleções)

```python
from consulta_mongodb import listar_bancos, listar_colecoes

# Listar todos os bancos
resultado_bancos = listar_bancos(status_conexao, client)
bancos = json.loads(resultado_bancos)["dados"]

# Para cada banco, listar suas coleções
for banco in bancos:
    if banco not in ["admin", "config", "local"]:  # Pular bancos de sistema
        print(f"\n📦 {banco}/")
        
        resultado_cols = listar_colecoes(status_conexao, client, banco)
        colecoes = json.loads(resultado_cols)["dados"]
        
        for col in colecoes:
            print(f"   └─ {col}")
```

### Exemplo 3: Análise de Schema com Paginação

```python
from consulta_mongodb import analisar_schema

# Analisar schema de uma grande coleção
resultado = analisar_schema(
    status_conexao, 
    client, 
    "ecommerce", 
    "produtos", 
    amostra=500  # Analisar 500 documentos
)

dados = json.loads(resultado)

# Mostrar campos mais comuns
print(f"Total de documentos: {dados['dados']['total_documentos']}")
print(f"Analisados: {dados['dados']['documentos_analisados']}\n")

print("Campos (ordenados por frequência):")
for campo, info in dados['dados']['campos'].items():
    print(f"  • {campo}: {info['percentual']:.1f}% ({', '.join(info['tipos'])})")
```

### Exemplo 4: Pipeline com Tratamento de Erros

```python
def executar_consulta_segura(query_json):
    """Wrapper com tratamento de erros completo"""
    try:
        # Conectar
        status, client, msg = conectar_mongodb()
        if not status:
            return {"erro": f"Conexão falhou: {msg}"}
        
        # Consultar
        resultado = consultar_mongodb(status, client, "db", "col", query_json)
        dados = json.loads(resultado)
        
        # Desconectar
        desconectar_mongodb(client)
        
        return dados
        
    except Exception as e:
        return {"erro": f"Exceção não tratada: {str(e)}"}

# Uso
resultado = executar_consulta_segura('{"status": "ativo"}')
if "erro" in resultado:
    print(f"❌ Erro: {resultado['erro']}")
else:
    print(f"✅ Sucesso: {len(resultado['dados'])} documentos")
```

## 🏗️ Arquitetura

### Estrutura de Diretórios

```
MongoDB_interface/
├── src/
│   ├── __init__.py                   # Pacote Python
│   ├── conexao_mongodb.py            # Gerenciamento de conexões
│   └── consulta_mongodb.py           # Operações de consulta
├── tests/
│   ├── teste_consulta_mongodb.py     # Testes de queries (15+ casos)
│   ├── teste_listar_estrutura.py     # Testes de metadados (10+ casos)
│   └── teste_analisar_schema.py      # Testes de análise de schema
├── data/
│   ├── README.md                     # Documentação dos datasets
│   ├── g1_marcha_policiais_sp.json   # Dataset de exemplo (~3000 docs)
│   └── Criacao_bases_mongo_cloud.ipynb  # Notebook de criação de bases
├── docs/
│   ├── ANALISE_CONSULTA_MONGODB.md   # Análise técnica do módulo
│   └── Artigo_MongoDB_eBay_ABNT.txt  # Artigo acadêmico
├── .gitignore
├── requirements.txt
├── conexao_mongo_secrets.example.json
├── conexao_mongo_secrets.json        # Credenciais (não commitado)
├── dados conexão do Mongo DB.txt     # Informações de conexão
├── SECURITY.md                        # Guia de segurança
├── CONTRIBUTING.md                    # Guia de contribuição
├── PROJECT_SUMMARY.md                 # Sumário executivo
├── GITHUB_SETUP.md                    # Guia de publicação
├── LICENSE
└── README.md
```

### Princípios de Design

**1. Separação de Responsabilidades (SRP)**
- `conexao_mongodb.py`: APENAS conexão/desconexão
- `consulta_mongodb.py`: APENAS operações de leitura

**Benefícios**:
- ✅ Reutilização de conexão (economia de ~400ms por query)
- ✅ Testabilidade isolada
- ✅ Manutenção simplificada

**2. Read-Only por Segurança**
- Nenhuma operação de escrita (insert, update, delete)
- Proteção contra modificações acidentais
- Ideal para ambientes de produção

**3. Estado Explícito**
- `status_conexao` boolean valida todas as operações
- Mensagens de erro descritivas
- Retorno JSON consistente

## 🧪 Testes

O projeto inclui 3 suítes de teste abrangentes:

### Executar Todos os Testes

```bash
# Teste de consultas (15+ casos)
python tests/teste_consulta_mongodb.py

# Teste de listagem (10+ casos)
python tests/teste_listar_estrutura.py

# Teste de análise de schema
python tests/teste_analisar_schema.py
```

### Cobertura de Testes

**teste_consulta_mongodb.py**:
- ✅ Conexão e desconexão
- ✅ Find (simples, com limite, resultados vazios)
- ✅ Aggregate (pipeline complexo, count simples)
- ✅ Distinct (com e sem filtro)
- ✅ Count (todos, com filtro)
- ✅ Find One (com e sem projection)
- ✅ Find com Opções (sort, skip, limit, projection)
- ✅ Cenários de erro (JSON inválido, tipo errado, banco inexistente)

**teste_listar_estrutura.py**:
- ✅ Listagem de bancos
- ✅ Listagem de coleções por banco
- ✅ Navegação hierárquica
- ✅ Bancos de sistema vs usuário
- ✅ Operações com conexão desconectada
- ✅ Consistência de múltiplas chamadas

**teste_analisar_schema.py**:
- ✅ Análise de schema com diferentes tamanhos de amostra
- ✅ Detecção de tipos MongoDB
- ✅ Campos aninhados
- ✅ Arrays e objetos complexos
- ✅ Coleções vazias

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add: nova funcionalidade incrível'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Diretrizes

- Mantenha o princípio **read-only** (não adicione operações de escrita)
- Adicione testes para novas funcionalidades
- Mantenha a consistência de retorno JSON
- Documente com docstrings detalhadas
- Use type hints

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [PyMongo](https://pymongo.readthedocs.io/) - Driver oficial MongoDB para Python
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) - Plataforma cloud MongoDB

## 📞 Suporte

- 📧 Email: seu-email@exemplo.com
- 🐛 Issues: [GitHub Issues](https://github.com/seu-usuario/MongoDB_interface/issues)
- 📖 Documentação: [Wiki do Projeto](https://github.com/seu-usuario/MongoDB_interface/wiki)

---

**Desenvolvido com ❤️ usando Python e MongoDB**
