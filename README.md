# Hello World Application

This repository is an example Hello World application.
It has already been submitted and is available in [App Store sandbox environment](https://app-sandbox.rebilly.com/app-store).
This readme describes how to submit and configure your own application.

## Structure

The application is an AWS Lambda function with two handlers:

+ `application_enabled`: handles webhooks when the app is installed.
+ `customer_created`: handles webhooks when new customers are added to users accounts in Rebilly.

When this app is installed, it provides discounts to new users.

## Configuration in Rebilly

1. Follow instructions to submit you application in [Rebilly App Store guide](https://www.rebilly.com/docs/content/concepts-and-features/tutorial/create-a-rebilly-app/#submit-an-app-to-the-app-store).
1. Deploy this Lambda function and receive an invocation URL.
1. In Rebilly, in the left navigation bar, click **Automations**, then click **Rules engine**.
1. Click **Core events**, and select the **Application instance enabled** event.
1. Click **Ruleset**, go to **Binds** tab, then click **Add Bind**. 
1. Complete all fields.
1. In the **Actions** section, click **Add action**, and select **Trigger webhook**.
1. Add your invocation URL. Ensure that the URL is in the following format: `https://your-api-name.execute-api.your-region.amazonaws.com/Prod/application-enabled`.
1. Click **Body**, and include an organization identifier of user who installed your app, using the following format: 
    ```json
    {"organizationId":  "{{organizationId}}"}
    ```

For more information on developing Rebilly apps, see [Rebilly App Store](https://www.rebilly.com/docs/content/concepts-and-features/app-store-grid).

## Develop and deploy

To develop, run, and deploy your own Lambda function, follow the [AWS SAM Reference](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-reference.html).
