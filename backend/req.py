import openai

openai.api_key = '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' # put in env later
language = "python3" # make way to choose language 
messages = [ {"role": "system", "content": "You are a helpful assistant who analyses code and provides meaningful feedback, the launguage used is" + language} ] 

while True:
    # ask user what language they're using
    message = input("Enter code to analyze: ") 
    if message == "-1": # exit 
        break
    if message: 
        messages.append( 
            {"role": "user", "content": message}, 
        ) 
        chat = openai.ChatCompletion.create( 
            model="gpt-3.5-turbo", max_tokens = 60, messages=messages
        ) 
    reply = chat.choices[0].message.content 
    print(reply) 
    messages.append({"role": "assistant", "content": reply}) 

    

