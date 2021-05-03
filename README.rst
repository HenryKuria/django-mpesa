=========================
django-mpesa-payments
=========================

django-mpesa-payments is a Django app to enable mpesa transactions on the web. Currently it features only the STK Push functionality.
The STK push will enable you to make payment request to users.


Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "mpesa" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'mpesa',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('mpesa/', include('mpesa.urls')),

3. Run ``python manage.py migrate`` to create the mpesa models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to add your paybill and developer account details for daraja. (you'll need the Admin app enabled).



APP ENDPOINTS
-------------

1. mpesa/request-stk-push/
    This endpoint sends a payment request to a users phone

    Below shows a test case for this endpoint. It demonstrates how this endpoint is used

    .. code-block::

        def test_send_stk_push(self):
            response = self.client.post(
                path='http://localhost:3000/mpesa/request-stk-push/',
                data={
                    'account_number': 'test_account', # replace with the account number that is to receive funds
                    'amount': '1', # replace with amount
                    'phone_number': '710586622', # replace with user phone number. Notice that '+254' is not included. It is hardcoded in the app
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
                path='http://localhost:3000/mpesa/stk-push/callback/',
                data={
                    'Body': {
                        'stkCallback': {
                            'MerchantRequestID': '<Merchant request ID>',
                            'CheckoutRequestID': 'ws_CO_30042021100956718221',
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
                path='http://localhost:3000/mpesa/confirm-stk-push-payment/',
                data={
                    'checkoutRequestID': 'ws_CO_29042021104344781746'
                }
            )
            data = response.json()
            self.assertEqual(data['ResponseCode'], "0")
            self.assertEqual(data['ResponseDescription'], "The service request has been accepted successsfully")
            self.assertEqual(data['ResultCode'], "0")
            self.assertEqual(data['ResultDesc'], "The service request is processed successfully.")
