from django.urls import path
from .views import GetMpesaOnlineTransaction, RequestMpesaSTKPushView, MpesaStkPushCallbackView

app_name = 'mpesa'

urlpatterns = [
    path('confirm-stk-push-payment/', GetMpesaOnlineTransaction.as_view(), name='confirm-mpesa-stk-push-payment'),
    path('request-stk-push/', RequestMpesaSTKPushView.as_view(), name='mpesa-stk-push'),
    path('stk-push/callback/', MpesaStkPushCallbackView.as_view(), name='mpesa-stk-push-callback'),
]
