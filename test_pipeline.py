import pandas as pd
import pytest
from pipeline import clean_sales, revenue_by_region


def test_clean_sales():
    
    df = pd.DataFrame({
            " OrDer ID ": ["SO-1", "SO-1", "SO-2", "NoID"],
            "Product": ["Keyboard", "Keyboard", "Keyboard", "Mouse"],
            "Region": [" north ", " north ", "souTh", "eAst"],
            "QuaNtity": ["2", "2", "-1", "1"],
            "Unit Price ": ["89,0", "89,0", "", "50.0"],
            "DiScount": ["10.0", "10.0", "", "0.0"],
        })

    
    df_expected = pd.DataFrame({
            "order_id": ["SO-1", "SO-2"],
            "product": ["Keyboard", "Keyboard"],
            "region": ["North", "South"],
            "quantity": [2, -1],
            "unit_price": [89.0, 89.0],
            "discount": [10.0, 0.0],
        })
    
    df_result = clean_sales(df)
    assert df_result.equals(df_expected), f"The function should clean sales data:\n\nResult:\n\n{df_result}\n\nExpected:\n\n{df_expected}"



def test_revenue_by_region():

    df = pd.DataFrame({
            "order_id": ["SO-1", "SO-2", "SO-3"],
            "product": ["Keyboard", "Keyboard", "Mouse"],
            "region": ["South", "East", "East"],
            "quantity": [2, -1, 3],
            "unit_price": [89.0, 89.0, 50.0],
            "discount": [10.0, 0.0, 5.5],
        })
    df_expected = pd.DataFrame({
            "region": ["South", "East"],
            "revenue": [168.0, 55.5],
        })
    df_result = revenue_by_region(df)
    assert df_result.equals(df_expected), f"The function should calculate revenue by region:\n\nResult:\n\n{df_result}\n\nExpected:\n\n{df_expected}"