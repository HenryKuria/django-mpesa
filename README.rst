
django-mpesa-payments
=========================

django-mpesa-payments is a django app to enable mpesa transactions on the web. Currently it features only the STK Push functionality.
The STK push will enable you to make payment request to users.


Quick start
-----------
1. Installation
    .. code-block::

        pip install django-mpesa-payments

2. Install required libraries
    .. code-block::

        pip install requests

2. Add "mpesa" to your INSTALLED_APPS setting like this
    .. code-block::

        INSTALLED_APPS = [
            ...
            'mpesa',
        ]

3. Include the mpesa URLconf in your project urls.py like this::
    .. code-block::

        path('mpesa/', include('mpesa.urls')),

4. Run ``python manage.py migrate`` to create the mpesa models.

5. Start the development server and visit http://127.0.0.1:8000/admin/
   to add your paybill and developer account details for daraja. (you'll need the Admin app enabled).



APP ENDPOINTS
-------------

1. mpesa/request-stk-push/
    This endpoint sends a payment request to a users phone

    Below shows a test case for this endpoint. It demonstrates how this endpoint is used

    .. code-block::

        def test_send_stk_push(self):
            response = self.client.post(
                path='http://127.0.0.1:8000/mpesa/request-stk-push/',
                data={
                    'account_number': 'test_account', # replace with the account number that is to receive funds
                    'amount': '100',
                    'phone_number': '712345678', # replace with user phone number. Notice that '+254' is not included. It is hardcoded in the app
                    'description': 'test_payment', # replace with adequate description
                }
            )
            data = response.json()
            self.assertEqual(data['ResponseCode'], "0")
            self.assertEqual(data['ResponseDescription'], "Success. Request accepted for processing")
            self.assertEqual(data['CustomerMessage'], "Success. Request accepted for processing")

2. mpesa/stk-push/callback/
    This endpoint receives the callback from safaricom servers.
    Safaricom calls this endpoint after processing the stk push. The structure of the post data sent by safaricom is demonstrated in the test case function below

    .. code-block::

        def test_callback_url(self):
            response = self.client.post(
                content_type='application/json',
                path='http://127.0.0.1:8000/mpesa/stk-push/callback/',
                data={
                    'Body': {
                        'stkCallback': {
                            'MerchantRequestID': '<Merchant request ID>',
                            'CheckoutRequestID': '<Checkout request ID>',
                            'ResultCode': 1031,
                            'ResultDesc': 'Request cancelled by user'
                        }
                    }
                }
            )
            data = response.json()
            self.assertEqual(data['ResultCode'], 0)
            self.assertEqual(data['ResultDesc'], 'Success')



3. mpesa/confirm-stk-push-payment/
    This endpoint confirms an mpesa payment using the checkout request id
    Below shows a test case demonstrating how this endpoint is used.

    .. code-block::

        def test_confirm_mpesa_stk_push_payment(self):
            response = self.client.post(
                path='http://127.0.0.1:8000/mpesa/confirm-stk-push-payment/',
                data={
                    'checkoutRequestID': '<Checkout request ID>' # checkout request id for a valid payment
                }
            )
            data = response.json()
            self.assertEqual(data['ResponseCode'], "0")
            self.assertEqual(data['ResponseDescription'], "The service request has been accepted successsfully")
            self.assertEqual(data['ResultCode'], "0")
            self.assertEqual(data['ResultDesc'], "The service request is processed successfully.")


Usage
----------------
**Retrieve a saved mpesa online payment**

    .. code-block::

        from mpesa.models import LipaNaMpesaOnlinePayment

        payment = LipaNaMpesaOnlinePayment.objects.get(checkout_request_Id=<checkout_request_Id>)


**Display meta data for a payment**

    .. code-block::

        from mpesa.models import LipaNaMpesaOnlinePayment, LipaNaMpesaOnlinePaymentCallbackMetadataItem

        payment = LipaNaMpesaOnlinePayment.objects.get(checkout_request_Id=<checkout_request_Id>)

        for meta_data in payment.CallbackMetadataItems:
            print(meta_data.name, meta_data.value)

    For each payment, the meta data are:
        1. The amount paid
        2. The receipt number of the transaction
        3. The transaction date
        4. The phone number of the user that made the payment


Further Reading
----------------

**Model Reference**

class LipaNaMpesaOnlinePayment
""""""""""""""""""""""""""""""""""""""""""""
    This model stores the response data from safaricom when a successful payment is made.

    *Database Fields*

    **merchant_request_Id**

    (text)

    The ID of the merchant that requested the payment

    **checkout_request_Id**

    (text)

    The ID of the payment request that was made for this payment

    **result_code**

    (number)

    The result code of a payment

    **result_description**

    (text)

    a short description of the transaction.


class LipaNaMpesaOnlinePaymentCallbackMetadataItem
""""""""""""""""""""""""""""""""""""""""""""""""""

This model stores the meta data for each successful payment

    *Database Fields*

    **payment**

    (foreign key to LipaNaMpesaOnlinePayment )

    The foreign key to the payment that a meta data is for

    **name**

    (text)

    The name of the meta data

    **value**

    (text)

    The value of the meta data item
