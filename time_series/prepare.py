import pandas as pd

def convert_to_datetime(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.assign(sale_date=pd.to_datetime(df.sale_date))
    )

#zach's way for converting to datetime
def parse_sales_date(df):
    datetime_format = '%a, %d %b %Y %H %M %S %Z'
    df.sale_date = pd.to_datetime(df.sale_date, format = datetime_format, utc=True)
    return df

def set_date_index(df):
    df['sale_date_copy'] = df['sale_date']
    df.set_index('sale_date')
    return df

def sales_total_diff(df):
    df['diff_from_last_day'] = df.sales_total.diff()
    return df

def six_columns_dates(df):
    df['year'] = df.sale_date_copy.dt.year
    df['quarter'] = df.sale_date_copy.dt.quarter
    df['month'] = df.sale_date_copy.dt.month
    df['day_of_month'] = df.sale_date_copy.dt.day
    df['day_of_week'] = df.sale_date_copy.dt.weekday
    df['weekend_vs_weekday'] = (df.sale_date_copy.dt.weekday < 5)
    return df

def sales_total_column(df):
    df['sales_total'] = df.sale_amount * df.item_price
    df = df.rename(columns={'sale_amount': 'quantity'})
    return df

def prepare_data():
    return df.pipe(parse_sales_date)\
        .pipe(set_date_index)\
        .pipe(sales_total_diff)\
        .pipe(six_columns_dates)\
        .pipe(sales_total_column)