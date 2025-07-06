import pandas as pd
from io import BytesIO

REQUIRED_COLS = ["hotel", "competitor", "date", "rate"]

def load_file(file_bytes, filename=None):
    """
    Loads an Excel or CSV file from bytes or path, normalizes columns, parses dates, coerces rate to float.
    Raises ValueError if required columns are missing.
    """
    # Determine file type
    if filename and filename.lower().endswith('.csv'):
        df = pd.read_csv(BytesIO(file_bytes)) if isinstance(file_bytes, bytes) else pd.read_csv(file_bytes)
    else:
        df = pd.read_excel(BytesIO(file_bytes)) if isinstance(file_bytes, bytes) else pd.read_excel(file_bytes)
    return clean_dataframe(df)

def clean_dataframe(df):
    """
    Normalizes DataFrame: lowercase column names, parses dates, coerces rates, validates required columns.
    """
    df = df.copy()
    # Normalize column names and strip spaces
    df.columns = [c.strip().lower() for c in df.columns]
    missing = [col for col in REQUIRED_COLS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}. Required: {REQUIRED_COLS}")
    # Parse dates
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    if df['date'].isnull().all():
        raise ValueError("No valid dates found in 'date' column. Please check your file format.")
    # Coerce rate
    df['rate'] = pd.to_numeric(df['rate'], errors='coerce')
    if df['rate'].isnull().all():
        raise ValueError("No valid numeric rates found in 'rate' column. Please check your file format.")
    # Drop rows with missing required fields
    df = df.dropna(subset=REQUIRED_COLS)
    # Standardize hotel/competitor as string
    df['hotel'] = df['hotel'].astype(str)
    df['competitor'] = df['competitor'].astype(str)
    return df.reset_index(drop=True)