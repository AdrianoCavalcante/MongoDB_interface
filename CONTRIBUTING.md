# 🤝 Guia de Contribuição

Obrigado por considerar contribuir com o MongoDB Interface! Este documento fornece diretrizes para contribuições.

## 📜 Código de Conduta

- Seja respeitoso e inclusivo
- Aceite feedback construtivo
- Foque no que é melhor para a comunidade
- Mostre empatia com outros membros da comunidade

## 🎯 Princípios do Projeto

### ⚠️ **REGRA #1: Somente Leitura (Read-Only)**

Este projeto é **exclusivamente para operações de leitura**. 

**NÃO serão aceitas contribuições que incluam**:
- ❌ Operações de escrita (insert, update, delete, replace)
- ❌ Modificação de documentos
- ❌ Criação/exclusão de bancos ou coleções
- ❌ Operações administrativas de escrita

**Por quê?** Segurança por design. Este projeto é projetado para ambientes onde apenas leitura é permitida.

### ✅ Contribuições Bem-Vindas

- ✅ Novas operações de **leitura**
- ✅ Melhorias de performance
- ✅ Correção de bugs
- ✅ Melhorias na documentação
- ✅ Novos testes
- ✅ Análise e visualização de dados
- ✅ Validações e tratamento de erros
- ✅ Suporte a novos tipos de queries MongoDB (read-only)

## 🔄 Processo de Contribuição

### 1. Fork e Clone

```bash
# Fork o repositório no GitHub (clique em "Fork")
# Clone seu fork
git clone https://github.com/SEU_USUARIO/MongoDB_interface.git
cd MongoDB_interface

# Adicione o repositório original como upstream
git remote add upstream https://github.com/USUARIO_ORIGINAL/MongoDB_interface.git
```

### 2. Crie uma Branch

```bash
# Atualize main
git checkout main
git pull upstream main

# Crie branch para sua feature
git checkout -b feature/minha-contribuicao
```

**Convenção de nomes**:
- `feature/nome-da-feature` - Nova funcionalidade
- `fix/descricao-do-bug` - Correção de bug
- `docs/descricao` - Melhorias na documentação
- `test/descricao` - Adição/melhoria de testes

### 3. Faça Suas Alterações

**Checklist antes de commitar**:
- [ ] Código segue o estilo do projeto
- [ ] Adicionou type hints
- [ ] Adicionou docstrings (formato Google)
- [ ] Criou/atualizou testes
- [ ] Testou localmente
- [ ] Atualizou README se necessário
- [ ] Não quebrou testes existentes

### 4. Commit

```bash
# Adicione arquivos
git add .

# Commit com mensagem descritiva
git commit -m "Add: descrição clara da mudança"
```

**Convenção de commits**:
- `Add: ...` - Nova funcionalidade
- `Fix: ...` - Correção de bug
- `Update: ...` - Atualização de código existente
- `Refactor: ...` - Refatoração sem mudança de funcionalidade
- `Docs: ...` - Mudanças na documentação
- `Test: ...` - Adição/modificação de testes

### 5. Push e Pull Request

```bash
# Push para seu fork
git push origin feature/minha-contribuicao
```

No GitHub:
1. Acesse seu fork
2. Clique em "Compare & pull request"
3. Preencha o template de PR
4. Aguarde review

## 📝 Padrões de Código

### Python Style Guide

```python
# ✅ BOM - Type hints, docstring, nomes descritivos
def consultar_documentos(
    status_conexao: bool,
    client: MongoClient,
    filtro: Dict[str, Any]
) -> str:
    """
    Consulta documentos com filtro especificado.
    
    Args:
        status_conexao: Status da conexão MongoDB
        client: Cliente MongoDB conectado
        filtro: Dicionário com filtros de busca
    
    Returns:
        JSON string com resultados
    """
    if not status_conexao:
        return json.dumps({"sucesso": False, "erro": "Não conectado"})
    
    # ... implementação
```

```python
# ❌ RUIM - Sem tipos, sem docstring, nomes genéricos
def consulta(s, c, f):
    if not s:
        return {"sucesso": False}
    # ...
```

### Docstrings

Use formato **Google Style**:

```python
def funcao_exemplo(param1: str, param2: int = 10) -> Dict[str, Any]:
    """
    Descrição curta da função.
    
    Descrição mais detalhada se necessário, explicando o comportamento,
    casos especiais, etc.
    
    Args:
        param1: Descrição do primeiro parâmetro
        param2: Descrição do segundo parâmetro (padrão: 10)
    
    Returns:
        Descrição do que a função retorna
    
    Raises:
        ValueError: Quando param1 é vazio
        ConnectionError: Quando não há conexão ativa
    
    Examples:
        >>> resultado = funcao_exemplo("teste", 20)
        >>> print(resultado["dados"])
        ['item1', 'item2']
    """
```

### Retorno JSON Consistente

**SEMPRE** retorne strings JSON com este formato:

```python
# Sucesso
return json.dumps({
    "sucesso": True,
    "dados": [...]  # ou "contagem": N
}, ensure_ascii=False, indent=2, default=str)

# Erro
return json.dumps({
    "sucesso": False,
    "erro": {
        "tipo": "TipoDoErro",
        "mensagem": "Descrição clara do erro"
    }
}, ensure_ascii=False, indent=2)
```

## 🧪 Testes

### Executar Testes

```bash
# Teste de consultas
python tests/teste_consulta_mongodb.py

# Teste de listagem
python tests/teste_listar_estrutura.py

# Teste de schema
python tests/teste_analisar_schema.py
```

### Criar Novos Testes

```python
# tests/teste_nova_funcionalidade.py
import sys
sys.path.append('./src')

from conexao_mongodb import conectar_mongodb, desconectar_mongodb
from consulta_mongodb import nova_funcao

# 1. Conectar
status_conexao, client, msg = conectar_mongodb()
assert status_conexao, f"Conexão falhou: {msg}"

# 2. Testar funcionalidade
resultado = nova_funcao(status_conexao, client, "param")
dados = json.loads(resultado)
assert dados["sucesso"], f"Teste falhou: {dados.get('erro')}"

# 3. Desconectar
desconectar_mongodb(client)

print("✅ Todos os testes passaram!")
```

## 📚 Documentação

Ao adicionar novas funções:

1. **Docstring completa** na função
2. **Atualizar README.md** com exemplos
3. **Adicionar à seção de API Reference**
4. **Atualizar `__all__` no `__init__.py`**

## ❓ Dúvidas?

- 📧 Abra uma [Issue](https://github.com/USUARIO/MongoDB_interface/issues)
- 💬 Inicie uma [Discussion](https://github.com/USUARIO/MongoDB_interface/discussions)

## 🎉 Reconhecimento

Todos os contribuidores serão reconhecidos no README.md!

---

**Obrigado por contribuir! 🙏**
