import json
import os
from urllib.parse import urlparse

import api_client
import customer_created


# Retrieve installed by an organization application instance details using your secret key
def _get_application_instance(organization_id):
    url = f"/applications/{os.environ.get('APPLICATION_ID')}/instances/{organization_id}"

    return api_client.get(url, secret_key=os.environ.get("SECRET_API_KEY")).json()


# Create default coupon to redeem when a new customer is created
def _create_coupon(token, amount):
    url = f"/coupons/{os.environ.get('COUPON_ID')}"
    payload = {
        "discount": {
            "type": "fixed",
            "amount": amount,
            "currency": "USD"
        },
        "restrictions": [
            {
                "type": "redemptions-per-customer",
                "quantity": 1
            }
        ],
        "description": "This coupon is a welcome coupon for every new user",
        "issuedTime": "2021-01-01T00:00:00Z",
        "expiredTime": None
    }
    api_client.put(url, payload, jwt=token)


# Parse event request context to retrieve host and path of the lambda function to route webhooks on it
def _get_customer_created_webhook_url(event):
    request_context = event["requestContext"]
    return "https://" + request_context["domainName"] + \
           str(request_context["path"]).replace(request_context["resourcePath"], customer_created.SELF_PATH)


# Add webhook subscriber to receive webhooks when a new customer is created
def _create_webhook_subscriber(token, organization_id, customer_created_handler_url):
    host = urlparse(customer_created_handler_url).netloc
    url = "/credential-hashes/webhooks"
    payload = {
        "host": host,
        "auth": {
            "type": "none"  # Consider to use authentication for your real webhooks
        }
    }
    credential_hash = api_client.post(url, payload, jwt=token).json()

    url = "/webhooks"
    payload = {
        "method": "POST",
        "url": f"{customer_created_handler_url}?organizationId={organization_id}",
        "credentialHash": credential_hash['hash'],
        "status": "active",
        "eventsFilter": ["customer-created"]
    }
    api_client.post(url, payload, jwt=token)


# Entrypoint of a function to handle `application-installed` event
def handler(event, context):
    # Parse webhook data
    webhook_data = json.loads(event["body"])
    organization_id = webhook_data["organizationId"].strip()

    # Retrieve application instance"s JWT token to perform API calls on behalf of an organization that installed the app
    application_instance = _get_application_instance(organization_id)
    jwt = application_instance["token"]

    # Subscribe for `customer-created` event
    _create_webhook_subscriber(jwt, organization_id, _get_customer_created_webhook_url(event))

    # Create coupon
    _create_coupon(jwt, application_instance["settings"]["welcomeAmount"])

    return {"statusCode": 204, "body": None}
