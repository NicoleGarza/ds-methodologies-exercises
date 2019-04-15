from sklearn.preprocessing import LabelEncoder
import pandas as pandas
import numpy as np
import seaborn as sns

def mall_encoded(df):
    encoder = LabelEncoder()
    encoder.fit(df.gender)
    df = df.assign(gender_encoded=encoder.transform(df.gender))
    return df

def mall_outliers_annual(df):
    q1 = df.annual_income.quantile(.25)
    q3 = df.annual_income.quantile(.75)
    iqr = q3 - q1
    df['is_annual_income_outlier'] = df.annual_income > (q3 + 1.5 * iqr)
    return df

def mall_outliers_age(df):
    q1 = df.age.quantile(.25)
    q3 = df.age.quantile(.75)
    iqr = q3 - q1
    df['is_age_outlier'] = df.age > (q3 + 1.5 * iqr)
    return df

def mall_outliers_spending(df):
    q1 = df.spending_score.quantile(.25)
    q3 = df.spending_score.quantile(.75)
    iqr = q3 - q1
    df['is_spending_score_outlier'] = df.spending_score > (q3 + 1.5 * iqr)
    return df

def mall_prep(df):
    return df.pipe(mall_encoded)\
        .pipe(mall_outliers_annual)\
        .pipe(mall_outliers_age)\
        .pipe(mall_outliers_spending)
