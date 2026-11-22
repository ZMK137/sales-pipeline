import pandas as pd


def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    
    if not isinstance(df, pd.DataFrame) or not isinstance(role, str) or not isinstance(new_column, str):
        return pd.DataFrame([])
    
    for column in list(df.columns) + [new_column]:
        if not isinstance(column, str) or column == "":
            return pd.DataFrame([])
        for character in column:
            if not (character.isalpha() or character == "_"):
                return pd.DataFrame([])


    clean_role = role.replace("+", " + ").replace("-", " - ").replace("*", " * ")
    words = clean_role.split()

    if len(words) < 3 or len(words) % 2 == 0:
        return pd.DataFrame([])

    for i in range(len(words)):
        if i % 2 == 0:
            if words[i] not in df.columns:
                return pd.DataFrame([])
        else:
            if words[i] not in ["+", "*", "-"]:
                return pd.DataFrame([])
            
    try:
        new_df = df.copy()
        new_df[new_column] = new_df.eval(" ".join(words))
        return new_df
    except Exception:
        return pd.DataFrame([])