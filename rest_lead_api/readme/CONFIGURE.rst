The api key and the user must be provided in the configuration file under
the section api_key_API_KEY. The key must be in the header of the REST request
and the user must exist in odoo and have the necessary permissions for the crm model.

in odoo.conf add for instance:

.. code-block:: ini

    [api_key_API_KEY]
    key=1234567890
    user=admin

in the REST request add the key in headers

.. code-block:: bash

    curl    -X GET \
            -H "API_KEY: 1234567890" \
            -H "accept: application/json" \
            "http://186.64.120.136:92/v1/private/team/search?name=dontcare"
