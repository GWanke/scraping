
# 🛠️ Baldor Product Scraper

Projeto de extração estruturada de dados de motores industriais a partir do site da Baldor (ABB Motors and Mechanical Inc.), utilizando API descoberta via XHR, scraping com Playwright e lógica de enriquecimento para criação de datasets padronizados por produto.

---

## 📌 Objetivo

Extrair informações técnicas, estrutura de componentes (BOM), arquivos técnicos e desenhos (assets) de produtos disponíveis na [seção de motores NEMA Baldor](https://www.baldor.com/catalog) de forma automatizada, estruturando os dados em arquivos `.json` e armazenando os arquivos `.pdf` relacionados.

---

## 🧩 Componentes

- **API Requests**: Acesso a endpoints descobertos via XHR (não oficialmente documentados; sujeitos a proteção contra bots).
- **Playwright**: Navegação headless para scraping da BOM de cada produto.
- **Download por requests**: Realização de downloads diretos de arquivos `.pdf` com headers personalizados.
- **Estruturação JSON**: Transformação dos dados em uma estrutura padronizada por produto.
- **Persistência de arquivos**: Armazenamento organizado por produto e tipo de documento.

---

## ⚙️ Tecnologias Utilizadas

- Python 3.12
- [Playwright (Python)](https://playwright.dev/python/)
- Requests
- JSON
- Pre-commit (Black, Flake8, isort)
- Linux / WSL

---

## 📁 Estrutura do Projeto

```
.
├── config/
│   └── config.json                    # Configurações reutilizáveis (headers, timeouts, paths)
├── output/
│   └── ...                           # Dados e arquivos gerados
├── src/
│   ├── main.py                       # Orquestra toda a extração
│   ├── fetch_data_from_api.py       # Busca e salva amostra de produtos da API
│   ├── parser.py                    # Parsing do JSON + scraping da BOM + download dos assets
│   └── utils.py                      # Funções auxiliares (Playwright, download, headers)
└── README.md
```

---

## ✅ Funcionalidades Concluídas

- [x] Extração de produtos da API com paginação dinâmica
- [x] Amostragem aleatória dos produtos coletados
- [x] Scraping da BOM via Playwright
- [x] Download de arquivos técnicos (DimensionSheet, ConnectionDiagram, Literature)
- [x] Organização do output em estrutura `.json` por produto

---


## ⚙️ Como Executar

1. Clone o repositório e crie um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
playwright install
```

3. Edite os parâmetros desejados no arquivo `config/config.json`.

4. Execute a coleta e o processamento:

```bash
python src/main.py
```

---

## 📦 Requisitos

- Python >= 3.9
- Playwright (instalado e configurado)
- Ambiente Unix-like (Linux/WSL recomendado)

---

## ✨ Melhorias Futuras

- [ ] Cache local para evitar downloads redundantes
- [ ] Testes unitários para scraping, parsing e validação
- [ ] Expansão para múltiplas categorias além da `61`
- [ ] Conversão dos arquivos gerados para schema final de consumo em pipelines ML

---

## 🙌 Créditos

Projeto desenvolvido por Gustavo Rodrigues com foco em scraping avançado, boas práticas de engenharia de dados e organização de pipelines reutilizáveis.

---
