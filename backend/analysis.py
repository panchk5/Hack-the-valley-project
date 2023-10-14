# import openai
from decouple import config
import openai
API_KEY = config('API_KEY_1')

openai.api_key = API_KEY # API_KEY_1 is the key for the GPT-3.5-turbo model

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant who analyses code and provides meaningful feedback"}, 
        {"role": "user", "content": "print(hello world)"},
        # {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        # {"role": "user", "content": "Where was it played?"}
    ]
)
response_message = response["choices"][0]["message"]
print(response_message)
