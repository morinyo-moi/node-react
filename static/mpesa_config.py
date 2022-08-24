import requests
from requests.auth import HTTPBasicAuth
from static.mpesa_exceptions import MpesaConfigurationException, IllegalPhoneNumberException, MpesaConnectionError, \
    MpesaError, MpesaInvalidParameterException, MpesaConnectionError
from requests import Response
import time
import os
import json
import base64
from datetime import datetime

mpesa_environment = 'production'
base_url = 'https://sortmycarke.com'
sandbox_paybill = '600986'
mpesa_paybill = '4085145'
consumer_key = os.environ.get("MPESA_CONSUMER_KEY")
consumer_secret = os.environ.get("MPESA_CONSUMER_SECRET")

if mpesa_environment == 'sandbox':
    business_short_code = sandbox_paybill
else:
    business_short_code = mpesa_paybill


def api_base_url():
    if mpesa_environment == 'sandbox':
        # return 'https://sandbox.safaricom.co.ke/'
        return 'https://api.safaricom.co.ke/'
    elif mpesa_environment == 'production':
        return 'https://api.safaricom.co.ke/'
        # return 'https://sandbox.safaricom.co.ke/'


def format_phone_number(phone_number):
    if len(phone_number) < 9:
        return 'Phone number too short'
    else:
        return '254' + phone_number[-9:]


def generate_access_token(consumer_key, consumer_secret):
    url = api_base_url() + 'oauth/v1/generate?grant_type=client_credentials'

    try:
        r = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        token = r.text
        response = json.loads(token)
        mpesa_access_token = response['access_token']
        print("xxxxxxxxxxxxxxxxxxxxxxxx")
        print(mpesa_access_token)
        print("xxxxxxxxxxxxxxxxxxxxxxxx")
    except Exception as ex:
        print("Could not generate access code")
        return ex
    return mpesa_access_token


def register_mpesa_url():
    mpesa_endpoint = api_base_url() + 'mpesa/c2b/v1/registerurl'
    headers = {
        'Authorization': 'Bearer ' + str(generate_access_token(consumer_key, consumer_secret)),
        'Content-Type': 'application/json'
    }
    req_body = {
        'ShortCode': business_short_code,
        'ResponseType': 'Completed',
        'ConfirmationURL': base_url + '/c2b/confirmation',
        'ValidationURL': base_url + '/c2b/validation'}

    response_data = requests.post(mpesa_endpoint, json=req_body, headers=headers)
    return response_data.json()


# stk push for incoming payments
def stk_push(phone_number, amount, account_reference, transaction_desc,c_url):
    """
	Attempt to send an STK prompt to customer phone
		Args:
			phone_number (str): -- The Mobile Number to receive the STK Pin Prompt.
			amount (int) -- This is the Amount transacted normaly a numeric value. Money that customer pays to the Shorcode. Only whole numbers are supported.
			account_reference (str) -- This is an Alpha-Numeric parameter that is defined by your system as an Identifier of the transaction for CustomerPayBillOnline transaction type. Along with the business name, this value is also displayed to the customer in the STK Pin Prompt message. Maximum of 12 characters.
			transaction_desc (str) -- This is any additional information/comment that can be sent along with the request from your system. Maximum of 13 Characters.
			call_back_url (str) -- This s a valid secure URL that is used to receive notifications from M-Pesa API. It is the endpoint to which the results will be sent by M-Pesa API.
		Returns:
			MpesaResponse: MpesaResponse object containing the details of the API response

		Raises:
			MpesaInvalidParameterException: Invalid parameter passed
			MpesaConnectionError: Connection error
	"""


    if str(account_reference).strip() == '':
        raise MpesaInvalidParameterException('Account reference cannot be blank')
    if str(transaction_desc).strip() == '':
        raise MpesaInvalidParameterException('Transaction description cannot be blank')
    if not isinstance(amount, int):
        raise MpesaInvalidParameterException('Amount must be an integer')

    callback_url = base_url + '/c2b/confirmation'
    phone_number = format_phone_number(phone_number)
    url = api_base_url() + 'mpesa/stkpush/v1/processrequest'
    passkey = os.environ.get('MPESA_PASSKEY')

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode((business_short_code + passkey + timestamp).encode('ascii')).decode('utf-8')
    transaction_type = 'CustomerPayBillOnline'
    party_a = phone_number
    party_b = business_short_code

    data = {
        'BusinessShortCode': business_short_code,
        'Password': password,
        'Timestamp': timestamp,
        'TransactionType': transaction_type,
        'Amount': amount,
        'PartyA': party_a,
        'PartyB': party_b,
        'PhoneNumber': phone_number,
        'CallBackURL': callback_url,
        'AccountReference': account_reference,
        'TransactionDesc': transaction_desc
    }
    headers = {"Authorization": "Bearer %s" % generate_access_token(consumer_key, consumer_secret),
               'Content-Type': 'application/json'
               }
    try:
        r = requests.post(url, json=data, headers=headers)
        response = r.text
        return json.loads(response)
    except requests.exceptions.ConnectionError:
        raise MpesaConnectionError('Connection failed')
    except Exception as ex:
        raise MpesaConnectionError(str(ex))


# outgoing payments
def b2c_payment(phone_number, amount, transaction_desc, callback_url, occassion, command_id='BusinessPayment'):
    """
	Attempt to perform a business payment transaction
	Args:
		phone_number (str): -- The Mobile Number to receive the STK Pin Prompt.
		amount (int) -- This is the Amount transacted normaly a numeric value. Money that customer pays to the Shorcode. Only whole numbers are supported.
		transaction_desc (str) -- This is any additional information/comment that can be sent along with the request from your system. Maximum of 13 Characters.
		call_back_url (str) -- This s a valid secure URL that is used to receive notifications from M-Pesa API. It is the endpoint to which the results will be sent by M-Pesa API.
		occassion (str) -- Any additional information to be associated with the transaction.
	Returns:
		MpesaResponse: MpesaResponse object containing the details of the API response

	Raises:
		MpesaInvalidParameterException: Invalid parameter passed
		MpesaConnectionError: Connection error
	"""

    if str(transaction_desc).strip() == '':
        raise MpesaInvalidParameterException('Transaction description cannot be blank')
    if not isinstance(amount, int):
        raise MpesaInvalidParameterException('Amount must be an integer')

    phone_number = format_phone_number(phone_number)
    url = api_base_url() + 'mpesa/b2c/v1/paymentrequest'

    party_a = business_short_code
    party_b = phone_number
    initiator_username = ''

    data = {
        'CommandID': command_id,
        'Amount': amount,
        'PartyA': party_a,
        'PartyB': party_b,
        'Remarks': transaction_desc,
        'QueueTimeOutURL': callback_url,
        'ResultURL': callback_url,
        'Occassion': occassion
    }

    headers = {
        'Authorization': 'Bearer ' + str(generate_access_token(consumer_key, consumer_secret)),
        'Content-Type': 'application/json'
    }

    try:
        r = requests.post(url, json=data, headers=headers)
        response = r.json()
        return response
    except requests.exceptions.ConnectionError:
        raise MpesaConnectionError('Connection failed')
    except Exception as ex:
        raise MpesaConnectionError(str(ex))
