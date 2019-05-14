#!/usr/bin/env bash
curl    -X POST \
        -H 'API_KEY: 1234567890' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        'http://localhost:8069/lead/v1/private/lead/create' \
        -d '{"name":"otro lead",
             "street":"La calle donde vivo",
             "mobile":"4587 3369",
             "contact_name":"Juan Perez",
             "email_from":"juan.perez@gmail.com",
             "description":"Me interesa el producto pirulo, contactenme"}'
