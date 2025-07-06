import pandas as pd

def create_summary(df, date_from=None, date_to=None, hotels=None):
    """
    Returns aggregated stats (avg, min, max, median) grouped by hotel & competitor for the selected filter.
    """
    filtered = df.copy()
    if hotels:
        filtered = filtered[filtered['hotel'].isin(hotels)]
    if date_from is not None and date_to is not None:
        filtered = filtered[(filtered['date'] >= date_from) & (filtered['date'] <= date_to)]
    agg = (
        filtered.groupby(['hotel', 'competitor'])
        .agg(
            avg_rate=('rate', 'mean'),
            min_rate=('rate', 'min'),
            max_rate=('rate', 'max'),
            median_rate=('rate', 'median'),
            count=('rate', 'count')
        )
        .reset_index()
    )
    return agg

def add_rankings(df):
    """
    Adds a 'rank' column: for each hotel/date, 1 = lowest rate among competitors (including self).
    """
    df = df.copy()
    df['rank'] = (
        df.groupby(['hotel', 'date'])['rate']
        .rank(method='min', ascending=True)
        .astype(int)
    )
    return df

def add_price_delta(df):
    """
    Adds a 'price_delta' column: hotel rate minus cheapest competitor rate, for each hotel/date.
    For each (hotel, date), finds min competitor rate and computes delta.
    """
    df = df.copy()
    min_rate = (
        df.groupby(['hotel', 'date'])['rate']
        .transform('min')
    )
    df['price_delta'] = df['rate'] - min_rate
    return df