import json
import datetime
import requests
from requests.auth import HTTPBasicAuth
from base64 import b64encode
from .models import MpesaDetails


def get_access_token(consumer_key, consumer_secret):
    """
    :return: auth token for mpesa api calls
    """
    oauth_url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(oauth_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    access_token = json.loads(response.text).get('access_token', None)

    return access_token


def get_timestamp():
    """
    :return: String Timestamp that is usable with mpesa api
    """
    t = datetime.datetime.now()
    year = t.year
    month = "{0:0=2d}".format(t.month)
    day = "{0:0=2d}".format(t.day)
    hour = "{0:0=2d}".format(t.hour)
    minute = "{0:0=2d}".format(t.minute)
    second = "{0:0=2d}".format(t.second)

    return '{}{}{}{}{}{}'.format(year, month, day, hour, minute, second)


def generate_password(timestamp, mpesa_shortcode, lipa_na_mpesa_online_passkey):
    bytes_obj = '{}{}{}'.format(mpesa_shortcode, lipa_na_mpesa_online_passkey, timestamp).encode('utf-8')
    encoded = b64encode(bytes_obj)
    encoded_str = encoded.decode('utf-8')
    return encoded_str


def lipa_na_mpesa_online_payment(account_number, amount, phone_number, description):
    """
    Sends stk push
    :param account_number: account number to deposit funds into
    :param amount: amount in kenyan shillings
    :param phone_number: phone number of the recipient of the stk push
    :param transaction_description: A description of the transaction
    :return:
    """
    mpesa_details = MpesaDetails.objects.first()
    mpesa_shortcode = mpesa_details.mpesa_shortcode
    lipa_na_mpesa_online_passkey = mpesa_details.lipa_na_mpesa_online_passkey

    access_token = get_access_token(mpesa_details.daraja_consumer_key, mpesa_details.daraja_consumer_secret)
    api_url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer {}".format(access_token)}
    timestamp = get_timestamp()

    stk_callback_url = '{}/mpesa/stk-push/callback/'.format(mpesa_details.site_url)
    request = {
        "BusinessShortCode": mpesa_shortcode,
        "Password": generate_password(timestamp, mpesa_shortcode, lipa_na_mpesa_online_passkey),
        "Timestamp": timestamp,
        "TransactionType": 'CustomerPayBillOnline',
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": mpesa_shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": stk_callback_url,
        "AccountReference": account_number,
        "TransactionDesc": description
    }

    response = requests.post(api_url, json=request, headers=headers)
    return response


def lipa_na_mpesa_online_query_request(checkout_request_id):
    """
    Used to confirm a payment
    :param checkout_request_id:
    :return:
    """

    api_url = "https://api.safaricom.co.ke/mpesa/stkpushquery/v1/query"
    timestamp = get_timestamp()

    mpesa_details = MpesaDetails.objects.first()
    mpesa_shortcode = mpesa_details.mpesa_shortcode
    lipa_na_mpesa_online_passkey = mpesa_details.lipa_na_mpesa_online_passkey
    access_token = get_access_token(mpesa_details.daraja_consumer_key, mpesa_details.daraja_consumer_secret)
    headers = {"Authorization": "Bearer {}".format(access_token)}

    data = {
        "BusinessShortCode": mpesa_shortcode,
        "Password": generate_password(timestamp, mpesa_shortcode, lipa_na_mpesa_online_passkey),
        "Timestamp": timestamp,
        "CheckoutRequestID": checkout_request_id
    }

    response = requests.post(api_url, json=data, headers=headers)

    return response
