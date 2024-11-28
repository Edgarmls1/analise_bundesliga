# Bundesliga Dashboard & Predictive Analysis

Este projeto é uma aplicação interativa para análise da Bundesliga (Campeonato Alemão de Futebol) com funcionalidades de visualização de dados e previsão de posição dos times em temporadas futuras.

## Recursos

- **Dashboard interativo**:
  - Visualize gráficos de desempenho por temporada.
  - Compare dados de gols, vitórias, empates, derrotas e outros.
  - Explore os minutos dos gols em histogramas.
  - Acompanhe a evolução das posições dos times ao longo da temporada.

- **Previsão de posições**:
  - Utiliza Regressão Linear para prever a posição de um time em uma temporada futura com base em dados históricos.

- **Integração com a API OpenLigaDB**:
  - Coleta dados das partidas de futebol das temporadas selecionadas.

---

## Estrutura do Projeto

O projeto é composto por dois arquivos principais:

1. **`componentes_bl.py`**:
   - Contém as funções para coleta, processamento e análise de dados.
   - Inclui funções para gráficos, tabelas e manipulação dos dados brutos obtidos da API OpenLigaDB.
   - Implementa o modelo de Regressão Linear para previsões.

2. **`dashboard_bl.py`**:
   - Configura o dashboard usando o framework Dash.
   - Faz o layout da interface do usuário com menus interativos e gráficos.
   - Define os callbacks para atualizar os gráficos e tabelas com base nas seleções do usuário.
   - Aplica o modelo de previsão de posições para os times selecionados.

---

## Pré-requisitos

- Python 3.8 ou superior
- Pacotes necessários (instale com `pip install *nome do pacote*`):
  - `dash`
  - `dash_bootstrap_components`
  - `plotly`
  - `pandas`
  - `scikit-learn`
  - `requests`

---

## Como Executar

1. Clone este repositório:
   ```bash
   git clone https://github.com/Edgarmls1/analise_bundesliga.git
   cd analise_bundesliga

2. Instale as dependências:
   ```bash
   pip install -q dash dash_bootstrap_components plotly pandas scikit-learn requests

3. Execute o dashboard:
   ```bash
   python dashboard_bl.py
