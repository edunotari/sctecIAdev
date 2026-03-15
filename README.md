# SCTEC — Empreendimentos SC

> **Desafio Técnico · Trilha Dev IA · SCTEC 2025**
> Aplicação CRUD para gerenciamento de empreendimentos em Santa Catarina.

---

## Vídeo Pitch

> **Assista à apresentação completa da solução:**
>
> [![Watch the video](https://img.youtube.com/vi/T-D1KVIuvjA/maxresdefault.jpg)](https://youtu.be/t0jomEHGy0E)
> 
>[![Video Title](https://img.youtube.com/vi/VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=t0jomEHGy0E)



---

## Descrição da Solução

A aplicação **SCTEC Empreendimentos SC** é um sistema CRUD completo para cadastro, listagem, edição e remoção de empreendimentos catarinenses, desenvolvida como resposta ao desafio técnico da **Trilha Dev IA do programa SCTEC**.

### Abordagem adotada

A solução combina as duas abordagens do desafio:

- **Back-end (serviço):** API REST em Flask com persistência em SQLite, acessível via qualquer cliente HTTP (Postman, curl, integrações).
- **Front-end (interface):** Dashboard web interativo servido pela própria aplicação, com tema visual **Cyberpunk 99** inspirado no programa SCTEC e na trilha de IA — incluindo logo SCTEC em circuito, mapa de Santa Catarina, matrix rain e efeitos neon animados.

### Funcionalidades

| Operação | Descrição |
|---|---|
| **Cadastrar** | Formulário completo com 6 seções, validação de campos obrigatórios e campos condicionais por segmento |
| **Listar** | Tabela paginada com busca livre, filtros por segmento e status |
| **Editar** | Pré-preenchimento de todos os campos do registro, atualização parcial suportada |
| **Remover** | Confirmação antes da exclusão permanente |
| **Detalhar** | Modal com todas as informações organizadas por seção, incluindo campos específicos do setor |

### Campos gerenciados

**Obrigatórios (desafio):** Nome do empreendimento · Empreendedor(a) responsável · Município de SC · Segmento · E-mail/contato · Status.

**Adicionais — Identificação e Localização:** Razão Social · Nome Fantasia · CNPJ · Data de Abertura · IE · IM · Tipo de Unidade · Telefone · E-mail NFe · Responsável pelo Cadastro · Endereço Completo · Link Google Maps.

**Adicionais — Dados Fiscais, Financeiros e Societários:** Regime Tributário · CNAE · Faturamento Médio · Capital Social · Prazo de Pagamento/Recebimento · Dados Bancários · QSA (Quadro de Sócios) · Verificação de PEP · Certidões Negativas.

**Campos Específicos por Segmento (exibidos condicionalmente):**

| Segmento | Campos exclusivos |
|---|---|
| Tecnologia | Segurança da Informação / LGPD · Stack Tecnológica e Licenças |
| Comércio | Substituição Tributária (ST) · Logística |
| Indústria | Licenças Ambientais / ISO · Capacidade de Produção e Matéria-prima |
| Serviços | Registro em Conselhos de Classe · Portfólio e Seguro de RC |
| Agronegócio | Número do CAR · Registro MAPA · Capacidade de Armazenagem |

**Documentação de Apoio:** Checklist de documentos · Descrição livre.

---

## Tecnologias Utilizadas

| Tecnologia | Versão mínima | Finalidade |
|---|---|---|
| Python | 3.10 | Linguagem principal |
| Flask | 3.0 | Framework web e servidor de templates |
| Flask-SQLAlchemy | 3.1 | ORM e gerenciamento do banco de dados |
| SQLite | — | Banco de dados relacional local (arquivo `.db`) |
| Bootstrap 5 | 5.3 (CDN) | Grid, modais e componentes do dashboard |
| Bootstrap Icons | 1.11 (CDN) | Ícones da interface |
| Google Fonts | — | Orbitron, Rajdhani, Share Tech Mono (tipografia cyberpunk) |
| HTML5 Canvas | — | Matrix rain animado no fundo (vanilla JS) |

> Nenhuma dependência de frontend além do que é carregado via CDN. Sem Node.js, sem build tools.

---

## Estrutura Geral do Projeto

```
sctecIAdev/
│
├── app.py            # Fábrica da aplicação Flask, rotas raiz, migration SQLite
├── models.py         # Modelo ORM (Empreendimento) e listas de constantes
├── routes.py         # Blueprint com todos os endpoints CRUD da API REST
│
├── templates/
│   └── index.html    # Dashboard web (HTML + CSS cyberpunk + JS vanilla)
│                     # — Matrix rain canvas
│                     # — Logo SCTEC SVG circuit
│                     # — Mapa SC SVG animado
│                     # — 6 seções de formulário (campos condicionais por setor)
│                     # — Modal de detalhes expandido
│
├── requirements.txt  # Dependências Python (Flask + Flask-SQLAlchemy)
├── README.md         # Esta documentação
│
└── instance/
    └── empreendimentos.db   # Banco SQLite (criado automaticamente)
```

### Responsabilidade de cada arquivo

| Arquivo | O que faz |
|---|---|
| `app.py` | Cria o app Flask, registra o blueprint, serve o dashboard em `/`, executa `db.create_all()` e a migration automática de novas colunas para bancos existentes |
| `models.py` | Define o modelo `Empreendimento` com todas as colunas e o `to_dict()` para serialização JSON |
| `routes.py` | Implementa os 7 endpoints REST (`GET`, `POST`, `PUT`, `DELETE`, metadados) com validação, filtros e paginação |
| `templates/index.html` | Interface completa: sidebar com logo SCTEC e mapa SC, topbar com efeito glitch, cards de estatísticas, filtros, tabela paginada, modal de formulário com campos condicionais por setor, modal de detalhes e toasts de feedback |

---

## Instruções para Execução

### Pré-requisitos

- **Python 3.10+** instalado (`python --version` para verificar)
- **pip** disponível
- Conexão com a internet (apenas para carregar fontes e Bootstrap via CDN na primeira vez)

### Passo a passo

**1. Acessar o diretório do projeto**

```bash
cd sctecIAdev
```

**2. Criar e ativar o ambiente virtual**

```bash
# Linux / macOS
python -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**3. Instalar as dependências**

```bash
pip install -r requirements.txt
```

**4. Iniciar a aplicação**

```bash
python app.py
```

O banco de dados `instance/empreendimentos.db` é criado automaticamente na primeira execução. Bancos existentes são migrados automaticamente com as novas colunas sem perda de dados.

**5. Acessar o dashboard**

Abra o navegador e acesse:

```
http://localhost:5000
```

---

## Endpoints da API REST

O dashboard web consome esta API, mas ela também pode ser usada diretamente:

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/` | Dashboard web (interface gráfica) |
| `GET` | `/api` | Metadados e lista de endpoints |
| `GET` | `/api/empreendimentos` | Listar (filtros: `status`, `segmento`, `municipio`, `q`, `page`, `per_page`) |
| `GET` | `/api/empreendimentos/<id>` | Obter registro por ID |
| `POST` | `/api/empreendimentos` | Cadastrar novo empreendimento |
| `PUT` | `/api/empreendimentos/<id>` | Atualizar parcialmente |
| `DELETE` | `/api/empreendimentos/<id>` | Remover |
| `GET` | `/api/empreendimentos/meta/segmentos` | Valores aceitos para segmento |
| `GET` | `/api/empreendimentos/meta/status` | Valores aceitos para status |

### Exemplo rápido com curl

```bash
# Cadastrar
curl -X POST http://localhost:5000/api/empreendimentos \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "AgriSC Tecnologia",
    "empreendedor": "Maria da Silva",
    "municipio": "Chapecó",
    "segmento": "Agronegócio",
    "contato": "maria@agrisc.com.br",
    "cnpj": "00.000.000/0001-00",
    "regime_tributario": "Simples Nacional",
    "agro_car": "SC-4204202-XXXX",
    "status": "ativo"
  }'

# Listar ativos do segmento Tecnologia
curl "http://localhost:5000/api/empreendimentos?status=ativo&segmento=Tecnologia"
```

---

## Segmentos e Campos Condicionais

O formulário exibe automaticamente os campos específicos quando o segmento é selecionado. Os campos desaparecem ao trocar o segmento, evitando preenchimento de dados irrelevantes.

```
Segmento selecionado → Seção 04 do formulário é revelada com os campos do setor
Segmento alterado    → Seção anterior é ocultada, nova seção aparece com animação
```

---

*Desenvolvido para o desafio técnico do programa **SCTEC — Trilha Dev IA** · Santa Catarina · 2025*
