#!/usr/bin/env bash
curl    -X POST \
        -H 'API_KEY: 1234567890' \
        -H "accept: application/json" \
        -H "Content-Type: application/json" \
        "http://localhost:8069/lead/v1/private/partner/create" \
        -d "{\"zip\":\"123\",\"street\":\"calle donde vive\",\"state\":{\"id\":0,\"name\":\"string\"},\"phone\":\"string\",\"name\":\"string\",\"street2\":\"string\",\"city\":\"string\",\"country\":{\"id\":0,\"name\":\"string\"},\"is_company\":true}"
