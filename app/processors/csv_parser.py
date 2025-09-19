import pandas as pd

def parse_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        return df.to_string()
    except Exception as e:
        raise ValueError(f"Ошибка при чтении CSV: {str(e)}")