=====
mpesa
=====

mpesa is a Django app to enable mpesa transactions on the web. Currently it features only the STK Push functionality.
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

5. Visit http://127.0.0.1:8000/polls/ to participate in the poll.
