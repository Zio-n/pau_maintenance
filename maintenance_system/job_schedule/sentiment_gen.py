from transformers import pipeline

def get_sentiment(text):
    sentiment_model = pipeline("sentiment-analysis")
    return sentiment_model(text)[0]['label']


