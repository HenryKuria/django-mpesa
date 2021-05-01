from django import forms


class STKPushForm(forms.Form):
    account_number = forms.CharField(label='paybill account number', max_length=250)
    amount = forms.CharField(label='amount to pay', max_length=250)
    phone_number = forms.CharField(label='phone number to send request', max_length=9)
    description = forms.CharField(label='Description of the payment', max_length=250)


class GetMpesaPaymentForm(forms.Form):
    checkoutRequestID = forms.CharField(label='checkout request id', max_length=250)

