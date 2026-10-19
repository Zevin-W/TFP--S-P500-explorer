# TFP Growth and S&P 500 Returns

## Research Question
What is the relationship between U.S. private business TFP growth and same-year S&P 500 annual total returns during 1989–2025?

## Intended Audience
Students and general readers interested in productivity and stock-market performance.


## Data

The analysis uses 37 annual observations from 1989 to 2025.

- **TFP:** BLS private business sector total factor productivity, including farm and nonfarm private business. Values are annual percentage changes.
- **Stock market:** S&P 500 Total Return Index (^SP500TR), obtained from Yahoo Finance historical data saved as a PDF and converted to CSV. Annual returns are calculated using consecutive year-end closing index values.
- **Observation unit:** One calendar year.

The processed dataset, `tfp_sp500_annual.csv`, contains:

- `Year`: Calendar year.
- `TFP_Growth_Pct`: Annual TFP growth in percent.
- `SP500_Return_Pct`: Annual S&P 500 total return in percent.

A value of 1.0 in either percentage column means 1%, not 100%.

## Run the App

Open a terminal in the project folder. With Python installed, run:

```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run app.py
```

Open the Local URL shown in the terminal to view the app.

Keep `app.py` and `tfp_sp500_annual.csv` in the same folder.


## Key Finding

For the full 1989–2025 sample (37 years), private business TFP growth
and same-year S&P 500 total returns have a weak positive Pearson
correlation (r = 0.273). The conventional two-sided test is not
statistically significant at the 5% level (p = 0.102).

## Limitations

- The sample contains only 37 annual observations.
- Private business TFP and S&P 500 companies have different coverage.
- Same-year correlation does not establish causation or predictive ability.
- TFP estimates may be revised; the 2025 estimate is preliminary.
- The conventional p-value relies on statistical assumptions.
  Dependence across years has not been formally assessed.
- Correlations for user-selected periods are exploratory and may be unstable,
  especially for small samples.


  ## Project Files

- `app.py`: Interactive Streamlit application.
- `10.15 版.ipynb`: Data preprocessing, exploratory analysis, and regression.
- `TFP.xlsx`: BLS TFP input data.
- `sp500_TR.csv`: Daily S&P 500 Total Return Index data extracted from the PDF.
- `tfp_sp500_annual.csv`: Processed annual dataset used by the app.
- `requirements.txt`: Python package dependencies.

## Reproduce the Analysis

Open `10.15 版.ipynb` in a Jupyter-compatible environment, such as
VS Code with Jupyter support.

Set the working directory to the project folder, then run all cells
from top to bottom. The notebook reads `TFP.xlsx` and `sp500_TR.csv`
and writes `tfp_sp500_annual.csv`.