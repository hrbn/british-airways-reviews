# British Airways Customer Reviews Analysis

## Project Overview

This project analyzes online reviews from British Airways customers on [Skytrax](https://www.airlinequality.com) using Natural Language Processing (NLP) and topic modeling. The goal is to discover recurring themes and sentiments to inform decision-making in customer service and product development.

## Installation

To set up the project, clone the repository and install the required packages:

```bash
git clone https://github.com/hrbn/british-airways-reviews.git
cd british-airways-reviews
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Usage

### Scraping Customer Review Data

The dataset is scraped from [Skytrax](https://www.airlinequality.com/airline-reviews/british-airways/). To run the scraper:

```bash
python scraper/scrape_reviews.py
```

To pseudonymize customer names in the dataset:

```bash
python scraper/pseudonymize.py
```

### Data Analysis Notebooks

Run the following Jupyter notebooks sequentially to perform the analysis:

1. `british_airways_1_clean.ipynb`: Data cleaning and preprocessing
2. `british_airways_2_nlp.ipynb`: NLP text analysis and feature extraction
3. `british_airways_3_topic_model.ipynb`: Topic modeling using BERTopic


