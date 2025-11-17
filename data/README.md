# 📊 Dados de Exemplo

Este diretório contém datasets de exemplo usados para testes e demonstrações do MongoDB Interface.

## 📁 Arquivos Disponíveis

### `g1_marcha_policiais_sp.json`

**Descrição**: Dataset com notícias do portal G1 sobre a marcha de policiais em São Paulo.

### `Exemplos_de_consultas.md`

**Descrição**: Guia completo com exemplos de consultas MongoDB organizados por tipo de operação.

**Conteúdo**:
- 📋 Exemplos de **Find** (busca simples)
- 📊 Exemplos de **Aggregate** (agregação e $lookup)
- 🔍 Exemplos de **Distinct** (valores únicos)
- 🔢 Exemplos de **Count** (contagem)
- 📄 Exemplos de **Find One** (buscar um documento)
- 🎯 Exemplos de **Find com Opções** (busca avançada)
- ✅ Análise de **Pontos Positivos** do MongoDB
- ⚠️ Análise de **Pontos Negativos** do MongoDB

**Uso**: Consulte este arquivo para exemplos práticos de queries baseadas nos schemas reais das coleções `jornalistas` e `noticias_g1`.

---

### `g1_marcha_policiais_sp.json`

**Estrutura**:
- **Formato**: JSON (Array de objetos)
- **Quantidade**: ~3000 documentos
- **Origem**: Portal G1 de Notícias

**Campos principais**:
- Título da notícia
- Texto completo
- Data de publicação
- URL da matéria
- Autor/jornalista
- Categoria
- Tags/palavras-chave

**Uso**:
Este dataset pode ser importado para o MongoDB para testes das funcionalidades do projeto:

```python
import json
import sys
sys.path.append('./src')

from conexao_mongodb import conectar_mongodb, desconectar_mongodb

# Carregar dados
with open('data/g1_marcha_policiais_sp.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

print(f"Total de notícias: {len(dados)}")

# Conectar ao MongoDB (apenas para consultas)
status, client, msg = conectar_mongodb()
if status:
    # Use as funções de consulta para explorar os dados
    # (Lembre-se: este projeto é READ-ONLY)
    print("Conectado! Use as funções de consulta para explorar os dados.")
    desconectar_mongodb(client)
```

**Importação para MongoDB** (via MongoDB Compass ou mongoimport):

```bash
# Usando mongoimport (linha de comando)
mongoimport --uri "mongodb+srv://usuario:senha@cluster.mongodb.net/banco" \
  --collection noticias_g1 \
  --file data/g1_marcha_policiais_sp.json \
  --jsonArray
```

## 🔍 Exemplos de Consultas

Após importar os dados, você pode testá-los com as funções do projeto:

### 1. Listar todas as notícias
```python
from consulta_mongodb import consultar_mongodb

resultado = consultar_mongodb(
    status_conexao, 
    client, 
    "seu_banco", 
    "noticias_g1", 
    '{}'  # Query vazia = todos os documentos
)
```

### 2. Buscar notícias por palavra-chave
```python
query = '{"titulo": {"$regex": "policial", "$options": "i"}}'
resultado = consultar_mongodb(status, client, "banco", "noticias_g1", query)
```

### 3. Agregação: Contar notícias por categoria
```python
query = '''[
    {"$group": {"_id": "$categoria", "total": {"$sum": 1}}},
    {"$sort": {"total": -1}}
]'''
resultado = consultar_mongodb(status, client, "banco", "noticias_g1", query)
```

### 4. Analisar schema do dataset
```python
from consulta_mongodb import analisar_schema

schema = analisar_schema(status, client, "banco", "noticias_g1", amostra=100)
print(schema)
```

## 📝 Notas

- **Licença**: Dados públicos do portal G1
- **Finalidade**: Exclusivamente para testes e demonstrações educacionais
- **Atualização**: Dataset estático (snapshot histórico)
- **Tamanho**: ~50 MB (formato JSON)

## ⚠️ Importante

Este projeto é **READ-ONLY**. Os dados servem apenas para:
- ✅ Testes de consultas
- ✅ Demonstrações de funcionalidades
- ✅ Aprendizado de MongoDB
- ❌ NÃO para modificação via este projeto (use MongoDB Compass ou mongo shell para isso)

---

**Para adicionar novos datasets**, simplesmente coloque arquivos JSON nesta pasta e documente-os neste README.
