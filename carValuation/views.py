from errno import ESTALE
import imp
from tkinter import ON
from django.http import  HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
import flask;
import boto3;
from flask import Flask, render_template, request, redirect, json, jsonify, flash, session,  Response, send_file
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_mail import Mail, Message
import pip
from werkzeug.utils import secure_filename
import pymysql
import os
from datetime import datetime, timedelta
import pandas as pd
from static import source_quotes
from static import s3_uploads
from static.xgb_model import make_inference
from django.views.decorators.csrf import csrf_exempt

import pandas as pd
import datetime
from xgboost import XGBRegressor
from sklearn.metrics import r2_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn import metrics

from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from . import models
from dateutil import parser
from django.core.mail import send_mail
from django.core.mail import send_mail
from static.mpesa_config import generate_access_token, register_mpesa_url, stk_push

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import threading
from django.contrib.sites.shortcuts import get_current_site

raw_dataset = "./static/dataset-1.2.csv"

application = Flask(__name__, template_folder='templates')
mail = Mail(application)
mail_settings = {
    "MAIL_SERVER": 'smtp.mail.us-east-1.awsapps.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ.get('WORKMAIL_USERNAME'),
    "MAIL_PASSWORD": os.environ.get('WORKMAIL_PASSWORD'),
    "MAIL_DEFAULT_SENDER": ("Elijah from SortMyCarKE", os.environ.get('WORKMAIL_USERNAME'))
}

print('email-------------------------')
print(mail_settings)




class EmailThread(threading.Thread):
    def __init__(self,message):
        self.message=message
        threading.Thread.__init__(self)

    def run(self):
        self.message.send()



def read_model_mapping(f):
    data = pd.read_csv(f, usecols=['model_id', 'model','make_id', 'make','region', 'origin', 'body_type'])
    data['make'] = data.make.apply(str.lower)
    data['model'] = data.model.apply(str.lower)
    data['region'] = data.region.apply(str.lower)
    data['origin'] = data.origin.apply(str.lower)
    data['body_type'] = data.body_type.apply(str.lower)
    new_modelMap = pd.DataFrame(data)
    return new_modelMap

model_master = read_model_mapping('./static/model_map.csv')

def ingest_rawdata(raw_data):

    """read the csv raw dataset and do initial preprocessing"""

    raw_data = pd.read_csv(raw_data)

    raw_data['trim'].fillna('standard', inplace=True)
    return raw_data

raw_data2 = ingest_rawdata(raw_dataset)

def signLogbook_s3(request):
    file_name = request.GET["lgbk_key"]
    file_type = request.GET["type"]
    res = s3_uploads.presigned_url(file_name, file_type)
    return JsonResponse(res, safe=False)


def signNatid_s3(request):
    file_name = request.GET["natid_key"]
    file_type = request.GET["type"]
    res=s3_uploads.presigned_url(file_name, file_type)
    return JsonResponse(res,safe=False)




@csrf_exempt
def mobilePayment(request):
    if request.method == 'POST':
        jsonMpesaResponse = request.get_json()
        add_pmt = models.client_payments_table(
        TransactionType=jsonMpesaResponse['TransactionType'],
        TransID=jsonMpesaResponse['TransID'],
        TransTime=jsonMpesaResponse['TransTime'],
        TransAmount=jsonMpesaResponse['TransAmount'],
        BusinessShortCode=jsonMpesaResponse['BusinessShortCode'],
        BillRefNumber=jsonMpesaResponse['BillRefNumber'],
        InvoiceNumber=jsonMpesaResponse['InvoiceNumber'],
        OrgAccountBalance=jsonMpesaResponse['OrgAccountBalance'],
        ThirdPartyTransID=jsonMpesaResponse['ThirdPartyTransID'],
        MSISDN=jsonMpesaResponse['MSISDN'],
        )
        add_pmt.save()
    return


def preprocess_features(raw_data):
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

def valuation(request):

    make = model_master[["make_id", "make"]].drop_duplicates()
    make['make'] = make['make'].str.upper()
    return render(request,'valuation.html',{'make':make})

def personalDetails(request):

    request.session["preferredInsurer"] = request.GET["insuranceName"]
    request.session["coverType"] = request.GET["coverType"]
    request.session["premiumPayable"] = request.GET["premiumAmount"]
    return  HttpResponse('/personalDetails')

def personalDetail(request):
    return render(request,'personal-details.html')


def insurance(request):

    make = model_master[["make_id", "make"]].drop_duplicates()
    make['make'] = make['make'].str.upper()




    new_info = {
        'mak': request.session['Make'].upper(),
        'model': request.session['Model'].upper(),
        'eng_capacity': request.session['ecc'],
        'age': request.session['yom'],
        'make': make

    }

    return render(request,'insurance.html',new_info)
def aboutus(request):
    return render(request,'aboutus.html')

def home(request):
    obj=models.CustomerRating.objects.all()
    return render(request,'welcome.html',{'obj':obj})

def paymentOption(request):

    if request.method == "POST":

        request.session['preferredInsuranceCompany'] = request.session['preferredInsurer']
        request.session['preferredInsurer'] = request.session['preferredInsurer'].replace(" ", "")

        if request.session['preferredInsurer'] == 'JUBILEEALLIANZ':
            request.session['mpesaPaybill'] = "7146151"
            amount = request.session['premiumPayable'].replace(",", "")
            request.session['instal_premium'] = '{:20,.0f}'.format(int(amount) / 3)
        elif request.session['preferredInsurer'] == 'MADISONINSURANCE':
            request.session['mpesaPaybill'] = "600802"
            amount = request.session['premiumPayable'].replace(",", "")
            request.session['instal_premium'] = '{:20,.0f}'.format(int(amount) / 3)

        elif request.session['preferredInsurer'] == 'CORPORATEINSURANCE':
            request.session['mpesaPaybill'] = "942300"
            amount = request.session['premiumPayable'].replace(",", "")
            request.session['instal_premium'] = '{:20,.0f}'.format(int(amount) / 3)

        elif request.session['preferredInsurer'] == 'PIONEERINSURANCE':
            request.session['mpesaPaybill'] = "999415"
            amount = request.session['premiumPayable'].replace(",", "")
            request.session['instal_premium'] = '{:20,.0f}'.format(int(amount) / 3)

        elif request.session['preferredInsurer'] == 'DIRECTLINEASSURANCE':
            if request.session['category'].lower() == 'third_party':
                request.session['mpesaPaybill'] = "4085145"
                amount = request.session['premiumPayable'].replace(",", "")
                request.session['instal_premium'] = '{:20,.0f}'.format(int(amount) / 3)
            else:
                request.session['mpesaPaybill'] = "509800"
                amount = request.session['premiumPayable'].replace(",", "")
                request.session['instal_premium'] = '{:20,.0f}'.format(int(amount) / 3)

        elif request.session['preferredInsurer'] == 'TRIDENTINSURANCE':
            if request.session['category'].lower() == 'third_party':
                request.session['mpesaPaybill'] = "4085145"
                amount = request.session['premiumPayable'].replace(",", "")
                request.session['instal_premium'] = '{:20,.0f}'.format(int(amount) / 3)

            else:
                request.session['mpesaPaybill'] = "985850"
                amount = request.session['premiumPayable'].replace(",", "")
                request.session['instal_premium'] = '{:20,.0f}'.format(int(amount) / 3)

        elif request.session['preferredInsurer'] == 'SANLAMINSURANCE':
            request.session['mpesaPaybill'] = "543200"
            amount = request.session['premiumPayable'].replace(",", "")
            request.session['instal_premium'] = '{:20,.0f}'.format(int(amount) / 3)
        elif request.session['preferredInsurer'] == 'UAPOLDMUTUAL':
            request.session['mpesaPaybill'] = "505800"
            amount = request.session['premiumPayable'].replace(",", "")
            request.session['instal_premium'] = '{:20,.0f}'.format(int(amount) / 3)

        elif request.session['preferredInsurer'] == 'BRITAMINSURANCE':
            request.session['mpesaPaybill'] = "541401"
            amount=request.session['premiumPayable'].replace(",", "")
            request.session['instal_premium'] = '{:20,.0f}'.format(int(amount)/3)

        if request.session['category'].upper() == 'COMPREHENSIVE':
            amount = request.session['premiumPayable'].replace(",", "")
            request.session['instal_premium'] = '{:20,.0f}'.format(int(amount) / 3)

        else:
             request.session['instal_premium'] = "Comprehensive Only"

        ownerNames = request.session['ownerNames'].upper()
        regNum = request.session['regNum'].upper()
        kraPIN = request.session['pinNum']

        if len(kraPIN) < 10:
            request.session['pinNum'] = "ASPERLOGBOOK"
        else:
            request.session['pinNum'] = request.session['pinNum']

        key_logbk = regNum.replace(" ", "") + "-LOGBOOK"
        key_id = regNum.replace(" ", "") + "-" + ownerNames.upper().replace(" ", "")

        S3_LOCATN ='https://{}.s3.amazonaws.com'.format(os.environ.get('S3_LOGBOOKS_BUCKET'))



        request.session['logbookURL'] = f"{S3_LOCATN}/{key_logbk}"
        request.session['natIdURL'] = f"{S3_LOCATN}/{key_id}"

        presigned_logbook_url = s3_uploads.get_s3file(key_logbk)
        presigned_natid_url = s3_uploads.get_s3file(key_id)

        request.session['amountPaid'] = 0
        request.session['paymentRef'] = ""
        startDate = parser.parse(request.session["startDate"])

        startDate = startDate.strftime("%Y-%m-%d")

        add_buy = models.insurance_client_table(cover_type=request.session['category'], insurance_type=request.session['insuranceType'],
                                                insurance_period=request.session['insurancePeriod'], make=request.session['Make'],
                                                model=request.session['Model'], year_man=request.session['yearMan'],
                                                body_type=request.session['bodyType'], owner_type=request.session['ownerType'],
                                                use_case=request.session['useCase'],
                                                tonage=request.session['tonage'], eng_capacity=request.session['engineCapacity'],
                                                seating_capacity=request.session['seatingCapacity'],
                                                owner_names=request.session['ownerNames'],
                                                email_address=request.session['emailAddress'],
                                                owner_contacts=request.session['ownerContact'], reg_number=request.session['regNum'],
                                                pin_number=request.session['pinNum'],
                                                valuation=request.session['valuation'],
                                                preferred_insurer=request.session['preferredInsuranceCompany'],
                                                start_date=startDate, premium=request.session['premiumPayable'],
                                                amount_paid=request.session['amountPaid'], payment_ref=request.session['paymentRef'],
                                                logbook_url=request.session['logbookURL'], natid_url=request.session['natIdURL'])
        add_buy.save()

        add_rating=models.CustomerRating(
             rating=request.session["rate"],
             name=request.session["ownerNames"],
             comment = request.session["vopinion"])
        add_rating.save()


        # send am email to the use
        msg = Message(subject=f"{request.session['regNum']} Welcome to SortMyCarKE, {request.session['ownerNames'].capitalize()}",
                      sender=("Elijah from SortMyCarKE", mail_settings['MAIL_USERNAME']),
                      recipients=[request.session['emailAddress']],
                      cc=["info@sortmycarke.com"],
                      bcc=["elijahkalii@gmail.com"])


        bodyForComprehensive = "<p style='paddng:40px'>Dear " + request.session['ownerNames'].capitalize().split()[0] + " \
                  <br><br>Welcome to SortMyCarKE, your trusted car solutions provider. \
                  <br><br>I am Elijah, your insurance advisor. My duty is to help you get a suitable insurance cover for your asset and support you through any future claims.\
                  <br><br>Please ensure you confirm all details for " + request.session['Make'].upper() + " " + request.session['Model'].upper() + " " + request.session['regNum'].upper() + " \
                  , pay using the company paybill number provided and share the Mpesa message with us. We shall process your insurance certificate within a maximum of 45 minutes thereafter. \
                  <br><br>For any feedback, feel free to reply to this email or call me on 0739881818 \
                  <br><br> Kind regards <br>Elijah Kalii<br><br><b>SortMyCar Africa<br>+254(0)202001810<br><br>VALUE, FAST</p><br><a href='https://sortmycarke.com'>SortMyCar Africa</a></b><br> \
                  <br><br><table style='border:solid;'><tr style='border:solid;'><th>Description</th><th>Details Provided</th> \
                  </tr><tr><td>Owner Names:</td><td>" + request.session['ownerNames'] + "</td></tr><tr > \
                  <td>Email Address:</td><td>" + request.session['emailAddress'] + "</td></tr><tr > \
                  <td>Phone Number:</td><td>" + request.session['ownerContact'] + "</td></tr><tr > \
                  <td>Registration Number:</td><td>" + request.session['regNum'].upper() + "</td></tr><tr > \
                  <td>KRA PIN Number:</td><td>" + request.session.get('pinNum').upper() + "</td></tr><tr > \
                  <td>Type Of Cover:</td><td>" + request.session.get('category').upper() + "</td></tr><tr > \
                  <td>Type Of Insurance:</td><td>" + request.session.get('insuranceType').upper() + "</td></tr><tr > \
                  <td>Period of Insurance:</td><td>" + request.session.get('insurancePeriod').upper() + "</td></tr><tr > \
                  <td>Make of the Car:</td><td>" + request.session.get('Make').upper() + "</td></tr><tr > \
                  <td>Model of the Car:</td><td>" + request.session.get('Model').upper() + "</td></tr><tr > \
                  <td>Type of Car:</td><td>" + request.session.get('bodyType').upper() + "</td></tr><tr > \
                  <td>Type of Owner:</td><td>" + request.session.get('ownerType').upper() + "</td></tr><tr > \
                  <td>Usage Details:</td><td>" + request.session.get('useCase').upper() + "</td></tr><tr > \
                  <td>Year of Manufacture:</td><td>" + str(request.session.get('yearMan')) + "</td></tr><tr > \
                  <td>Engine Capacity (CC):</td><td>" + str(request.session.get('engineCapacity')) + "</td></tr><tr > \
                  <td>Tonage:</td><td>" + request.session.get('tonage') + "</td></tr><tr > \
                  <td>Passenger Seating Capacity:</td> <td>" + str(request.session.get('seatingCapacity')) + "</td></tr><tr> \
                  <td>Estimated Valuation, Ksh:</td><td>" +  request.session.get('valuation') + "</td></tr><tr > \
                  <td>Preferred Insurer:</td> <td>" + str(request.session['preferredInsuranceCompany']) + "</td></tr><tr > \
                  <td>Starting Date:</td> <td>" + startDate + "</td></tr><tr> \
                  <td>Premium Payable, Ksh:</td> <td>" + str( '{:20,.0f}'.format(int( request.session['premiumPayable'])) ) + "</td></tr><tr> \
                  <td>Pay in 3 monthly instalments, Ksh:</td> <td>" + str(request.session['instal_premium']) + " Comprehensive Only </td></tr><tr> \
                  <td>Logbook:</td><td><a href=" + presigned_logbook_url + ">" + key_logbk + "</a></td></tr><tr> \
                  <td>National ID:</td><td><a href=" + presigned_natid_url + ">" + key_id + "</a></td></tr></table>"


        bodyForThirdParty = "<p style='paddng:40px'>Dear " + request.session['ownerNames'].capitalize().split()[0] + " \
                  <br><br>Welcome to SortMyCarKE, your trusted car solutions provider. \
                  <br><br>I am Elijah, your insurance advisor. My duty is to help you get a suitable insurance cover for your asset and support you through any future claims.\
                  <br><br>Please ensure you confirm all details for " + request.session['Make'].upper() + " " + request.session['Model'].upper() + " " + request.session['regNum'].upper() + " \
                  , pay using the company paybill number provided and share the Mpesa message with us. We shall process your insurance certificate within a maximum of 45 minutes thereafter. \
                  <br><br>For any feedback, feel free to reply to this email or call me on 0739881818 \
                  <br><br> Kind regards <br>Elijah Kalii<br><br><b>SortMyCar Africa<br>+254(0)202001810<br><br>VALUE, FAST</p><br><a href='https://sortmycarke.com'>SortMyCar Africa</a></b><br> \
                  <br><br><table style='border:solid;'><tr style='border:solid;'><th>Description</th><th>Details Provided</th> \
                  </tr><tr><td>Owner Names:</td><td>" + request.session['ownerNames'] + "</td></tr><tr > \
                  <td>Email Address:</td><td>" + request.session['emailAddress'] + "</td></tr><tr > \
                  <td>Phone Number:</td><td>" + request.session['ownerContact'] + "</td></tr><tr > \
                  <td>Registration Number:</td><td>" + request.session['regNum'].upper() + "</td></tr><tr > \
                  <td>KRA PIN Number:</td><td>" + request.session.get('pinNum').upper() + "</td></tr><tr > \
                  <td>Type Of Cover:</td><td>" + request.session.get('category').upper() + "</td></tr><tr > \
                  <td>Type Of Insurance:</td><td>" + request.session.get('insuranceType').upper() + "</td></tr><tr > \
                  <td>Period of Insurance:</td><td>" + request.session.get('insurancePeriod').upper() + "</td></tr><tr > \
                  <td>Make of the Car:</td><td>" + request.session.get('Make').upper() + "</td></tr><tr > \
                  <td>Model of the Car:</td><td>" + request.session.get('Model').upper() + "</td></tr><tr > \
                  <td>Type of Car:</td><td>" + request.session.get('bodyType').upper() + "</td></tr><tr > \
                  <td>Type of Owner:</td><td>" + request.session.get('ownerType').upper() + "</td></tr><tr > \
                  <td>Usage Details:</td><td>" + request.session.get('useCase').upper() + "</td></tr><tr > \
                  <td>Tonage:</td><td>" + request.session.get('tonage') + "</td></tr><tr > \
                  <td>Passenger Seating Capacity:</td> <td>" + str(request.session.get('seatingCapacity')) + "</td></tr><tr> \
                  <td>Preferred Insurer:</td> <td>" + str(request.session['preferredInsuranceCompany']) + "</td></tr><tr > \
                  <td>Starting Date:</td> <td>" + startDate + "</td></tr><tr> \
                  <td>Premium Payable, Ksh:</td> <td>" + str('{:20,.0f}'.format(int( request.session['premiumPayable']))) + "</td></tr><tr> \
                  <td>Pay in 3 monthly instalments, Ksh:</td> <td>" + str(request.session['instal_premium']) + " Comprehensive Only</td></tr><tr> \
                  <td>Logbook:</td><td><a href=" + presigned_logbook_url + ">" + key_logbk + "</a></td></tr><tr> \
                  <td>National ID:</td><td><a href=" + presigned_natid_url + ">" + key_id + "</a></td></tr></table>"

        if request.session['category'].lower() == "third_party":
            html_message = bodyForThirdParty
        else:
            html_message = bodyForComprehensive


        subject= f"{request.session['regNum']} Welcome to SortMyCarKE, {request.session['ownerNames'].capitalize()}"
        from_email=os.environ.get('WORKMAIL_USERNAME')
        # message = EmailMessage(subject, html_message, from_email, [request.session['emailAddress']],bcc=['elijahkalii@gmail.com'], cc=['info@sortmycarke.com'])
        message = EmailMessage(subject, html_message, from_email, [request.session['emailAddress']])
        message.content_subtype = 'html'

        EmailThread(message).start()

        contetx={
            "PreferredInsurer":request.session['preferredInsuranceCompany'],
            "startDate":startDate,
            "premiumPayable":request.session['premiumPayable'],
            "instal_premium":request.session['instal_premium'],
            "mpesaPaybill":request.session['mpesaPaybill'],
            "category":request.session['category'].lower(),
            "regNo":request.session['regNum'].upper(),
            "phone": request.session['ownerContact']
        }

        return render(request,'payment-option.html',contetx)
    else:
        startDate = parser.parse(request.session["startDate"])
        startDate = startDate.strftime("%Y-%m-%d")
        contetx = {
            "PreferredInsurer": request.session['preferredInsuranceCompany'],
            "startDate": startDate,
            "premiumPayable": request.session['premiumPayable'],
            "instal_premium": request.session['instal_premium'],
            "mpesaPaybill": request.session['mpesaPaybill'],
            "category": request.session['category'].lower()
        }
        return render(request, 'payment-option.html', contetx)


def saveContact(request):

    subject = f"{request.GET['cemail'].lower()} , {request.GET['cphone']}, {request.GET['cfname'].upper()}"
    from_email = os.environ.get('WORKMAIL_USERNAME')
    html_message = request.GET["message"]

    request.session["cemail"] = request.GET['cemail'].lower()
    request.session["cphone"] = request.GET['cphone']
    request.session["cfname"] = request.GET['cfname']

    # message = EmailMessage(subject, html_message,from_email , ['maurice.otieno@jubileekenya.com'],bcc=['elijahkalii@gmail.com'],cc=['info@sortmycarke.com'])
    message = EmailMessage(subject, html_message,from_email , ['morinyomoi@gmail.com'])
    EmailThread(message).start()
    return HttpResponse("success")


def saveRating(request):

    rate=request.GET['star']
    opinion=request.GET['opinion']
    request.session["rate"]=rate
    request.session["vopinion"]=opinion
    return HttpResponse("success")


def confirmation(request):
    phone_number = request.session['ownerContact']
    amount = int(request.GET["amount"])
    request.session["amount"]=amount
    account_reference = 'KCZ064Y'
    transaction_desc = 'Third-Party cover for KCZ064Y'
    c_url = ''.join(['http://', get_current_site(request).domain, '/mobilePayment'])
    obj = stk_push(phone_number, amount, account_reference, transaction_desc,c_url)
    return JsonResponse({
        "obj":obj
    })


def showConfirmation(request):

    startDate = parser.parse(request.session["startDate"])
    startDate = startDate.strftime("%Y-%m-%d")
    # amount = '{:20,.2f}'.format(int(request.session["amount"]))
    amount = '{:20,.2f}'.format(int(request.session["amount"]))
    context = {
        "preferredInsuranceCompany": request.session['preferredInsuranceCompany'],
        "amount": amount,
        "startDate": startDate
    }
    return render(request,'confirmation.html',context)

def detailsSummary(request):
    if request.method=="POST":
        category = request.session['category']
        coverType = request.session['coverType']
        period = request.session['insurancePeriod']
        make =  request.session['Make'].lower()
        make_upper = request.session['Make'].upper()
        model =  request.session['Model'].lower()

        yom =  request.session['yearMan']
        vtype = request.session['bodyType']
        ownership = request.session['ownerType']
        usage = request.session['useCase']
        ecc = request.session['engineCapacity']
        pc = request.session['seatingCapacity']
        tonage = request.session['tonage']
        if len(request.session['valuation']) > 0:
            estValue = '{:20,.2f}'.format(round(int(request.session['valuation']), -4))
        else:
            estValue = request.session['valuation']

        name = request.POST["ownerNames"]

        phone ='254' + request.POST["phone"][-9:]
        email = request.POST["email"]

        reg = request.POST["regNum"].upper()
        kra = request.POST["kraPIN"]
        kraPIN = request.POST["kraPIN"]
        sdate = request.POST["startDate"]

        if len(kraPIN) < 10:
            request.session['kraPIN'] = "AS PER LOGBOOK"
        else:
            request.session['kraPIN'] = request.POST["kraPIN"]

        key_logbk = reg.replace(" ", "") + "-LOGBOOK"
        key_id = reg.replace(" ", "") + "-" + name.upper().replace(" ", "")

        S3_LOCATN = 'https://{}.s3.amazonaws.com'.format(os.environ.get('S3_LOGBOOKS_BUCKET'))

        request.session['logbookURL'] = f"{S3_LOCATN}/{key_logbk}"
        request.session['natIdURL'] = f"{S3_LOCATN}/{key_id}"

        presigned_logbook_url = s3_uploads.get_s3file(key_logbk)
        presigned_natid_url = s3_uploads.get_s3file(key_id)

        request.session['presigned_natid_url']=presigned_natid_url
        request.session['presigned_logbook_url']=presigned_logbook_url

        startDate = parser.parse(request.POST["startDate"])

        startDate = startDate.strftime("%Y-%m-%d")

        request.session['make_upper'] = make_upper

        request.session['ownerNames']=name
        request.session['ownerContact']=phone
        request.session['emailAddress']=email
        request.session['pinNum'] = kra
        request.session['regNum'] = reg
        request.session['startDate'] = startDate

        context = {
            "category": category.upper(),
            "coverType": request.session['insuranceType'].upper(),
            "period": period.upper(),
            "make": make.upper(),
            "make_upper": make_upper,
            "model": model.upper(),
            "yom": yom,
            "vtype": vtype.upper(),
            "ownership": ownership.upper(),
            "usage": usage.upper(),
            "ecc": ecc,
            "pc": pc,
            "tonage": tonage,
            "estValue": estValue,
            "name":name.upper(),
            "phone":phone,
            "email":email,
            "reg":reg.upper(),
            "kra":request.session['kraPIN'].upper(),
            "sdate":sdate,
            "ID":presigned_natid_url,
            "logbook":presigned_logbook_url,
        }

        return render(request, 'details-summary.html', context)
    else:

        category = request.session['category']
        coverType = request.session['coverType']
        period = request.session['insurancePeriod']
        make = request.session['Make'].lower()
        make_upper = request.session['Make'].upper()
        model = request.session['Model'].lower()

        yom = request.session['yearMan']
        vtype = request.session['bodyType']
        ownership = request.session['ownerType']
        usage = request.session['useCase']
        ecc = request.session['engineCapacity']
        pc = request.session['seatingCapacity']
        tonage = request.session['tonage']
        context = {
            "category": category.upper(),
            "coverType": request.session['insuranceType'].upper(),
            "period": period.upper(),
            "make": make.upper(),
            "make_upper": make_upper,
            "model": model.upper(),
            "yom": yom,
            "vtype": vtype.upper(),
            "ownership": ownership.upper(),
            "usage": usage.upper(),
            "ecc": ecc,
            "pc": pc,
            "tonage": tonage,
            "estValue": request.session['valuation'],
            "name": request.session['ownerNames'].upper(),
            "phone": request.session['ownerContact'],
            "email": request.session['emailAddress'],
            "reg": request.session['regNum'].upper(),
            "kra": request.session['kraPIN'].upper(),
            "sdate": request.session['startDate'],
            "ID": request.session['presigned_natid_url'],
            "logbook":request.session['presigned_logbook_url'] ,
        }

        return render(request, 'details-summary.html', context)
def insuranceCompanies(request):

    if request.method=="POST":
        category = request.POST['category']
        request.session["category"]=category
        coverType = request.POST['coverType']
        period = request.POST['period']
        make = model_master[model_master['make_id'] == int(request.POST['make'])].make.iloc[0].lower()
        make_upper = model_master[model_master['make_id'] == int(request.POST['make'])].make.iloc[0].upper()
        model = model_master[model_master['model_id'] == int(request.POST['model'])].model.iloc[0].lower()
        yom = request.POST['yom']
        vtype = request.POST['vtype']
        ownership = request.POST['ownership']
        usage = request.POST['usage']
        ecc = request.POST['ecc']
        pc = request.POST['pc']
        tonage = request.POST['tonage']
        estValue = request.POST['estValue']


        request.session['category'] = category.upper()
        request.session['coverType'] = category.upper()
        request.session['insuranceType'] = coverType.upper()
        request.session['insurancePeriod'] = period
        request.session['Make'] = make.upper()
        request.session['Model'] = model.upper()
        request.session['yearMan'] = yom
        request.session['bodyType'] = vtype.upper()
        request.session['ownerType'] = ownership.upper()
        request.session['useCase'] = usage.upper()
        request.session['engineCapacity'] = ecc
        request.session['seatingCapacity'] = pc
        request.session['tonage'] = tonage
        request.session['valuation'] = estValue
        request.session['make_upper'] = make_upper

        new_info = {
            'cover_type': category.lower(),
            'insurance_type': coverType.lower(),
            'insurance_period': period.lower(),
            'make': make.lower(),
            'model': model.lower(),
            'year_man': yom,
            'body_type': vtype.lower(),
            'owner_type': ownership.lower(),
            'use_case': usage.lower(),
            'eng_capacity': ecc,
            'seating_capacity': pc,
            'tonage': tonage
        }
        if len(estValue) == 0:
            new_info['valuation'] = 0
        else:
            new_info['valuation'] = int(estValue)

        if len(new_info['year_man']) == 0:
            age = 0
        else:
            current_yr = datetime.date.today().year
            age = current_yr - int(new_info['year_man'])
        if len(new_info['eng_capacity']) == 0:
            new_info['eng_capacity'] = 0
        else:
            new_info['eng_capacity'] = int(ecc)

        if len(new_info['seating_capacity']) == 0:
            new_info['seating_capacity'] = 0
        else:
            # new_info['seating_capacity'] = int(pc)
            new_info['seating_capacity'] = 0

        if len(new_info['tonage']) == 0:
            new_info['tonage'] = 0
        else:
            # new_info['tonage'] = int(tonage)
            new_info['tonage'] = 0


        quotation = source_quotes.quotations(cover_type=new_info['cover_type'], model=new_info['model'],  duration=new_info['insurance_period'], age=age, ins_type=new_info['insurance_type'], owner_type=new_info["owner_type"], body_type=new_info['body_type'], usage=new_info['use_case'], tonnage=new_info["tonage"], seat_cap=new_info['seating_capacity'], sum_assured=new_info['valuation'])

        request.session['quotation']=quotation


        est_value=request.session['estm_value']
        yom=request.session['yom']
        make=request.session['Make']
        model=request.session['Model']
        trim=request.session['trim']
        ecc=request.session['ecc']
        fuel=request.session['fuel']
        mileage=request.session['mileage']
        transmission=request.session['transmission']
        usage=request.session['usage']
        if(category.lower()=="third_party"):
            cover="Third Party"
        else:
            cover = category.lower()

        context={
            'est_value':est_value,
            'yom':yom,
            'make':make.upper(),
            'model':model.upper(),
            'trim':trim.upper(),
            'ecc':ecc.upper(),
            'fuel':fuel.upper(),
            'mileage':mileage,
            'transmission':transmission.upper(),
            'usage':usage.upper(),
            'quotation':quotation,
            'coverType':cover
             }
        return render(request,'insurance-companies.html',context)
    else:

        if (request.session["category"].lower() == "third_party"):
            cover = "Third Party"
        else:
            cover = request.session["category"].lower()

        context = {
            'est_value': request.session['estm_value'],
            'yom': request.session['yom'],
            'make': request.session['Make'].upper(),
            'model': request.session['Model'].upper(),
            'trim': request.session['trim'].upper(),
            'ecc': request.session['ecc'],
            'fuel':  request.session['fuel'].upper(),
            'mileage': request.session['mileage'],
            'transmission': request.session['transmission'].upper(),
            'usage': request.session['usage'].upper(),
            'quotation': request.session['quotation'],
            'coverType': cover
        }
        return render(request, 'insurance-companies.html',context)


def valuate(request):
    if request.method=="POST":
        yomf=request.POST["yom"]

        yom = int(yomf)
        make=model_master[model_master['make_id'] == int(request.POST['make'])].make.iloc[0].lower()
        model=model_master[model_master['model_id'] == int(request.POST['model'])].model.iloc[0].lower()

        if bool(request.POST["trim"]):
            trim =request.POST["trim"]
        else:
            trim ="Standard"

        ecc=request.POST["ecc"]
        fuel=request.POST["fuel"]
        mileage=request.POST["mileage"]
        transmission=request.POST["transmission"]
        usage=request.POST["usage"]

        request.session['yom']=yomf
        request.session['make']=make
        request.session['model']=model
        request.session['trim']=trim
        request.session['ecc']=ecc
        request.session['fuel']=fuel
        request.session['mileage']=mileage
        request.session['transmission']=transmission
        request.session['usage']=usage

        current_yr = datetime.date.today().year

        age = current_yr - yom
        new_info = {
            'make': make,
            'model': model,
            'fuel_type': fuel,
            'eng_capacity': ecc,
            'transmission': transmission,
            'how_used': usage,
            'mileage': mileage,
            'age': age,

        }

        new_info['trim'] = 'standard'
         #convert the dictionary to a df
        df1 = pd.DataFrame([new_info])
        df1 = df1.loc[:,[ 'make', 'model', 'trim', 'transmission', 'how_used', 'fuel_type', 'eng_capacity','mileage', 'age']]

        #Do a vlook-up in the model_map table to get the other details and add to the df
        all_otherdetails = pd.merge(df1, model_master, how ='left', on=['make', 'model'])
        all_otherdetails = all_otherdetails.drop(['make_id', 'model_id'], axis=1)

        all_otherdetails['descriptn'] = all_otherdetails['make']+' '+all_otherdetails['model']+' '+all_otherdetails['trim']+' '+all_otherdetails['region']+' '+all_otherdetails['origin']+ ' '+all_otherdetails['body_type']
        # +' '+all_otherdetails['model']+' '+all_otherdetails['trim']+' '+all_otherdetails['region']+' '+all_otherdetails['origin']+ ' '+all_otherdetails['body_type']

        new_data = all_otherdetails.loc[:,[ 'descriptn', 'transmission', 'how_used', 'fuel_type', 'eng_capacity','mileage', 'age']]
        new_data = new_data.rename({'how_used':'usage'}, axis='columns')
        new_data['usage'] = new_data.usage.map({'locally_used': str(0), 'foreign_used': str(1)})
        new_data['fuel_type'] = new_data.fuel_type.map({'petrol': str(0), 'diesel': str(1), 'hybrid': str(2)})
        new_data['transmission'] = new_data.transmission.map({'automatic': str(0), 'manual': str(1), 'cvt': str(2)})

        prediction=make_inference(new_data) * 0.85

        estm_value = '{:20,.2f}'.format(round(int(prediction[0]), -4))


        request.session['estm_value']=estm_value
        if bool(request.POST["trim"]):
            trim = request.POST["trim"]
        else:
            trim = "Standard"

        context = {
            'estm_value': estm_value,
            'make': make,
            'model': model,
            'trim': trim,
            'ecc': ecc,
            'fuel': fuel,
            'mileage': mileage,
            'transmission': transmission,
            'usage': usage,
            'yom':yomf
        }
        return render(request,'summary.html',context)
    else:
        context = {
            'estm_value': request.session['estm_value'],
            'make': request.session['make'],
            'model': request.session['model'],
            'trim': request.session['trim'],
            'ecc': request.session['ecc'],
            'fuel': request.session['fuel'],
            'mileage': request.session['mileage'],
            'transmission': request.session['transmission'],
            'usage': request.session['usage'],
            'yom': request.session['yom']
        }
        return render(request, 'summary.html', context)


def modelbymake(request,id):
    result = model_master[model_master['make_id']==int(id)].loc[:,['model_id', 'model']]

    result['model'] = result['model'].str.upper()

    modelArray = []
    for i in range(len(result)):
        modelObj = {
            'id': int(result.iloc[i, 0]),
            'name': result.iloc[i, 1]}
        modelArray.append(modelObj)
    return JsonResponse({"model_make":modelArray})





