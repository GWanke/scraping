
# Baldor Product Scraper

Projeto de extração estruturada de dados de motores industriais a partir do site da Baldor (ABB Motors and Mechanical Inc.), utilizando API descoberta via XHR, scraping com Playwright e lógica de enriquecimento para criação de datasets padronizados por produto.

---

## Objetivo

Extrair informações técnicas, estrutura de componentes (BOM), arquivos técnicos e desenhos (assets) de produtos disponíveis na [seção de motores NEMA Baldor](https://www.baldor.com/catalog) de forma automatizada, estruturando os dados em arquivos `.json` e armazenando os arquivos `.pdf` relacionados.

---

## Componentes

- API Requests: Acesso a endpoints descobertos via XHR (não oficialmente documentados; sujeitos a proteção contra bots).
- Playwright: Navegação headless para scraping da BOM de cada produto.
- Download por requests: Realização de downloads diretos de arquivos `.pdf` com headers personalizados.
- Estruturação JSON: Transformação dos dados em uma estrutura padronizada por produto.
- Persistência de arquivos: Armazenamento organizado por produto e tipo de documento.

---

## Tecnologias Utilizadas

- Python 3.12
- Playwright (Python)
- Requests
- JSON
- Pre-commit (Black, Flake8, isort)
- Linux / WSL
- uv (gerenciador de dependências)

---

## Estrutura do Projeto

```
.
├── config/
│   └── config.json                 # Configurações reutilizáveis
├── output/
│   ├── products/                   # Um JSON por produto com as informações finais
│   ├── assets/                     # Pasta com os PDFs por tipo (DimensionSheet, etc.)
│   └── selected_products.json      # Lista com os produtos selecionados após o fetch
├── src/
│   ├── main.py                     # Pipeline principal
│   ├── fetch_data_from_api.py     # Coleta dos produtos e amostragem
│   ├── parser.py                  # Construção e enriquecimento dos JSONs
│   └── utils.py                    # Funções auxiliares para Playwright e download
└── README.md
```

---

## Funcionalidades Concluídas

- [x] Extração de produtos da API com paginação dinâmica
- [x] Amostragem aleatória dos produtos coletados
- [x] Scraping da BOM via Playwright
- [x] Download de arquivos técnicos (DimensionSheet, ConnectionDiagram, Literature)
- [x] Organização do output em estrutura `.json` por produto

---

## Como Executar

1. Clone o repositório e crie um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate
```

2. Instale o `uv` e as dependências:

```bash
uv pip install -r requirements.txt
playwright install
```

3. Para gerar o lockfile atualizado:

```bash
uv pip compile requirements.txt > requirements.lock
```

4. Edite `config/config.json` com os parâmetros desejados.

5. Execute o pipeline completo:

```bash
python src/main.py
```

---

## Requisitos

- Python >= 3.9
- Playwright instalado
- Ambiente Unix-like (Linux/WSL recomendado)

---

## Melhorias Futuras

- Cache para evitar downloads duplicados
- Testes unitários para parsing e scraping
- Expansão para outras categorias além da ID 61
- Conversão para schema final de consumo por pipelines ML

---

## Autor

Desenvolvido por Gustavo Rodrigues com foco em scraping robusto e boas práticas de engenharia de dados.

## Notas e Suposições

Durante o desenvolvimento do projeto, algumas decisões técnicas e suposições foram tomadas com base na análise do comportamento do site da Baldor:

### Suposições

- **Uso da API via XHR**: Embora não documentada oficialmente, foi identificado que a aplicação carrega os dados dos produtos e dos arquivos de desenho técnico (assets) através de chamadas XHR para endpoints sob `/api/products`. Foi considerado que essas APIs fossem públicas ou de uso tolerado, uma vez que estavam expostas na navegação do site.

- **Identificação dos tipos de arquivo via API**: Inicialmente foram inferidos os tipos de arquivos (`DimensionSheet`, `ConnectionDiagram`, `Literature`) com base nos nomes e sufixos dos links. No entanto, isso se mostrou frágil. A versão final utiliza a chave `kind` da resposta da API, que categoriza corretamente os arquivos.

- **Limitações de Playwright para downloads**: Durante os testes, foi observado que os links de download abrem novas abas que, em alguns casos, permanecem indefinidamente em `about:blank`. Isso dificultou o uso confiável do Playwright para baixar os assets diretamente, optando-se pelo uso de `requests` com headers apropriados.

- **Headers necessários para evitar bloqueio por bot**: Algumas requisições falhavam silenciosamente com `timeout` ou `SSL error`. Após análise, foi identificado que o envio de headers personalizados (em especial o `User-Agent`) era necessário para simular um navegador real.

### Notas

- **Separação de responsabilidades**: O código foi modularizado com clareza entre orquestração (`main.py`), parsing (`parser.py`), coleta de produtos (`fetch_data_from_api.py`) e funções auxiliares (`utils.py`).

- **Playwright utilizado apenas para BOM**: A única etapa que requer renderização do DOM é a extração da BOM (`Bill of Materials`), realizada via Playwright. As demais são feitas exclusivamente com `requests`.

- **Arquivos de saída organizados**:
    - `output/product_links.json`: Contém a lista completa de produtos coletados da API.
    - `output/selected_products.json`: Subconjunto amostrado para processamento.
    - `output/products/{product_id}.json`: Dicionários completos por produto contendo os dados estruturados.
    - `output/assets/{product_id}/`: Pasta contendo os arquivos `.pdf` baixados (dimension sheets, diagrams, etc.).

- **Execução com `uv`**: Foi utilizado o `uv` como gerenciador de ambiente e geração de lockfile, mantendo o projeto leve, reprodutível e rápido.
