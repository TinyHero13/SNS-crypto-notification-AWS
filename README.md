# Crypto Notifier on AWS

This project implements a **cryptocurrency notifier** using various AWS services, focusing on automation and scalability. The main flow consists of a Lambda function that, every 2 hours, makes a request to the CoinGecko API to obtain cryptocurrency data and then sends that data via email using Amazon SNS.

## Project Architecture
![Project Architecture](/imgs/arq.png)

The architecture consists of:
- **AWS Lambda**: to execute the code.
- **Amazon EventBridge**: to schedule and trigger the Lambda function every 2 hours.
- **CoinGecko API**: to obtain cryptocurrency data.
- **Amazon SNS**: to send notifications via email.

## Features
- **Connection with CoinGecko API**: The Lambda function makes requests to the CoinGecko API to obtain cryptocurrency information.
- **Scheduling with Amazon EventBridge**: The Lambda function is executed automatically every 2 hours.
- **Sending emails via Amazon SNS**: After the Lambda function runs, cryptocurrency information is sent via email.

## Technologies Used
- **AWS Lambda**: Serverless computing service that lets you run code in response to events.
- **Python**: The language used to write the Lambda function that interacts with the CoinGecko API and sends data via SNS.
- **Amazon EventBridge**: Event bus service that allows scheduling and triggering events, such as the execution of the Lambda function.
- **Amazon SNS**: Notification service that sends messages (like emails) in response to events.
- **IAM**: Identity and Access Management service used to grant permissions to the Lambda function.

## How to Set Up the Project

### 1. Create an AWS Account
First, you will need to create an AWS account to access and use the platform's services. If you already have an account, simply log in.

### 2. Create an SNS Topic
1. Access the **SNS** service on AWS and create a new "Standard" topic, which allows sending notifications via SMS, email, or HTTP.
2. Give your topic a name and then create a **subscription** for that topic by entering an email of your choice.
3. After creating the topic and subscribing, the system will send an email to the provided address. You will need to confirm the subscription.

### 3. Create Role and Policy in IAM
For AWS Lambda to publish messages to SNS, you will need to create a **policy** that grants this access.

1. Create a policy in IAM with the following content, replacing `YOUR_SNS_ARN` with the ARN of your SNS topic:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sns:Publish",
            "Resource": "YOUR_SNS_ARN"
        }
    ]
}
```
   
Then, create a role for Lambda and attach the created policy, along with the AWSLambdaBasicExecutionRole, which is required to grant execution permission to the Lambda function.

### 4. Create the Lambda
Access the Lambda service and create a new function.
During setup, in the "Change execution role" option, choose the role you created earlier.
Use Python or another language to extract the desired data from the CoinGecko API (see the code example below for reference).
Test the function to ensure it is working correctly.

### 5. Configure Amazon EventBridge
In Amazon EventBridge, create a new rule with the cron expression `0 */2 * * ? *`, which will schedule the Lambda function to run every 2 hours.

To understand more about cron expressions, I recommend the site [CronTabGuru](https://crontab.guru).

Choose AWS Lambda as the target for the rule and select the Lambda function you created.
After configuration, the Lambda function will run automatically every 2 hours.

With these steps, the cryptocurrency notifier will be ready to run automatically every 2 hours, sending cryptocurrency market information to your email via SNS.
