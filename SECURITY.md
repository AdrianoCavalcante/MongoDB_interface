# 🔐 Guia de Segurança - Gerenciamento de Credenciais

## ⚠️ IMPORTANTE: Nunca Commite Credenciais!

O arquivo `conexao_mongo_secrets.json` contém informações sensíveis e **NUNCA** deve ser commitado no Git ou compartilhado publicamente.

## 🛡️ Como Está Protegido

### 1. `.gitignore` Configurado

O arquivo `.gitignore` já inclui:

```gitignore
# Arquivo de credenciais MongoDB (NUNCA COMMITAR!)
conexao_mongo_secrets.json
```

**Verificar proteção**:
```bash
git status
# conexao_mongo_secrets.json NÃO deve aparecer na lista
```

### 2. Template de Exemplo Fornecido

O arquivo `conexao_mongo_secrets.example.json` serve como template:

```json
{
  "username": "seu_usuario_mongodb_atlas",
  "password": "sua_senha_mongodb_atlas",
  "cluster": "cluster0.xxxxx.mongodb.net"
}
```

**Não contém dados reais** - apenas orienta novos desenvolvedores.

## 📋 Setup para Novos Desenvolvedores

### Passo 1: Copiar Template

```bash
# Windows PowerShell
Copy-Item conexao_mongo_secrets.example.json conexao_mongo_secrets.json

# Linux/Mac
cp conexao_mongo_secrets.example.json conexao_mongo_secrets.json
```

### Passo 2: Editar com Credenciais Reais

Abra `conexao_mongo_secrets.json` e substitua pelos dados reais:

```json
{
  "username": "python_script",
  "password": "30K0yZrCa40k1fnP",
  "cluster": "cluster0.hddbms5.mongodb.net",
  "database": "testeAdrianodatabase"
}
```

### Passo 3: Verificar que Não Será Commitado

```bash
git status
# conexao_mongo_secrets.json NÃO deve aparecer!
```

## 🔒 Métodos de Gerenciamento Seguro

### ✅ Opção 1: Arquivo Local (ATUAL - Recomendado para Dev)

**Prós**:
- ✅ Simples de usar
- ✅ Protegido por `.gitignore`
- ✅ Cada desenvolvedor tem suas próprias credenciais

**Contras**:
- ⚠️ Arquivo pode ser compartilhado acidentalmente
- ⚠️ Não funciona bem em ambientes containerizados

**Quando usar**: Desenvolvimento local

---

### ✅ Opção 2: Variáveis de Ambiente (Recomendado para Produção)

Modificar `conexao_mongodb.py` para suportar variáveis de ambiente:

```python
import os
import json
from typing import Tuple, Optional
from pymongo import MongoClient, errors

def conectar_mongodb() -> Tuple[bool, Optional[MongoClient], str]:
    """Conecta usando variáveis de ambiente OU arquivo JSON"""
    try:
        # Tentar variáveis de ambiente primeiro
        username = os.getenv("MONGODB_USERNAME")
        password = os.getenv("MONGODB_PASSWORD")
        cluster = os.getenv("MONGODB_CLUSTER")
        
        if username and password and cluster:
            # Usar variáveis de ambiente
            credenciais = {
                "username": username,
                "password": password,
                "cluster": cluster
            }
        else:
            # Fallback para arquivo JSON
            with open("conexao_mongo_secrets.json", 'r', encoding='utf-8') as f:
                credenciais = json.load(f)
        
        # ... resto do código
```

**Configurar variáveis de ambiente**:

```bash
# Windows PowerShell
$env:MONGODB_USERNAME="python_script"
$env:MONGODB_PASSWORD="30K0yZrCa40k1fnP"
$env:MONGODB_CLUSTER="cluster0.hddbms5.mongodb.net"

# Linux/Mac
export MONGODB_USERNAME="python_script"
export MONGODB_PASSWORD="30K0yZrCa40k1fnP"
export MONGODB_CLUSTER="cluster0.hddbms5.mongodb.net"
```

**Prós**:
- ✅ Mais seguro em produção
- ✅ Funciona bem em containers/Docker
- ✅ Suportado por plataformas cloud (Heroku, AWS, Azure)

**Contras**:
- ⚠️ Requer configuração extra
- ⚠️ Variáveis podem expirar na sessão do terminal

**Quando usar**: Produção, CI/CD, containers

---

### ✅ Opção 3: AWS Secrets Manager / Azure Key Vault (Enterprise)

Para ambientes corporativos:

```python
# Exemplo com AWS Secrets Manager
import boto3
import json

def get_mongodb_credentials():
    secret_name = "mongodb_credentials"
    region_name = "us-east-1"
    
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])
```

**Prós**:
- ✅ Máxima segurança
- ✅ Auditoria completa
- ✅ Rotação automática de credenciais
- ✅ Controle de acesso granular

**Contras**:
- ⚠️ Custo adicional
- ⚠️ Complexidade de setup
- ⚠️ Requer infraestrutura cloud

**Quando usar**: Produção enterprise, aplicações críticas

---

### ✅ Opção 4: python-dotenv (Meio Termo)

Usar arquivo `.env` com biblioteca `python-dotenv`:

**1. Instalar**:
```bash
pip install python-dotenv
```

**2. Criar arquivo `.env`** (também no .gitignore):
```env
MONGODB_USERNAME=python_script
MONGODB_PASSWORD=30K0yZrCa40k1fnP
MONGODB_CLUSTER=cluster0.hddbms5.mongodb.net
```

**3. Modificar código**:
```python
from dotenv import load_dotenv
import os

def conectar_mongodb():
    load_dotenv()  # Carrega .env
    
    credenciais = {
        "username": os.getenv("MONGODB_USERNAME"),
        "password": os.getenv("MONGODB_PASSWORD"),
        "cluster": os.getenv("MONGODB_CLUSTER")
    }
    # ... resto do código
```

**Prós**:
- ✅ Mais limpo que variáveis de ambiente manuais
- ✅ Fácil de usar
- ✅ Padrão em muitos projetos Python

**Contras**:
- ⚠️ Dependência adicional
- ⚠️ Ainda é um arquivo local

**Quando usar**: Desenvolvimento e produção (boa opção intermediária)

---

## 🚨 O Que NUNCA Fazer

### ❌ 1. Commitar Credenciais no Git

```bash
# NUNCA faça isso!
git add conexao_mongo_secrets.json
git commit -m "Add credentials"  # ❌❌❌
```

**Se acontecer acidentalmente**:
```bash
# Remover do histórico (antes de fazer push)
git reset HEAD~1
git checkout conexao_mongo_secrets.json

# Se já fez push - TROCAR SENHA IMEDIATAMENTE!
# Depois limpar histórico com git-filter-branch ou BFG Repo-Cleaner
```

### ❌ 2. Hardcoded no Código

```python
# NUNCA faça isso!
username = "python_script"  # ❌
password = "30K0yZrCa40k1fnP"  # ❌❌❌
```

### ❌ 3. Compartilhar por Email/Chat

```
❌ "Oi, a senha é: 30K0yZrCa40k1fnP"
✅ "Vou te passar as credenciais pessoalmente"
✅ Use um gerenciador de senhas seguro (1Password, LastPass)
```

### ❌ 4. Deixar em Repositórios Públicos

- ❌ GitHub público com credenciais
- ❌ Gist público
- ❌ Pastebin/CodePen

## ✅ Checklist de Segurança

Antes de fazer push para o GitHub:

- [ ] ✅ `.gitignore` contém `conexao_mongo_secrets.json`
- [ ] ✅ `git status` NÃO mostra arquivo de credenciais
- [ ] ✅ Template `.example.json` NÃO contém dados reais
- [ ] ✅ README.md explica como configurar credenciais
- [ ] ✅ Credenciais reais estão APENAS no arquivo local
- [ ] ✅ Nenhum hardcoded de senhas no código

## 🔍 Verificar Vazamentos

### Ferramenta: git-secrets

```bash
# Instalar git-secrets
# Windows (com Git Bash)
git clone https://github.com/awslabs/git-secrets
cd git-secrets
./install.sh

# Configurar para detectar credenciais
git secrets --install
git secrets --register-aws
```

### Ferramenta: truffleHog

```bash
pip install truffleHog

# Escanear histórico Git
truffleHog --regex --entropy=False https://github.com/SEU_USUARIO/MongoDB_interface
```

## 📚 Documentação para o Time

### README.md - Seção de Setup

Adicione ao README.md:

```markdown
## ⚙️ Configuração de Credenciais

**IMPORTANTE**: Nunca commite o arquivo `conexao_mongo_secrets.json`!

1. Copie o template:
   ```bash
   cp conexao_mongo_secrets.example.json conexao_mongo_secrets.json
   ```

2. Edite `conexao_mongo_secrets.json` com suas credenciais MongoDB Atlas

3. Verifique que não será commitado:
   ```bash
   git status  # conexao_mongo_secrets.json NÃO deve aparecer
   ```
```

## 🎯 Recomendação Final

### Para Este Projeto (MongoDB_interface):

**✅ MANTER como está** - Arquivo local protegido por `.gitignore`

**Razões**:
1. ✅ Projeto já configurado corretamente
2. ✅ `.gitignore` protege o arquivo
3. ✅ Template `.example.json` orienta desenvolvedores
4. ✅ Simples para desenvolvimento local
5. ✅ Fácil de entender para iniciantes

**⚡ Melhorias futuras** (opcional):
- Adicionar suporte a variáveis de ambiente (fallback)
- Documentar opções de produção no README
- Adicionar validação de credenciais no código

---

## 📞 Em Caso de Vazamento

**Se credenciais foram expostas publicamente**:

1. **🚨 IMEDIATO**: Trocar senha no MongoDB Atlas
2. **🔒 Revogar** acesso do usuário comprometido
3. **🔍 Auditar** logs de acesso
4. **🧹 Limpar** histórico Git (se necessário)
5. **📝 Documentar** incidente
6. **🔄 Revisar** processos de segurança

**MongoDB Atlas**:
- Acesse: https://cloud.mongodb.com
- Database Access → Editar usuário → Trocar senha
- Network Access → Revisar IPs permitidos

---

**🔐 Segurança é responsabilidade de todos!**

*Última atualização: 16 de novembro de 2025*
