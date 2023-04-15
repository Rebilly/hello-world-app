import json
import os
from datetime import datetime, timedelta, timezone

import api_client

SELF_PATH = "/customer-created"


# Retrieve installed by an organization application instance details using your secret key
def _get_application_instance(organization_id):
    url = f"/applications/{os.environ.get('APPLICATION_ID')}/instances/{organization_id}"
    return api_client.get(url, secret_key=os.environ.get("SecretApiKey")).json()


# Retrieve application instance configuration
def _get_application_instance_configuration(token):
    url = f"/application-instances/{os.environ.get('APPLICATION_ID')}/configuration"
    return api_client.get(url, jwt=token).json()


def _redeem_coupon(token, customer_id, paid_by_time):
    url = "/coupons-redemptions"
    payload = {
        "couponId": os.environ.get('COUPON_ID'),
        "customerId": customer_id,
        "additionalRestrictions": [
            {
                "type": "paid-by-time",
                "time": paid_by_time.replace(tzinfo=timezone.utc).isoformat(timespec="seconds")
            }
        ]
    }
    api_client.post(url, payload, jwt=token)


def handler(event, context):
    organization_id = event["queryStringParameters"]["organizationId"]
    application_instance = _get_application_instance(organization_id)
    jwt = application_instance["token"]
    settings = _get_application_instance_configuration(jwt)['settings']
    customer_id = json.loads(event["body"])["customerId"]
    paid_by_time = datetime.now() + timedelta(days=settings["welcomeDays"])
    _redeem_coupon(jwt, customer_id, paid_by_time)
    return {"statusCode": 204, "body": None}
