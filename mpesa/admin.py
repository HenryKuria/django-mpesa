from django.contrib import admin
from .models import MpesaDetails, LipaNaMpesaOnlinePayment, LipaNaMpesaOnlinePaymentCallbackMetadataItem


class MpesaDetailsAdmin(admin.ModelAdmin):
    """
    Don't allow addition of more than one model instance in Django admin
    """
    def has_add_permission(self, request):
        if self.model.objects.count() > 0:
            return False
        else:
            return True


admin.site.register(MpesaDetails, MpesaDetailsAdmin)
admin.site.register(LipaNaMpesaOnlinePayment)
admin.site.register(LipaNaMpesaOnlinePaymentCallbackMetadataItem)

