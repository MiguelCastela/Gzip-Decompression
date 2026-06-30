# Information Theory: Entropy, Mutual Information and Huffman Coding

A university coursework project applying information-theoretic measures to a
car dataset. The goal is to characterise each vehicle variable, measure how
much information it shares with fuel economy (MPG), and use that to reason
about a simple MPG predictor.

The analysis covers:

- Exploratory plots of each variable against MPG.
- Per-symbol occurrence counting and histograms.
- Binning of high-cardinality variables into coarser alphabets.
- Shannon entropy of each variable and of the full dataset.
- Average Huffman code length and its variance per variable.
- Pearson correlation between each variable and MPG.
- Mutual information between each variable and MPG.
- A linear MPG predictor, evaluated with mean absolute error when the most
  and least informative variables are removed.

## Repository structure

```
.
├── README.md                 This file
├── requirements.txt          Python dependencies
├── .gitignore
├── src/
│   └── information_metrics.py Main analysis script
├── data/
│   ├── README.md             Dataset description and layout
│   └── CarDataset.xlsx       Dataset (provided separately, not committed)
└── docs/
    └── Relatorio_TP1_Miguel_Castela.pdf   Written report
```

## Requirements

- Python 3.8 or newer
- The packages in `requirements.txt` (pandas, numpy, matplotlib, openpyxl)
- `huffmancodec.py`, the course-provided Huffman module. It is not on PyPI;
  place it in `src/` next to `information_metrics.py` or anywhere on your
  `PYTHONPATH`.

Install the published dependencies with:

```
pip install -r requirements.txt
```

## Dataset

The script reads `data/CarDataset.xlsx`. This file is not redistributed in the
repository; add it yourself before running. See `data/README.md` for the
expected columns and their order.

## Running

From the repository root:

```
python src/information_metrics.py
```

The dataset path is resolved relative to the script, so the command works from
any working directory as long as `data/CarDataset.xlsx` is present.

Running the script opens several matplotlib windows in sequence (each must be
closed to continue) and prints, for every variable, its entropy after binning,
the average Huffman code length and variance, the Pearson correlation with MPG,
and the mutual information with MPG. It finishes by reporting the predictor
error with all variables, without the most informative variable, and without
the least informative variable.

## How it works

The script is organised around small functions, each mapping to a step of the
assignment:

- `compareMPG` plots each variable against MPG.
- `ocorrencias` and `ocorrenciasPlot` count and chart symbol occurrences.
- `binning` groups neighbouring values into a smaller alphabet.
- `entropy` computes Shannon entropy from the empirical distribution.
- `entropyHuff` and `varianceHuff` derive the mean and variance of Huffman
  code lengths.
- `pearson` and `infoMut` measure linear correlation and mutual information
  with MPG.
- `predictMPG` and `MAE` apply the linear MPG model and score its error.

## Notes

Source comments and printed output are in Portuguese, matching the original
coursework. The accompanying report in `docs/` explains the results in detail.
