from django.test import TestCase, Client


class TestSTKPush(TestCase):
    fixtures = ['data.json']

    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

    def test_customer_has_sufficient_funds(self):
        response = self.client.post(
            path='http://localhost:3000/mpesa/request-stk-push/',
            data={
                'account_number': 'test_account',
                'amount': '1',
                'phone_number': '712345678',
                'description': 'test_payment',
            }
        )
        data = response.json()
        self.assertEqual(data['ResponseCode'], "0")
        self.assertEqual(data['ResponseDescription'], "Success. Request accepted for processing")
        self.assertEqual(data['CustomerMessage'], "Success. Request accepted for processing")

    def test_customer_has_insufficient_funds_and_insufficient_fuliza(self):
        response = self.client.post(
            path='http://localhost:3000/mpesa/request-stk-push/',
            data={
                'account_number': 'test_account',
                'amount': '100000',  # amount greater than both customer fuliza and account balance
                'phone_number': '712345678',
                'description': 'test_payment',
            }
        )
        data = response.json()
        self.assertEqual(data['ResponseCode'], "0")
        self.assertEqual(data['ResponseDescription'], "Success. Request accepted for processing")
        self.assertEqual(data['CustomerMessage'], "Success. Request accepted for processing")

    def test_confirm_mpesa_stk_push_payment(self):
        response = self.client.post(
            path='http://localhost:3000/mpesa/confirm-stk-push-payment/',
            data={
                'checkoutRequestID': 'ws_CO_29042231104344781746'
            }
        )
        data = response.json()
        self.assertEqual(data['ResponseCode'], "0")
        self.assertEqual(data['ResponseDescription'], "The service request has been accepted successsfully")
        self.assertEqual(data['ResultCode'], "0")
        self.assertEqual(data['ResultDesc'], "The service request is processed successfully.")

    def test_callback_url(self):
        response = self.client.post(
            content_type='application/json',
            path='http://localhost:3000/mpesa/stk-push/callback/',
            data={
                'Body': {
                    'stkCallback': {
                        'MerchantRequestID': '1256-12654756-1',
                        'CheckoutRequestID': 'ws_CO_05052021143007860557',
                        'ResultCode': 0,
                        'ResultDesc': 'The service request is processed successfully.',
                        'CallbackMetadata': {
                            'Item': [
                                {'Name': 'Amount', 'Value': '1.0'},
                                {'Name': 'MpesaReceiptNumber', 'Value': 'PE52LJ8G4O'},
                                {'Name': 'TransactionDate', 'Value': 20210505143026},
                                {'Name': 'PhoneNumber', 'Value': '254712345678'}
                            ]
                        }

                    }
                }
            }
        )
        data = response.json()
        self.assertEqual(data['ResultCode'], 0)
        self.assertEqual(data['ResultDesc'], 'Success')

