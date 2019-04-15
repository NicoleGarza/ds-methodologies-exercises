# Wrangling
import pandas as pd
import numpy as np
# Exploring
import scipy.stats as stats
# Modeling
import statsmodels.api as sm
from scipy.stats import pearsonr
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, median_absolute_error

def single_unit_props(df):
    df = df[df.unitcnt == 1]
    df = df[df.bathroomcnt >= 1]
    df = df[df.bedroomcnt >= 1]
    single = ['Single Family Residential', 'Condominium']
    df = df[df.propertylandusedesc.isin(single)]
    return df

def make_non_numeric(df):
   for col in ('id', 'parcelid', 'decktypeid', 'fips', 'pooltypeid10', 'pooltypeid2', 'pooltypeid7', 'rawcensustractandblock', 'regionidcity', 'regionidcounty', 'regionidneighborhood', 'regionidzip', 'censustractandblock', 'fireplaceflag'):
       df[col] = df[col].astype(str)
   return df

def zillow_missing_values_columns(df):
    percentage_missing = df.isna().mean().round(4) * 100
    percentage_missing = pd.DataFrame(data=percentage_missing, dtype=np.float64)
    percentage_missing = percentage_missing.rename(columns={0: "percentage_missing"})
    count_missing = df.isna().sum()
    count_missing = pd.DataFrame(data=count_missing, dtype=np.float64)
    count_missing = count_missing.rename(columns={0: "count_missing"})
    missing_values = pd.concat([percentage_missing, count_missing], axis=1, sort=False)
    return missing_values

def zillow_missing_values_rows(df):
    for i in range(len(df.index)) :
        print("Nan in row ", i , " : " ,  df.iloc[i].isnull().sum())

def zillow_drop_columns(df):
    df = df.drop(['basementsqft', 'finishedfloor1squarefeet', 'finishedsquarefeet13', 'finishedsquarefeet15', 'finishedsquarefeet50',
                  'finishedsquarefeet6', 'fireplacecnt', 'garagecarcnt' ,'garagetotalsqft' ,'hashottuborspa', 'poolcnt', 'poolsizesum',
                  'threequarterbathnbr', 'yardbuildingsqft17', 'yardbuildingsqft26', 'numberofstories','taxdelinquencyflag',
                  'taxdelinquencyyear','architecturalstyledesc','buildingclassdesc','storydesc', 'typeconstructiondesc', 'id', 'parcelid','fullbathcnt','fips','finishedsquarefeet12','roomcnt','calculatedbathnbr','propertyzoningdesc','rawcensustractandblock','censustractandblock','propertycountylandusecode'], axis=1)
    df = df.replace({'nan':np.nan})
    df = df.drop(['regionidneighborhood','airconditioningdesc','fireplaceflag','decktypeid','pooltypeid2','pooltypeid10', 'pooltypeid7','Unnamed: 0'], axis=1)
    return df

def handle_missing_values(df, columns):
    for columns in df:
        fillna('0')
    return df
    
def impute_landsqft(df):
   good_land = df.loc[~df.lotsizesquarefeet.isna()]
   lm1 = LinearRegression()
   lm1.fit(good_land[['landtaxvaluedollarcnt']], good_land[['lotsizesquarefeet']])
   y_pred_lm1 = lm1.predict(df.loc[df.lotsizesquarefeet.isna(), ['landtaxvaluedollarcnt']])
   df.loc[df.lotsizesquarefeet.isna(), ['lotsizesquarefeet']] = y_pred_lm1
   return df

def zillow_drop_nas(df):
    df = df.dropna()
    return df

def prep_zillow(df):
    return df.pipe(single_unit_props)\
        .pipe(make_non_numeric)\
        .pipe(zillow_drop_columns)\
        .pipe(impute_landsqft)\
        .pipe(zillow_drop_nas)

def remove_outliers():
    keys = ['bathroomcnt','bedroomcnt','calculatedfinishedsquarefeet',
                      'structuretaxvaluedollarcnt','landtaxvaluedollarcnt']
    values = [(1,7), (1,7), (500,8000), (25000,2000000), (10000,2500000)]
    dictionary = dict(zip(keys, values))
    for key, value in dictionary.items():
        df = df[df[key] >= value[0]]
        df = df[df[key] <= value[1]]

# def pairplot_heatmap():

