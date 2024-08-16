"""
Replace author names in scraped datasets with artificial identifiers.
Authors are unique if they have the same name and country.
Usage: python pseudonymize.py
"""

import os
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def process_dataset(filepath: str) -> None:
    try:
        df = pd.read_csv(filepath)
        if "Author" not in df.columns or "Country" not in df.columns:
            logging.warning(f"Skipping {filepath}: missing required columns.")
            return

        df["author_id"] = pd.factorize(df["Author"] + "|" + df["Country"])[0]
        df.drop(columns=["Author"]).to_csv(filepath, index=False)
        logging.info(f"Pseudonymization of {filepath} complete.")
    except Exception as e:
        logging.error(f"Error processing {filepath}: {e!s}")


def main() -> None:
    for filename in os.listdir("data"):
        if filename.endswith("_reviews.csv"):
            process_dataset(os.path.join("data", filename))


if __name__ == "__main__":
    main()
