GET THE SALES TEAMS AVAILABLE TO CREATE LEADS

NOTE: The name parameter is irrelevant

.. code-block:: bash

    curl    -X GET \
            -H "API_KEY: 1234567890" \
            -H "accept: application/json" \
            "http://186.64.120.136:92/v1/private/team/search?name=dontcare"

CREATE A LEAD IN THE CRM.LEAD MODEL

Fields description:

- name : Text: Required: Short requirement description
- street: Text: Prospect Address
- mobile: Text: Prospect Mobile
- contact_name: Text: Required: Prospect Full Name
- email_from: Text: Required: Prospect Email
- description: Text: Long description of the requirement
- team_id: Integer: Required: Sales Channel ID

.. code-block:: bash

    curl    -X POST \
            -H 'API_KEY: 1234567890' \
            -H 'accept: application/json' \
            -H 'Content-Type: application/json' \
            'http://186.64.120.136:92/v1/private/lead/create' \
            -d '{
                 "name":"I wanted information about xxxx product",
                 "street":"742 Evergreen Terrace, Springfield",
                 "mobile":"1 (971) 762-1052",
                 "contact_name":"Marsh Simpson",
                 "email_from":"michi1234@crostyburg.com",
                 "description":"Wanna have a call with a handsome salesman",
                 "team_id":1
                 }'

SEARCH LEADS BY A PORTION OF NAME

In this example we get all the leads with the word "Need" in the name

.. code-block:: bash

    curl    -X GET \
            -H 'API_KEY: 1234567890' \
            -H "accept: application/json" \
            "http://186.64.120.136:92/v1/private/lead/search?name=Need"

GET ALL SALES TEAMS

.. code-block:: bash

    curl    -X GET \
            -H 'API_KEY: 1234567890' \
            -H "accept: application/json" \
            "http://186.64.120.136:92/v1/private/team/search?name=dontcare"

GET A LEAD BY ID

In this example we get the lead with id=10

.. code-block:: bash

    curl    -X GET \
            -H 'API_KEY: 1234567890' \
            -H "accept: application/json" \
            "http://186.64.120.136:92/v1/private/lead/10/get"
