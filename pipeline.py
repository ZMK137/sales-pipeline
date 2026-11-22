import pandas as pd
from solution import add_virtual_column

def main():
    df = pd.read_csv("sales.csv", dtype=str, keep_default_na=False)
    cleaned_df = clean_sales(df)
    region_df = revenue_by_region(cleaned_df)
    region_df.to_csv("revenue_by_region.csv", index=False)
    print(region_df)

def clean_sales(df: pd.DataFrame):
    
    clean_df = df.copy()

    # columns standardizing
    clean_df.columns = clean_df.columns.str.strip().str.replace(' ', '_').str.lower()

    # order_id cleaning 
    clean_df = clean_df[clean_df["order_id"].astype(str).str.startswith('SO-', na=False)]
    clean_df = clean_df.drop_duplicates(subset=["order_id"])
    clean_df = clean_df.reset_index(drop=True)

    # region cleaning
    clean_df["region"] = clean_df["region"].str.strip().str.title()

    # quantity cleaning
    no_space = clean_df["quantity"].str.replace(" ", "")
    clean_df["quantity"] = pd.to_numeric(no_space, errors="coerce").fillna(0).astype(int)

    # unit_price cleaning
    clean_df["unit_price"] = clean_df["unit_price"].str.replace(",", ".")
    clean_df["unit_price"] = pd.to_numeric(clean_df["unit_price"], errors="coerce")
    
    prices = (clean_df.dropna(subset=["unit_price"]).groupby("product")["unit_price"].first())
    clean_df["unit_price"] = clean_df["unit_price"].fillna(clean_df["product"].map(prices))

    # discount cleaning
    clean_df["discount"] = pd.to_numeric(clean_df["discount"], errors="coerce").fillna(0.0)


    return clean_df

def revenue_by_region(clean_df: pd.DataFrame):
    df_plus_revenue = add_virtual_column(clean_df, role="quantity * unit_price - discount", new_column="revenue")
    
    if df_plus_revenue.empty:
        raise ValueError("No data")
    
    group = (df_plus_revenue.groupby("region", as_index=False))["revenue"].sum().round(2)

    result = group.sort_values(by="revenue", ascending=False).reset_index(drop=True)
    return result

if __name__ == "__main__":
    main()