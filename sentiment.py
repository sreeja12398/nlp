import requests
from config2 import hf_sentiment_api
api_url="https://api-inference.huggingface.co/models/distilbert/distilbert-base-uncased-finetuned-sst-2-english"


headers= {
    "Authorization":f"Bearer {hf_sentiment_api}"
}

text= "I hate this movie it was horrible"

response= requests.post(api_url, headers=headers, json={"inputs": text})

if response.status_code==200:
    result=response.json()
    label=result[0][0]['label']
    score=result[0][0]['score']
    print(f"sentiment: {label} (confidence: {score:.2f})")
else: 
    print(f"Error {response.status_code}: {response.text}")
