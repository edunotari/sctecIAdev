# SCTEC — Empreendimentos SC

> **Desafio Técnico · Trilha Dev IA · SCTEC 2025**
> Aplicação CRUD para gerenciamento de empreendimentos em Santa Catarina.



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
