# Hello World Application 

This repository is an example of application submitted to Rebilly App Store.
You can find this application in [Sandbox environment](https://app-sandbox.rebilly.com/).

The application consists of two Lambda functions:

+ `application_enabled` to handle webhooks when a new app is enabled
+ `customer_created` to handle webhook when a new customer is created

Keep in mind the app is just an example and doesn't have any input validation
to not overload the code.

## Test locally and deploy

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools:

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Python 3 installed](https://www.python.org/downloads/)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

### Deploy the lambda function

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build --use-container
sam deploy --guided
```

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

### Use the SAM CLI to build and test locally

Build your application with the `sam build --use-container` command.

```bash
hello-world-app$ sam build --use-container
hello-world-app$ sam local start-api
```
