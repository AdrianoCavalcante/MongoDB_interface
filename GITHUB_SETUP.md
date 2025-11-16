# 🚀 Instruções para Publicar no GitHub

Este documento contém os passos para publicar o projeto MongoDB_interface no GitHub.

## 📋 Pré-requisitos

- ✅ Conta GitHub criada ([github.com](https://github.com))
- ✅ Git instalado localmente
- ✅ Repositório local inicializado (já feito!)

## 🔧 Passos para Publicar

### 1. Criar Repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login
2. Clique no botão **"+"** no canto superior direito
3. Selecione **"New repository"**
4. Configure o repositório:
   - **Repository name**: `MongoDB_interface`
   - **Description**: `Interface simplificada e segura para consultas MongoDB Atlas - Somente leitura`
   - **Visibility**: Public ou Private (sua escolha)
   - ⚠️ **NÃO marque** "Initialize this repository with a README" (já temos um!)
   - ⚠️ **NÃO adicione** .gitignore ou license (já temos!)
5. Clique em **"Create repository"**

### 2. Conectar Repositório Local ao GitHub

Após criar o repositório no GitHub, você verá instruções. Execute no PowerShell:

```powershell
# Navegue até o diretório do projeto
cd c:\Users\AdrianoCavalcante\Documents\VSC\MongoDB_interface

# Adicione o remote (substitua SEU_USUARIO pelo seu nome de usuário GitHub)
git remote add origin https://github.com/SEU_USUARIO/MongoDB_interface.git

# Renomeie a branch para 'main' (GitHub usa 'main' como padrão)
git branch -M main

# Faça o push do código
git push -u origin main
```

### 3. Verificar Upload

1. Atualize a página do seu repositório no GitHub
2. Você deverá ver todos os arquivos:
   - ✅ README.md (documentação completa)
   - ✅ src/ (código fonte)
   - ✅ tests/ (testes)
   - ✅ requirements.txt
   - ✅ .gitignore
   - ✅ LICENSE
   - ✅ conexao_mongo_secrets.example.json

### 4. Configurar Repositório (Opcional)

#### Adicionar Topics/Tags
No GitHub, clique em ⚙️ (Settings) e adicione topics:
- `python`
- `mongodb`
- `mongodb-atlas`
- `pymongo`
- `database`
- `read-only`
- `query-interface`

#### Configurar About
No canto superior direito do repositório:
- **Description**: Interface simplificada e segura para consultas MongoDB Atlas - Somente leitura
- **Website**: (se tiver)
- **Topics**: (adicione as tags acima)

#### Habilitar GitHub Pages (se quiser)
Para hospedar a documentação:
1. Settings → Pages
2. Source: Deploy from a branch
3. Branch: main, folder: /docs

## 🔄 Workflow de Desenvolvimento

### Fazer Alterações e Commit

```powershell
# Navegue até o projeto
cd c:\Users\AdrianoCavalcante\Documents\VSC\MongoDB_interface

# Verifique o status
git status

# Adicione alterações
git add .

# Commit
git commit -m "Descrição da alteração"

# Push para GitHub
git push origin main
```

### Criar Branches para Features

```powershell
# Criar nova branch
git checkout -b feature/nova-funcionalidade

# Fazer alterações e commit
git add .
git commit -m "Add: nova funcionalidade"

# Push da branch
git push origin feature/nova-funcionalidade

# No GitHub, criar Pull Request para merge na main
```

## 📊 Badges e Shields

Após publicar, você pode adicionar badges ao README.md:

```markdown
[![GitHub stars](https://img.shields.io/github/stars/SEU_USUARIO/MongoDB_interface.svg)](https://github.com/SEU_USUARIO/MongoDB_interface/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/SEU_USUARIO/MongoDB_interface.svg)](https://github.com/SEU_USUARIO/MongoDB_interface/network)
[![GitHub issues](https://img.shields.io/github/issues/SEU_USUARIO/MongoDB_interface.svg)](https://github.com/SEU_USUARIO/MongoDB_interface/issues)
[![GitHub license](https://img.shields.io/github/license/SEU_USUARIO/MongoDB_interface.svg)](https://github.com/SEU_USUARIO/MongoDB_interface/blob/main/LICENSE)
```

## 🛡️ Segurança

### ⚠️ IMPORTANTE: NUNCA commite o arquivo de credenciais!

O arquivo `conexao_mongo_secrets.json` está no `.gitignore` para **prevenir** que credenciais sejam expostas.

**Verificar antes de cada push**:
```powershell
# Ver o que será commitado
git status

# Se conexao_mongo_secrets.json aparecer, NÃO faça commit!
# Adicione ao .gitignore imediatamente
```

**Se acidentalmente committou credenciais**:
1. Mude IMEDIATAMENTE as credenciais no MongoDB Atlas
2. Remova o arquivo do histórico Git (pesquise "git remove sensitive data")
3. Force push (cuidado!)

## 📝 Checklist Final

Antes de publicar, verifique:

- ✅ README.md atualizado e completo
- ✅ Todos os testes funcionando
- ✅ requirements.txt com todas as dependências
- ✅ .gitignore protegendo arquivos sensíveis
- ✅ LICENSE incluída
- ✅ conexao_mongo_secrets.example.json como template
- ✅ Código documentado com docstrings
- ✅ Sem credenciais hardcoded no código

## 🎉 Pronto!

Seu projeto está pronto para ser publicado no GitHub!

Após o push, compartilhe o link:
```
https://github.com/SEU_USUARIO/MongoDB_interface
```

---

**Última atualização**: 16 de novembro de 2025
