from django.db import models
from django.core.exceptions import ValidationError


class MpesaDetails(models.Model):
    site_url = models.URLField(blank=False, null=False,
                               help_text="enter your site full url without '/' at the end. Example: https://mysite.com")
    daraja_consumer_key = models.CharField(max_length=250, blank=False, null=False)
    daraja_consumer_secret = models.CharField(max_length=250, blank=False, null=False)
    mpesa_shortcode = models.CharField(max_length=250, blank=False, null=False)
    lipa_na_mpesa_online_passkey = models.CharField(max_length=250, blank=False, null=False)

    class Meta:
        verbose_name_plural = 'Mpesa Details'

    def clean(self):
        """
        Throw ValidationError if you try to save more than one model instance
        """
        model = self.__class__
        if model.objects.count() > 0 and self.id != model.objects.get().id:
            raise ValidationError(
                "Can only create 1 instance of {}.".format(model.__name__))

    def __str__(self):
        return self.site_url


class LipaNaMpesaOnlinePayment(models.Model):
    merchant_request_Id = models.CharField(max_length=250, blank=False, null=False)
    checkout_request_Id = models.CharField(max_length=250, blank=False, null=False, unique=True)
    result_code = models.IntegerField(blank=False)
    result_description = models.TextField(blank=False)

    @property
    def success(self):
        if self.CallbackMetadataItems.count() > 0:
            return True
        return False

    def __str__(self):
        return self.checkout_request_Id


class LipaNaMpesaOnlinePaymentCallbackMetadataItem(models.Model):
    payment = models.ForeignKey(LipaNaMpesaOnlinePayment, on_delete=models.CASCADE,
                                related_name='CallbackMetadataItems')
    name = models.CharField(blank=False, max_length=250)
    value = models.CharField(blank=False, max_length=250)