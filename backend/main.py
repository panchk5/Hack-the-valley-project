# Import from standard library
import logging
import random
import re

# Import from 3rd party libraries
from taipy.gui import Gui, notify

# Import modules
import oai

# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)

def error_prompt_flagged(state, prompt):
    """Notify user that a prompt has been flagged."""
    notify(state, "error", "Prompt flagged as inappropriate.")
    logging.info(f"Prompt flagged as inappropriate: {prompt}")

def error_too_many_requests(state):
    """Notify user that too many requests have been made."""
    notify(state, "error", "Too many requests. Please wait a few seconds before generating another text or image.")
    logging.info(f"Session request limit reached: {state.n_requests}")
    state.n_requests = 1


# Define functions 
def generate_text(state):
    """Generate Explaination text."""
    state.Explaination = ""
    # state.image = None

    # Check the number of requests done by the user
    if state.n_requests >= 5:
        error_too_many_requests(state)
        return

    # Check if the user has put a Language
    if state.Language == "":
        notify(state, "error", "Please enter a Language")
        return
   
    state.prompt = f"Explain the following {state.Language} code in simple language so someone without a coding background can understand it. {state.style}"


    # openai configured and check if text is flagged
    openai = oai.Openai()
    flagged = openai.moderate(state.prompt)
    
    if flagged:
        error_prompt_flagged(state, f"Prompt: {state.prompt}\n")
        return
    else:
        # Generate the Explaination
        state.n_requests += 1
        state.Explaination = (
            openai.complete(state.prompt).strip().replace('"', "")
        )

        # Notify the user in console and in the GUI
        logging.info(
            f"Language: {state.prompt}{state.style}\n"
            f"Explaination: {state.Explaination}"
        )
        notify(state, "success", "Explaination created!")

def generate_scalable_rating(state):
    """Generate Scalable Rating Score"""
    state.rating = ""

    # Check the number of requests done by the user
    if state.n_requests >= 5:
        error_too_many_requests(state)
        return
   
    state.prompt = f"Imagine you are a Senior Software developer and are doing some code reviews. Look at the following {state.Language} and evaluate the scalability of the code from a scale of 1-100. Give it a score of 1-100 based on scalable you interpret the code as."
    # openai configured and check if text is flagged
    openai = oai.Openai()
    flagged = openai.moderate(state.prompt)
    
    if flagged:
        error_prompt_flagged(state, f"Prompt: {state.prompt}\n")
        return
    else:
        # Generate the Rating
        state.n_requests += 1

        try:
            state.rating = float(openai.complete(state.prompt))
        except ValueError:
            # Handle the case where the response is not a valid number
            state.rating = 0  # You can set it to None or another default value
        

        # Notify the user in console and in the GUI
        logging.info(
            f"Rating: {state.rating}\n"
        )
        notify(state, "success", "Rating created!")


# def generate_image(state):
#     """Generate Explaination image."""
#     notify(state, "info", "Generating image...")

#     # Check the number of requests done by the user
#     if state.n_requests >= 5:
#         error_too_many_requests(state)
#         return

#     state.image = None

#     # Creates the prompt
#     prompt_wo_hashtags = re.sub("#[A-Za-z0-9_]+", "", state.prompt)
#     processing_prompt = (
#         "Create a detailed but brief description of an image that captures "
#         f"the essence of the following text:\n{prompt_wo_hashtags}\n\n"
#     )

#     # Openai configured and check if text is flagged
#     openai = oai.Openai()
#     flagged = openai.moderate(processing_prompt)

#     if flagged:
#         error_prompt_flagged(state, processing_prompt)
#         return
#     else:
#         state.n_requests += 1
#         # Generate the prompt that will create the image
#         processed_prompt = (
#             openai.complete(
#                 prompt=processing_prompt, temperature=0.5, max_tokens = 1000
#             )
#             .strip()
#             .replace('"', "")
#             .split(".")[0]
#             + "."
#         )

#         # Generate the image
#         state.image = openai.image(processed_prompt)

#         # Notify the user in console and in the GUI
#         logging.info(f"Explaination: {state.prompt}\nImage prompt: {processed_prompt}")
#         notify(state, "success", f"Image created!")


# Variables
Explaination = ""
rating = 0
prompt = ""
n_requests = 0

Language = "Python"
style = "x = 1"

# image = None

# Called whever there is a problem
def on_exception(state, function_name: str, ex: Exception):
    logging.error(f"Problem {ex} \nin {function_name}")
    notify(state, 'error', f"Problem {ex} \nin {function_name}")


# Markdown for the entire page
## <text|
## |text> 
## "text" here is just a name given to my part/my section
## it has no meaning in the code
page = """
<|container|>
# **Generate**{: .color-primary} Explanations

This mini-app generates Explainations using OpenAI's GPT-3 based [Davinci model](https://beta.openai.com/docs/models/overview) for texts and [DALL·E](https://beta.openai.com/docs/guides/images) for images. You can find the code on [GitHub](https://github.com/Avaiga/demo-Explaination-generation) and the original author on [Code_Explaination](https://Code_Explaination.com/kinosal).

<br/>

<|layout|columns=1 1 1|gap=30px|class_name=card|
<Language|
## **Language**{: .color-primary}

<|{Language}|input|label=Language|>
|Language>

<style|
## Enter **Code**{: .color-primary}

<|{style}|input|multiline|label=Code_Explaination account handle to style-copy recent Explainations (optional)|>
|style>

<|Generate text|button|on_action=generate_text|label=Generate text|>
|>

<br/>

---

<br/>

### Generated **Explanation**{: .color-primary}

<|{Explaination}|input|multiline|label=Resulting Explaination|class_name=fullwidth|>

### Generated **Scalability Rating**{: .color-primary}

rating = [(0,{rating})]
data = pandas.DataFrame(rating, columns= [Scalability Rating, "1-100"])

<|{data}|chart|type=bar|x=Scalability Rating|y=1-100|>

"""

if __name__ == "__main__":
    Gui(page).run(title='Explaination Generation')
