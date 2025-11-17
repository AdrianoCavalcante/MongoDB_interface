# Exemplos de Consultas MongoDB

Este documento contém exemplos práticos de consultas para o sistema MongoDB Interface, organizados por tipo de operação.

---

## Find (Busca Simples)

### Buscar todas as notícias da seção "Economia"
```json
{"fonte.secao": "Economia"}
```

### Buscar notícias publicadas pelo "G1"
```json
{"fonte.publicador": "G1"}
```

---

## Aggregate (Agregação)

### Contar o total de notícias por seção
```json
[
  {"$group": {"_id": "$fonte.secao", "total": {"$sum": 1}}},
  {"$sort": {"total": -1}}
]
```

### Listar o número de notícias por jornalista com $lookup (JOIN)
```json
[
  {"$lookup": {
      "from": "jornalistas",
      "localField": "jornalista_id",
      "foreignField": "_id",
      "as": "jornalista"
  }},
  {"$unwind": "$jornalista"},
  {"$group": {
      "_id": "$jornalista.nome",
      "total_noticias": {"$sum": 1}
  }},
  {"$sort": {"total_noticias": -1}},
  {"$project": {"_id": 0, "jornalista": "$_id", "total_noticias": 1}}
]
```

---

## Distinct (Valores Únicos)

### Listar todas as seções únicas das notícias
```json
{"_distinct": "fonte.secao"}
```

### Listar todos os publicadores únicos
```json
{"_distinct": "fonte.publicador"}
```

---

## Count (Contagem)

### Contar notícias publicadas na data de 4 de julho de 2013
```json
{"_count": true, "_query": {"fonte.data_publicacao": {"$regex": "^2013-07-04"}}}
```

### Contar notícias que mencionam "assassinato" no corpo
```json
{"_count": true, "_query": {"fonte.corpo": {"$regex": "assassinato", "$options": "i"}}}
```

---

## 📄 Find One (Buscar Um Documento)

### Buscar uma notícia da seção "Economia"
```json
{"_find_one": true, "_query": {"fonte.secao": "Economia"}}
```

### Buscar uma notícia com título específico
```json
{"_find_one": true, "_query": {"fonte.titulo": "SP registra a tarde mais quente do inverno"}}
```

---

## 🎯 Find com Opções (Busca Avançada)

### Buscar os 5 títulos mais recentes da seção "Economia"
```json
{
  "_find_with_options": true,
  "_query": {"fonte.secao": "Economia"},
  "_sort": {"fonte.data_publicacao": -1},
  "_limit": 5,
  "_projection": {"fonte.titulo": 1, "_id": 0}
}
```

### Buscar todos os títulos onde o corpo da notícia contenha "assassinato"
```json
{
  "_find_with_options": true,
  "_query": {"fonte.corpo": {"$regex": "assassinato", "$options": "i"}},
  "_projection": {"titulo": 1, "_id": 0}
}
```

---

## ✅ Pontos Positivos do MongoDB

### Vantagens para este Projeto

- **Flexibilidade no esquema de dados**: Permite armazenar documentos com estruturas variadas, facilitando a adaptação a mudanças nos requisitos.

- **Escalabilidade horizontal**: Facilita a distribuição de dados em múltiplos servidores, suportando grandes volumes de dados e alta demanda.

- **Alto desempenho em consultas**: Oferece respostas rápidas para operações de leitura e escrita, ideal para aplicações com grande volume de dados.

- **Suporte a consultas complexas**: Permite realizar operações avançadas como agregações, junções e filtragens detalhadas.

- **Comunidade ativa e ecossistema robusto**: Conta com ampla documentação, ferramentas e suporte da comunidade, facilitando o desenvolvimento e a resolução de problemas.

- **Integração com diversas linguagens de programação**: Possui drivers oficiais para várias linguagens, facilitando a integração com diferentes stacks de desenvolvimento.

- **Suporte a replicação e alta disponibilidade**: Garante a continuidade do serviço através de réplicas e failover automático.

- **Fácil de usar e aprender**: A sintaxe baseada em JSON é intuitiva para desenvolvedores familiarizados com JavaScript e outras linguagens.

- **Amplo suporte a ferramentas de análise e visualização de dados**: Integra-se bem com ferramentas populares para análise de dados, facilitando a extração de insights.

- **Índices Poderosos**: Suporta a criação de índices em campos específicos e aninhados para melhorar o desempenho das consultas.

---

## ⚠️ Pontos Negativos do MongoDB

### Limitações e Considerações

- **Consistência Eventual**: Em ambientes distribuídos, pode haver atrasos na propagação de dados entre réplicas, levando a leituras inconsistentes temporariamente.

- **Limitações em Transações Complexas**: Embora suporte transações ACID, o desempenho pode ser afetado em operações que envolvem múltiplos documentos ou coleções.

- **Consumo de Memória**: Pode exigir mais memória para armazenar índices e dados em comparação com bancos de dados relacionais tradicionais.

- **Curva de Aprendizado para Modelagem de Dados**: A modelagem eficiente de dados pode ser desafiadora para desenvolvedores acostumados com bancos de dados relacionais.

- **Ferramentas de Administração Limitadas**: Embora existam ferramentas disponíveis, elas podem não ser tão robustas quanto as oferecidas por bancos de dados relacionais estabelecidos.

- **Sobrecarga de Armazenamento**: O formato BSON pode resultar em maior uso de espaço em disco em comparação com formatos mais compactos.

- **Gerenciamento de Índices**: A criação e manutenção de índices podem ser complexas e impactar o desempenho se não forem gerenciadas adequadamente.

- **Falta de Suporte a Joins Complexos**: Embora suporte operações de junção via `$lookup`, elas podem ser menos eficientes e mais limitadas em comparação com bancos de dados relacionais.

---

## 📚 Referências

- [Documentação Oficial MongoDB](https://docs.mongodb.com/)
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- [PyMongo Driver](https://pymongo.readthedocs.io/)
