# Baldor Product Scraper

Projeto de extração estruturada de dados de motores industriais do site da Baldor (ABB Motors and Mechanical Inc.). A coleta é realizada a partir de uma API descoberta via inspeção de rede (XHR), combinada com scraping via Playwright para dados não disponíveis diretamente na API. O pipeline inclui enriquecimento dos dados e estruturação em arquivos JSON com os respectivos documentos técnicos em PDF.

---

## Objetivo

Automatizar a coleta de dados técnicos, estrutura de componentes (BOM) e arquivos técnicos (DimensionSheet, ConnectionDiagram, Literature) de produtos da linha de motores NEMA Baldor, estruturando as informações por produto para facilitar seu uso posterior em pipelines de Machine Learning ou sistemas de gestão de ativos industriais.

---

## Principais Componentes

- **API Requests**: Acesso aos endpoints identificados via XHR. Embora públicos, os endpoints não são documentados oficialmente e apresentam medidas de proteção contra bots.
- **Playwright**: Utilizado para renderizar e extrair a tabela de componentes (BOM) da aba "Parts".
- **Requests**: Usado com headers personalizados para download direto dos arquivos PDF.
- **Transformação de Dados**: Os dados extraídos são estruturados em um JSON padronizado contendo especificações técnicas, BOM e caminhos para arquivos associados.
- **Organização de Output**: Os arquivos e dados são salvos em diretórios separados por produto.

---

## Tecnologias Utilizadas

- Python 3.12
- Playwright (Python)
- Requests
- JSON
- Pre-commit hooks (Black, Flake8, isort)
- Sistema operacional Unix-like (Linux/WSL recomendado)

---

## Estrutura do Projeto

```
.
├── config/
│   └── config.json                   # Parâmetros customizáveis da coleta
├── output/
│   └── products/                     # JSONs por produto e arquivos PDF baixados
├── src/
│   ├── main.py                       # Orquestra o processo de coleta e enriquecimento
│   ├── fetch_data_from_api.py       # Busca produtos da API e realiza a amostragem
│   ├── parser.py                     # Parsing do JSON, scraping da BOM, download dos assets
│   └── utils.py                      # Funções auxiliares (headers, Playwright, etc.)
├── requirements.txt                 # Lista de dependências diretas
├── requirements.lock                # Snapshot travado com versões exatas
└── README.md
```

---

## Funcionalidades

- Coleta paginada de produtos da API
- Seleção aleatória de produtos com base em amostragem
- Extração da BOM via Playwright na aba "Parts"
- Download dos arquivos técnicos diretamente via API
- Estruturação final do output em JSON padronizado

---

## Como Executar

1. Clone o repositório e crie um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Instale o [uv](https://github.com/astral-sh/uv) (recomendado para ambientes rápidos e reprodutíveis):

```bash
pip install uv
```

3. Instale as dependências usando o lockfile:

```bash
uv pip sync requirements.lock
```

4. Instale os navegadores do Playwright:

```bash
playwright install
```

5. Ajuste o `config/config.json` conforme necessário (ex: número de amostras, categoria, etc.).

6. Execute o pipeline completo:

```bash
python src/main.py
```

---

## Requisitos

- Python 3.9 ou superior
- Navegadores instalados via Playwright
- Ambiente Unix-like (Linux/WSL recomendado para melhor compatibilidade)

---

## Melhorias Futuras

- Implementação de cache local para evitar downloads repetidos
- Criação de testes automatizados para validação da estrutura extraída
- Suporte a múltiplas categorias além da `61`
- Geração de schema compatível com pipelines de Machine Learning

---

## Autor

Desenvolvido por Gustavo Rodrigues como prova técnica com foco em scraping avançado, organização de código, boas práticas de engenharia de dados e reprodutibilidade.

---
