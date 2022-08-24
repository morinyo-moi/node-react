#Load the required packages
import pandas as pd
import datetime
from xgboost import XGBRegressor
from sklearn.metrics import r2_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split


raw_dataset = "./static/dataset-1.2.csv"

def ingest_rawdata(raw_data):
    
    """read the csv raw dataset and do initial preprocessing"""
    
    raw_data = pd.read_csv(raw_data)
    
    raw_data['trim'].fillna('standard', inplace=True)
    return raw_data

raw_data2 = ingest_rawdata(raw_dataset)


def preprocess_features(raw_data):
    
    """Preprocessing of the features;
    get the age from year, change all strings to lower case,
    binary-encode the features with few options, and finally create one column
    that combines all vehicle description for NLP"""
    
    #include an age column and compute age from year
    current_year = datetime.date.today().year
    raw_data['age'] = current_year - raw_data['year_man']
    
    #Encode selective features
    raw_data['usage'] = raw_data.usage.apply(str.lower).map({'locally_used': str(0), 'foreign_used': str(1)})
    raw_data['fuel_type'] = raw_data.fuel_type.apply(str.lower).map({'petrol': str(0), 'diesel': str(1), 'hybrid': str(2)})
    raw_data['transmission'] = raw_data.transmission.apply(str.lower).map({'automatic': str(0), 'manual': str(1), 'CVT': str(2)})
    
    #make the remaining text columns into lower case
    raw_data['make'] = raw_data.make.apply(str.lower)
    raw_data['model'] = raw_data.model.apply(str.lower)
    raw_data['trim'] = raw_data.trim.astype(str).apply(str.lower)
    raw_data['region'] = raw_data.region.apply(str.lower)
    raw_data['origin'] = raw_data.origin.apply(str.lower)
    raw_data['body_type'] = raw_data.body_type.apply(str.lower)
   
    #drop the year column
    clean_data = raw_data.drop('year_man', axis=1)
    
    #add a new column to combine all text columns for the vectorizer
    clean_data['descriptn'] = clean_data['make']+' '+clean_data['model']+' '+clean_data['trim']+' '+clean_data['region']+' '+clean_data['origin']+' '+clean_data['body_type']
    clean_data = clean_data.loc[:,['descriptn', 'transmission', 'usage', 'fuel_type', 'eng_capacity', 'mileage', 'age', 'selling_price']]
    clean_data.reset_index(drop=True)
    return clean_data

preprocessed_data = preprocess_features(raw_data2)


#define the features and target columns
features = preprocessed_data.drop('selling_price', axis=1)
labels = preprocessed_data.selling_price

#Split the dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(features, labels, shuffle=True, test_size=0.1, random_state=99)

#make a column transforer to scale the mileage feature using a scaler that 
#is robust to outliers. Vectorize the description column for feature extraction
col_trans = ColumnTransformer(
                            [('rob', RobustScaler(), ['mileage']), 
                            ('vectorizer', CountVectorizer(), 'descriptn')], remainder='passthrough')

#Define the xtreme gradient boosting algorithm with hyperparameters we had identified
#using gridsearch hyperparameter tuning
xgb_regressor = XGBRegressor(base_score=0.5,
                            n_estimators=77, 
                            max_depth=39,
                            min_child_weight=5, 
                            learning_rate=0.25, 
                            reg_lambda=0.3, 
                            booster='gbtree', 
                            tree_method='exact',
                            importance_type='gain', 
                            subsample=1.0,
                            colsample_bylevel=1,
                            colsample_bynode=1, 
                            colsample_bytree=1.0, 
                            gamma=0.0, 
                            reg_alpha=0, 
                            max_delta_step=0, 
                            num_parallel_tree=1, 
                            scale_pos_weight=1, 
                            validate_parameters=1, 
                            random_state=0,
                            verbosity=None)

#Define a pipeline with the column transformer and the xgboost algorithm
pipe_xgb = make_pipeline(col_trans, xgb_regressor)

# fit the pipeline with our train dataframes
pipe_xgb.fit(X_train, y_train)

#get the accuracy of the model by running an inference on the test data and get
#the coefficient of determination

pred = pipe_xgb.predict(X_test)
score_xgb = r2_score(y_test, pred)


def make_inference(new_data):
    
    
    """make inferences using the model on new data"""
    
    inference = pipe_xgb.predict(new_data)
    assert (inference > 0),"Sorry. We cannot find a valuation of a vehicle with the provided details"
    return inference


    
