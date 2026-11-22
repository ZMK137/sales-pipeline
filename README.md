# Sales Data Cleaning & Regional Revenue Pipeline

This is a Python (`pandas`) data pipeline that cleans messy sales data from `sales.csv`, calculates net revenue for each row using `add_virtual_column` (from `solution.py`), groups the total revenue by region, and saves the final summary to `revenue_by_region.csv`. It also includes unit tests written with `pytest`.

## Project Overview

Here is a quick look at what the main files do:
* `sales.csv` – raw input dataset with messy sales records.
* `solution.py` – contains the `add_virtual_column` helper function used to calculate row-level revenue.
* `pipeline.py` – runs the full pipeline: loads `sales.csv`, cleans the data (`clean_sales`), calculates regional totals (`revenue_by_region`), prints the summary table to the console, and exports `revenue_by_region.csv`.
* `test_virtual_column.py` & `test_pipeline.py` – automated `pytest` unit tests covering the virtual column logic and the pipeline steps.

*(Note: `requirements.txt` and `.gitignore` were intentionally left out of this project. Dependencies are installed directly in the environment, and generated files like `revenue_by_region.csv` stay in the project root folder.)*

## Setup & How to Run

### 1. Install Dependencies
Make sure you have Python 3 installed, then install `pandas` and `pytest`:

```bash
pip install pandas pytest
```

If your system uses `python3` explicitly, run:

```bash
python3 -m pip install pandas pytest
```

### 2. Run the Pipeline
From the project root directory, run:

```bash
python pipeline.py
```

*(or `python3 pipeline.py` depending on your setup)*

This will read `sales.csv`, clean the data, print the regional revenue summary in your terminal, and create `revenue_by_region.csv`.

### 3. Run the Tests
To run all unit tests in `test_virtual_column.py` and `test_pipeline.py`, just run:

```bash
pytest
```

## Assumptions I Made

Some parts of the task were open to interpretation, so I made the following decisions:

* **Negative quantities (`quantity < 0`):** I treated negative numbers as product returns.
* **Missing or blank discounts (`discount`):** If a discount is empty, missing, or non-numeric, I treated it as no discount (`0.0`) instead of dropping the whole order.
* **Missing unit prices (`unit_price`):** I decided that the same `product` has the same price across the dataset, so missing prices I filled with the first known non-null `unit_price` for that product.
* **Valid order IDs:** Only rows where `order_id` starts with `SO-` I consider as real sales orders. Everything else like for example TOTAL gets filtered out.
* **Duplicate order IDs:** Each order should be counted only once. After filtering for `SO-` IDs, I keep the first occurrence and drop duplicates.
* **Revenue formula, rounding, and sorting:** Row revenue is calculated via `add_virtual_column` as `quantity * unit_price - discount`. Totals are summed by region, rounded to 2 decimal places (`round(2)`), and I sorted that from highest to lowest revenue.
* **Empty dataset handling:** If no valid rows are left to aggregate in `revenue_by_region`, the script raises a `ValueError` instead of exporting an empty or broken CSV file.

## Data Issues in `sales.csv` & How I Handled Them

Because the exact number of affected rows depends on the local `sales.csv` file, you can check exact counts directly in pandas before/after each cleaning step. Below is every issue found in the dataset and how the pipeline fixes it:

| Problem in `sales.csv` | Affected Rows | How I Handled That |
| :--- | :--- | :--- |
| **Messy column headers** (extra spaces, spaces instead of underscores, mixed case) | All rows (dataset schema) | I have standardized it in `clean_sales` using `str.strip().str.replace(" ", "_").str.lower()`. |
| **Invalid `order_id` values** (not starting with `SO-`) | Any row where `order_id` does not start with `"SO-"` | I have filtered `clean_df` to keep only rows matching `order_id.astype(str).str.startswith("SO-", na=False)`. |
| **Duplicate `order_id` records** | Repeated `SO-` order rows | Dropped duplicates with `drop_duplicates(subset=["order_id"])` and reset the index using `reset_index(drop=True)`. |
| **Inconsistent `region` names** (extra spaces, mixed case like `" north "`, `"SOUTH"`) | Rows with unformatted region strings | Cleaned with `str.strip().str.title()` so regions group properly. |
| **Spaces or non-numeric values in `quantity`** | Rows with spaces inside numbers or unparseable text | I have removed spaces with `str.replace(" ", "")`, I have converted it by `pd.to_numeric(..., errors="coerce")`, and filled NaNs with `0`, and cast it to `int`. |
| **Negative `quantity` values** | Rows where `quantity < 0` | I kept them as negative integers so returns subtract from net revenue (`quantity * unit_price - discount`). |
| **Comma decimals & missing values in `unit_price`** | Rows using `,` instead of `.` or missing a price | I have replaced `,` with `.`, and converted it with `pd.to_numeric(..., errors="coerce")`, also I have built a `product` -> `unit_price` lookup from non-null rows, and filled missing prices using `.map(...)`. |
| **Missing or blank `discount` values** | Rows with empty strings or NaN discounts | I decided to treat them as no discount (0.0) with `pd.to_numeric(..., errors="coerce")` and filled missing values with `0.0`. |
