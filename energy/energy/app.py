import json

# import requests

def lambda_handler(event, context):
    from_date = event['from_date']
    to_date = event['to_date']
    oil_type = event['oil_type']
    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "oil": "Brent",
                "price": 105.00, 
                # "location": ip.text.replace("\n", "")
            }
        ),
    }
