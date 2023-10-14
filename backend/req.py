import openai

openai.api_key = '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' # put in env later

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
