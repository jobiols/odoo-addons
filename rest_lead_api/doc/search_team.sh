#!/usr/bin/env bash
curl    -X GET \
        -H 'API_KEY: 1234567890' \
        -H "accept: application/json" \
        "http://localhost:8069/lead/v1/private/team/search?name=dontcare"
