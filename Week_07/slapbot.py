import slack
import pyjokes

oauth_token = "xoxb-1227345553298-1339454685137-UPiY420Y2fjYLlkTKo2Ek2FR"

client = slack.WebClient(token=oauth_token)
joke = pyjokes.get_joke()

response = client.chat_postMessage(channel='#random', text=f"Here is a Python joke: {joke}")