import urllib.request
import os
from urllib.parse import urlencode
from datetime import datetime, timedelta
import boto3
import json

def fetch_api(coin):
    base_url = 'https://api.coingecko.com/api/v3/coins/markets'

    params = {
        'vs_currency': 'brl',
        'ids': coin,
    }
    url = f"{base_url}?{urlencode(params)}"
    with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
    
    return data
    

def messages_transform(coin):
    coin = coin[0]
    name = coin['name']
    current_price = coin['current_price']
    high_24h = coin['high_24h']
    low_24h = coin['low_24h']
    last_updated = datetime.strptime(coin['last_updated'].split('.')[0], '%Y-%m-%dT%H:%M:%S') - timedelta(hours=3)

    return (
        f'Date: {last_updated}\n'
        f'Crypto name: {name}\n'
        f'Current price: {current_price}\n'
        f'Highest last 24h: {high_24h}\n'
        f'Lowest last 24h: {low_24h}'
    )

def lambda_handler(event, context):
    sns_topic_arn = os.getenv('SNS_TOPIC_ARN')
    sns_client = boto3.client('sns')

    coins_list = ['bitcoin', 'ethereum']
    message_list = []

    print('Fetching info')
    for coin in coins_list:
        try:
            response = fetch_api(coin)
            message_list.append(messages_transform(response))
        except Exception as e:
            print(f"Error fetching or processing data for {coin}: {e}")

    message_body = "\n\n".join(message_list)

    print('Sending SNS')

    try:
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=message_body,
            Subject='Crypto Notification'
        )
        print('SNS sent successfully')
    except Exception as e:
        print(f'Error sending SNS: {e}')
