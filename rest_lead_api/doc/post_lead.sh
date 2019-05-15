#!/usr/bin/env bash
curl    -X POST \
        -H 'API_KEY: 1234567890' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        'http://localhost:8069/v1/private/lead/create' \
        -d '{
             "name":"Quisiera informacion sobre el producto pepe",
             "street":"La calle donde vivo",
             "mobile":"4587 3369",
             "contact_name":"Juan Perez",
             "email_from":"juan.perez@gmail.com",
             "description":"Quiero que me contacten a mi telefono",
             "team_id":1
             }'
