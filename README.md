# Rate Shopper MVP — Benchmark de Tarifas Hoteleiras

Esta aplicação permite que hotéis ou analistas de revenue management comparem rapidamente tarifas próprias e de concorrentes em múltiplas datas. Basta enviar uma planilha (Excel ou CSV) no formato indicado e visualizar insights, rankings e gráficos instantâneos via interface Streamlit.

## 📦 Funcionalidades

- **Upload de arquivo** (.xlsx ou .csv) com dados de tarifas.
- **Validação automática** dos campos obrigatórios: hotel, competitor, date, rate.
- **Cálculos de benchmarking**:
    - Média, mínimo, máximo, mediana por hotel e concorrente.
    - Ranking de posição (1 = mais barato) por data/hotel.
    - Delta de preço: tarifa do hotel menos a menor tarifa do dia.
- **Controles interativos**: seleção de hotéis e período de datas.
- **Visualizações**: tabela colorida, gráfico de barras (médias), gráfico de linha (tendência).
- **Download** dos resultados em Excel.
- **Aparência agradável**: tema escuro, rankings destacados.
- **Dataset de exemplo incluso** para demonstração rápida.

---

## 🚀 Como usar

1. **Clone o projeto**:
    ```bash
    git clone <repositorio-url>
    cd <pasta-do-projeto>
    ```

2. **Crie e ative um ambiente virtual**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate     # Linux/macOS
    .venv\Scripts\activate        # Windows
    ```

3. **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Execute o Streamlit**:
    ```bash
    streamlit run streamlit_app.py
    ```

5. **Acesse no navegador**:  
    Normalmente em http://localhost:8501

---

## 📊 Formato esperado dos dados

A planilha precisa conter as colunas obrigatórias:
- `hotel` (nome do hotel)
- `competitor` (nome do concorrente ou própria marca)
- `date` (data, qualquer formato reconhecido pelo Excel/pandas)
- `rate` (valor numérico da diária)

Exemplo de linhas:

| hotel    | competitor   | date       | rate  |
|----------|--------------|------------|-------|
| Hotel A  | Hotel B      | 2024-06-13 | 420.0 |
| Hotel A  | Hotel C      | 2024-06-13 | 425.0 |
| Hotel B  | Hotel A      | 2024-06-13 | 430.0 |
| Hotel C  | Hotel A      | 2024-06-13 | 410.0 |
| ...      | ...          | ...        | ...   |

Um arquivo exemplo é fornecido em `sample_data/hotel_rates_sample.xlsx`.

---

## 🖼️ Screenshot

![Exemplo de interface do Rate Shopper](docs/screenshot.png)

---

## 📝 Notas

- Se faltar alguma coluna obrigatória, o sistema mostrará uma mensagem de erro amigável.
- Rankings e deltas são calculados para cada hotel/data.
- O download exporta a tabela de resumo filtrada no Excel.

---

Desenvolvido com [Streamlit](https://streamlit.io/) & [pandas](https://pandas.pydata.org/).