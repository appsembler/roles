#!/bin/bash
echo "$CERTBOT_VALIDATION" > {{ letsencrypt_webroot }}/{{ letsencrypt_alternative_acme_folder }}/"$CERTBOT_TOKEN"
