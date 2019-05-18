The api key and the user must be provided in the configuration file.
And this key must be in the header of the REST request the user must exist in
odoo and have the necessary permissions for the crm model.

In odoo.conf add for instance:

.. code-block:: ini

    rest_api_key = 1234567890
    rest_api_user = admin

In the REST request add the key in headers.

.. code-block:: bash

    curl    -X GET \
            -H "API_KEY: 1234567890" \
            -H "accept: application/json" \
            "http://186.64.120.136:92/v1/private/team/search?name=dontcare"
