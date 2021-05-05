import json
from django.views import View
from django.db import IntegrityError
from django.http.response import JsonResponse
from .models import LipaNaMpesaOnlinePayment, LipaNaMpesaOnlinePaymentCallbackMetadataItem
from .daraja_functions import lipa_na_mpesa_online_payment, lipa_na_mpesa_online_query_request
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import STKPushForm, GetMpesaPaymentForm


class RequestMpesaSTKPushView(View):
    def post(self, request):
        form = STKPushForm(request.POST)
        if form.is_valid():
            response = json.loads(lipa_na_mpesa_online_payment(
                account_number=form.data['account_number'],
                amount=form.data['amount'],
                phone_number='254{}'.format(form.data['phone_number']),
                description=form.data['description']
            ).text)

            return JsonResponse(response)


@method_decorator(csrf_exempt, name='dispatch')
class MpesaStkPushCallbackView(View):

    def post(self, request):
        data = json.loads(request.body)['Body']['stkCallback']

        if data['ResultCode'] == 0:
            try:
                payment = LipaNaMpesaOnlinePayment.objects.create(
                    merchant_request_Id=data['MerchantRequestID'],
                    checkout_request_Id=data['CheckoutRequestID'],
                    result_code=data['ResultCode'],
                    result_description=data['ResultDesc']
                )
                callback_metadata = data['CallbackMetadata']
                items = [item for item in callback_metadata['Item']]
                for item in items:
                    new_metadata_item = LipaNaMpesaOnlinePaymentCallbackMetadataItem(
                        payment=payment,
                        name=item.get('Name'),
                        value=item.get('Value', '')
                    )
                    new_metadata_item.save()
            except IntegrityError:
                pass

        return JsonResponse({"ResultCode": 0, "ResultDesc": "Success", "ThirdPartyTransID": 0})


class GetMpesaOnlineTransaction(View):
    def post(self, request):
        form = GetMpesaPaymentForm(request.POST)

        if form.is_valid():
            checkout_request_id = form.data['checkoutRequestID']
            resp = lipa_na_mpesa_online_query_request(checkout_request_id).text
            resp = json.loads(resp)

            return JsonResponse(resp)

