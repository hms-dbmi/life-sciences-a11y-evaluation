# Life Sciences Accessibility Evaluation [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hms-dbmi/life-sciences-a11y-evaluation/blob/main/notebooks/index.ipynb)

This repository contains source code for surveying the accessibility of life sciences data resources and journals and visualizing results.

## Development

Set up environments using Conda:

```sh
conda env create -f environment.yml
```

Start Jupyter with the Python kernal:

```sh
conda activate life-sciences-a11y-evaluation
jupyter lab notebooks
```

Accessibility is evaluated using [WAVE API](https://wave.webaim.org/api/). To run the evaluation, you need to put a `api.lab.key` file that contains the [API key](https://wave.webaim.org/api/details). If you are the member of [HIDIVE Lab](https://hidivelab.org/), contact either Sehi L'Yi (sehi_lyi@hms.harvard.edu) or Nils Gehlenborg to obtain the API key.

To add or remove a conda package, update the environment file. Then run

```sh
conda env update -f environment.yml
```

## Data

Webpages to data portals are selected from Database Commons (https://ngdc.cncb.ac.cn/databasecommons) which is a recommended site by Cell Press and Bioinformatics Advances. 

```
https://ngdc.cncb.ac.cn/databasecommons/database/browse?term=&q=&draw=1&columns%5B0%5D.data=0&columns%5B0%5D.name=&columns%5B0%5D.searchable=false&columns%5B0%5D.orderable=false&columns%5B0%5D.search.value=&columns%5B0%5D.search.regex=false&columns%5B1%5D.data=zindex&columns%5B1%5D.name=&columns%5B1%5D.searchable=true&columns%5B1%5D.orderable=true&columns%5B1%5D.search.value=&columns%5B1%5D.search.regex=false&columns%5B2%5D.data=citation&columns%5B2%5D.name=&columns%5B2%5D.searchable=true&columns%5B2%5D.orderable=true&columns%5B2%5D.search.value=&columns%5B2%5D.search.regex=false&columns%5B3%5D.data=shortName&columns%5B3%5D.name=&columns%5B3%5D.searchable=true&columns%5B3%5D.orderable=true&columns%5B3%5D.search.value=&columns%5B3%5D.search.regex=false&columns%5B4%5D.data=foundedYear&columns%5B4%5D.name=&columns%5B4%5D.searchable=true&columns%5B4%5D.orderable=true&columns%5B4%5D.search.value=&columns%5B4%5D.search.regex=false&order%5B0%5D.column=1&order%5B0%5D.dir=desc&order%5B1%5D.column=4&order%5B1%5D.dir=DESC&start=0&length=10000&search.value=&search.regex=false&_=1667231167872
```

## Cite

> Sehi L'Yi, Thomas C Smits, Alexander Lex, Nils Gehlenborg, Digital Accessibility of Life Sciences Data Portals and Journal Websites, OSF Preprints, [10.31219/osf.io/5v98j](https://osf.io/5v98j/)
