import openai

openai.api_key = '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' # put in env later
language = "python3" # make way to choose language using a menu or something
messages = [ {"role": "system", "content": "You are a helpful assistant who explains what the code is doing, do not provide feedback, the launguage used is" + language} ] 

while True:
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

    

