import json
import os
from datetime import datetime, timedelta, timezone

import api_client

SELF_PATH = "/customer-created"


# Retrieve installed by an organization application instance details using your secret key
def _get_application_instance(organization_id):
    url = f"/applications/{os.environ.get('APPLICATION_ID')}/instances/{organization_id}"
    return api_client.get(url, secret_key=os.environ.get("SECRET_API_KEY")).json()


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
    customer_id = json.loads(event["body"])["customerId"]
    paid_by_time = datetime.now() + timedelta(days=application_instance["settings"]["welcomeDays"])
    _redeem_coupon(application_instance["token"], customer_id, paid_by_time)

    return {"statusCode": 204, "body": None}
