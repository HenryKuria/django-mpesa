# Generated by Django 3.2 on 2021-04-30 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LipaNaMpesaOnlinePayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant_request_Id', models.CharField(max_length=250)),
                ('checkout_request_Id', models.CharField(max_length=250)),
                ('result_code', models.IntegerField()),
                ('result_description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='MpesaDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_url', models.URLField()),
                ('daraja_consumer_key', models.CharField(max_length=250)),
                ('daraja_consumer_secret', models.CharField(max_length=250)),
                ('mpesa_shortcode', models.CharField(max_length=250)),
                ('lipa_na_mpesa_online_passkey', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name_plural': 'Mpesa Details',
            },
        ),
        migrations.CreateModel(
            name='LipaNaMpesaOnlinePaymentCallbackMetadataItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('value', models.CharField(max_length=250)),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CallbackMetadataItems', to='mpesa.lipanampesaonlinepayment')),
            ],
        ),
    ]
