# Empreendimentos SC — API REST

API REST para gerenciamento de empreendimentos em Santa Catarina, desenvolvida como desafio técnico de back-end (CRUD).

---

## Descrição da solução

A aplicação expõe uma API REST que permite cadastrar, listar, editar e remover registros de empreendimentos catarinenses. Os dados são persistidos em um banco SQLite local, sem necessidade de configuração de infraestrutura externa.

A abordagem escolhida foi **desenvolvimento de serviço (back-end)**, implementada como uma **API REST** com Flask.

---

## Tecnologias utilizadas

| Tecnologia | Versão mínima | Finalidade |
|---|---|---|
| Python | 3.10 | Linguagem principal |
| Flask | 3.0 | Framework web |
| Flask-SQLAlchemy | 3.1 | ORM e persistência (SQLite) |
| SQLite | — | Banco de dados (arquivo local) |

---

## Estrutura do projeto

```
sctecIAdev/
├── app.py            # Fábrica da aplicação Flask e ponto de entrada
├── models.py         # Modelo de dados (Empreendimento) e constantes de validação
├── routes.py         # Blueprint com todos os endpoints CRUD
├── requirements.txt  # Dependências Python
├── README.md         # Esta documentação
└── instance/
    └── empreendimentos.db  # Banco SQLite (gerado automaticamente)
```

---

## Campos do empreendimento

| Campo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `nome` | string | sim | Nome do empreendimento |
| `empreendedor` | string | sim | Nome do(a) empreendedor(a) responsável |
| `municipio` | string | sim | Município de Santa Catarina |
| `segmento` | string | sim | `Tecnologia`, `Comércio`, `Indústria`, `Serviços` ou `Agronegócio` |
| `contato` | string | sim | E-mail ou outro meio de contato |
| `status` | string | não | `ativo` (padrão) ou `inativo` |
| `descricao` | string | não | Descrição livre do empreendimento |
| `data_fundacao` | string | não | Data de fundação no formato `YYYY-MM-DD` |

---

## Instruções de execução

### 1. Pré-requisitos

- Python 3.10 ou superior instalado
- `pip` disponível

### 2. Clonar / acessar o projeto

```bash
cd sctecIAdev
```

### 3. Criar e ativar ambiente virtual (recomendado)

```bash
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

### 5. Executar a aplicação

```bash
python app.py
```

A API ficará disponível em `http://localhost:5000`.

O banco de dados SQLite (`instance/empreendimentos.db`) é criado automaticamente na primeira execução.

---

## Endpoints da API

### Informações gerais

```
GET /
```

Retorna metadados da API e lista de endpoints disponíveis.

---

### Listar empreendimentos

```
GET /api/empreendimentos
```

**Parâmetros de query (opcionais):**

| Parâmetro | Descrição |
|---|---|
| `status` | Filtra por `ativo` ou `inativo` |
| `segmento` | Filtra por segmento exato |
| `municipio` | Busca parcial no município |
| `q` | Busca livre em nome, empreendedor e município |
| `page` | Número da página (padrão: 1) |
| `per_page` | Registros por página (padrão: 20, máximo: 100) |

**Exemplo:**
```
GET /api/empreendimentos?status=ativo&segmento=Tecnologia&page=1
```

**Resposta:**
```json
{
  "total": 1,
  "pagina": 1,
  "por_pagina": 20,
  "paginas": 1,
  "dados": [...]
}
```

---

### Obter empreendimento por ID

```
GET /api/empreendimentos/<id>
```

---

### Cadastrar empreendimento

```
POST /api/empreendimentos
Content-Type: application/json
```

**Corpo da requisição:**
```json
{
  "nome": "TechFloripa Soluções",
  "empreendedor": "Ana Paula Souza",
  "municipio": "Florianópolis",
  "segmento": "Tecnologia",
  "contato": "contato@techfloripa.com.br",
  "status": "ativo",
  "descricao": "Startup de software para gestão agrícola.",
  "data_fundacao": "2021-03-15"
}
```

Retorna o registro criado com status HTTP **201**.

---

### Atualizar empreendimento

```
PUT /api/empreendimentos/<id>
Content-Type: application/json
```

Todos os campos são opcionais. Apenas os campos enviados são atualizados.

**Exemplo (desativar um empreendimento):**
```json
{
  "status": "inativo"
}
```

---

### Remover empreendimento

```
DELETE /api/empreendimentos/<id>
```

**Resposta:**
```json
{
  "mensagem": "Empreendimento 'TechFloripa Soluções' removido com sucesso."
}
```

---

### Metadados (valores aceitos)

```
GET /api/empreendimentos/meta/segmentos
GET /api/empreendimentos/meta/status
```

---

## Exemplos com curl

```bash
# Listar todos
curl http://localhost:5000/api/empreendimentos

# Cadastrar
curl -X POST http://localhost:5000/api/empreendimentos \
  -H "Content-Type: application/json" \
  -d '{"nome":"Cachaça Vale do Peixe","empreendedor":"João da Silva","municipio":"Joaçaba","segmento":"Agronegócio","contato":"joao@valedopeixe.com.br"}'

# Atualizar
curl -X PUT http://localhost:5000/api/empreendimentos/1 \
  -H "Content-Type: application/json" \
  -d '{"status":"inativo"}'

# Remover
curl -X DELETE http://localhost:5000/api/empreendimentos/1

# Filtrar por segmento e busca livre
curl "http://localhost:5000/api/empreendimentos?segmento=Tecnologia&q=floripa"
```

---

## Tratamento de erros

Todas as respostas de erro seguem o padrão:

```json
{
  "erro": "Descrição do erro."
}
```

| Código HTTP | Situação |
|---|---|
| 400 | Dados inválidos ou campos obrigatórios ausentes |
| 404 | Empreendimento não encontrado |
| 405 | Método HTTP não permitido |
| 500 | Erro interno no servidor |
