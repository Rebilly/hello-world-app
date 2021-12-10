# Hello World Application

This repository is an example of Hello World application submitted to Rebilly App Store. You can find it
in [Sandbox environment](https://app-sandbox.rebilly.com/).

## Structure of the application

The application is a Lambda function with two handlers:

+ `application_enabled` to handle webhooks when app installed
+ `customer_created` to handle webhooks when new customers created in users accounts

## Configuration in Rebilly

* Follow instructions to submit you application
  in [Rebilly App Store guide](https://www.rebilly.com/docs/content/concepts-and-features/app-store-grid).
* Deploy this Lambda function to get invocation url.
* Configure a bind in rules engine when an *Application instance enabled* event occurs to send a webhook to the
  invocation url you got plus the `application_enabled` handler path. The webhook url must then look
  like `https://your-api-name.execute-api.your-region.amazonaws.com/Prod/application-enabled`.
* Configure the webhook body to include an identifier of organization where your app installed:
    ```json
    {"organizationId":  "{{organizationId}}"}
    ```

When a user installs your application, the event occurs, and the webhook sends. Application receives the webhook and
subscribes itself to receive webhooks when a new customer created. You can change this part to execute the logic you
need.

## Develop and deploy

Follow [AWS SAM Reference](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-reference.html)
to develop, run and deploy your Lambda function.