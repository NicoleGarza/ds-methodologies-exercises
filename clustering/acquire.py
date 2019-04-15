
import pandas as pd
import env

def get_connection(db, user=env.username, host=env.hostname, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def get_titanic_data():
    return pd.read_sql('SELECT * FROM passengers', get_connection('titanic_db'))

def get_iris_data():
   return pd.read_sql('SELECT s.species_name, m.* FROM species s JOIN measurements m ON m.species_id = s.species_id', get_connection('iris_db'))


def get_telco_data():
    return pd.read_sql('SELECT * FROM customers', get_connection('telco_churn'))


def get_2016_zillow():
    df = pd.read_sql('\
    SELECT p16.*, pred16.logerror, pred16.transactiondate, act.airconditioningdesc, ast.architecturalstyledesc, bct.buildingclassdesc, hst.heatingorsystemdesc, plut.propertylandusedesc, st.storydesc, tct.typeconstructiondesc FROM properties_2016 p16\
    JOIN predictions_2016 pred16 ON pred16.parcelid = p16.parcelid\
    LEFT JOIN airconditioningtype act ON p16.airconditioningtypeid = act.airconditioningtypeid\
    LEFT JOIN architecturalstyletype ast ON p16.architecturalstyletypeid = ast.architecturalstyletypeid\
    LEFT JOIN buildingclasstype bct ON p16.buildingclasstypeid = bct.buildingclasstypeid\
    LEFT JOIN heatingorsystemtype hst ON p16.heatingorsystemtypeid = hst.heatingorsystemtypeid\
    LEFT JOIN propertylandusetype plut ON p16.propertylandusetypeid = plut.propertylandusetypeid\
    LEFT JOIN storytype st ON p16.storytypeid = st.storytypeid\
    LEFT JOIN typeconstructiontype tct ON p16.typeconstructiontypeid = tct.typeconstructiontypeid',\
    get_connection('zillow'))
    df = df.drop(columns=['airconditioningtypeid', 'architecturalstyletypeid','buildingclasstypeid', 'heatingorsystemtypeid', 'propertylandusetypeid', 'storytypeid', 'typeconstructiontypeid'],index=1)
    df.to_csv(r'/Users/nicolegarza/ds-methodologies-exercises/clustering/zillow_data_2016.csv')
    return df

def get_2017_zillow():
    df = pd.read_sql('\
    SELECT p17.*, pred17.logerror, pred17.transactiondate, act.airconditioningdesc, ast.architecturalstyledesc, bct.buildingclassdesc, hst.heatingorsystemdesc, plut.propertylandusedesc, st.storydesc, tct.typeconstructiondesc FROM properties_2017 p17\
    JOIN predictions_2017 pred17 ON pred17.parcelid = p17.parcelid\
    LEFT JOIN airconditioningtype act ON p17.airconditioningtypeid = act.airconditioningtypeid\
    LEFT JOIN architecturalstyletype ast ON p17.architecturalstyletypeid = ast.architecturalstyletypeid\
    LEFT JOIN buildingclasstype bct ON p17.buildingclasstypeid = bct.buildingclasstypeid\
    LEFT JOIN heatingorsystemtype hst ON p17.heatingorsystemtypeid = hst.heatingorsystemtypeid\
    LEFT JOIN propertylandusetype plut ON p17.propertylandusetypeid = plut.propertylandusetypeid\
    LEFT JOIN storytype st ON p17.storytypeid = st.storytypeid\
    LEFT JOIN typeconstructiontype tct ON p17.typeconstructiontypeid = tct.typeconstructiontypeid',\
    get_connection('zillow'))
    df = df.drop(columns=['airconditioningtypeid', 'architecturalstyletypeid','buildingclasstypeid', 'heatingorsystemtypeid', 'propertylandusetypeid', 'storytypeid', 'typeconstructiontypeid'],index=1)
    df.to_csv(r'/Users/nicolegarza/ds-methodologies-exercises/clustering/zillow_data_2017.csv')
    return df

def merge_zillow():
    df1 = get_2016_zillow()
    df2 = get_2017_zillow()
    frames = [df1, df2]
    df = pd.concat(frames)
    df = df.dropna(subset=['latitude', 'longitude'])
    df.to_csv(r'/Users/nicolegarza/ds-methodologies-exercises/clustering/zillow_data.csv')
    return df


def get_mall_data():
       return pd.read_sql('SELECT * FROM customers', get_connection('mall_customers'))