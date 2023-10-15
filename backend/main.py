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
    state.image = None

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
        
# Variables
Explaination = ""
prompt = ""
n_requests = 0

Language = "Python"
style = "x = 1"

image = None

# Called whever there is a problem
def on_exception(state, function_name: str, ex: Exception):
    logging.error(f"Problem {ex} \nin {function_name}")
    notify(state, 'error', f"Problem {ex} \nin {function_name}")


# Markdown for the entire page
## <text|
## |text> 
## "text" here is just a name given to my part/my section
## it has no meaning in the code

programming_languages = [
    'Ada', 'ALGOL', 'Assembly Language', 'Bash', 'C', 'C#', 'C++', 'Clojure', 'COBOL', 'CoffeeScript',
    'Crystal', 'D', 'Dart', 'Elixir', 'Elm', 'Erlang', 'F#', 'Fortran', 'Go', 'Groovy',
    'Haskell', 'HTML/CSS', 'Java', 'JavaScript', 'Julia', 'Kotlin', 'Lisp', 'Lua', 'MATLAB', 'Objective-C',
    'Pascal', 'Perl', 'PHP', 'Prolog', 'Python', 'R', 'Ruby', 'Rust', 'Scala', 'Scheme', 'Shell',
    'SQL', 'Swift', 'TypeScript', 'VB.NET', 'Visual Basic', 'VHDL', 'Verilog', 'VHDL', 'XML'
]


page = """
<|container|
# **Script**{: .color-primary} Sage

This mini-app generates code explainations using OpenAI's [Davinci model](https://beta.openai.com/docs/models/overview). Made for HTV 8. You can find the code on [GitHub](https://github.com/panchk5/Hack-the-valley-project).

<br/>

Made By: [Shashwat Murawala](https://www.linkedin.com/in/shashwatmurawala/), [Franklin Ramirez](https://www.linkedin.com/in/franklin-ramirez611/), [Krish Panchal](https://www.linkedin.com/in/panchk5/), and [Savvy Liu](https://www.linkedin.com/in/qi-liu-08556790/).

<br/>

<|layout|columns=1 1 1|gap=30px|class_name=card|
<Language|
## **Language**{: .color-primary}

<|{Language}|selector|lov={programming_languages}|dropdown|label=Language|>
|Language>
|>

<style|
## Enter **Code**{: .color-primary}

<|{style}|input|multiline|class_name=fullwidth|>
|style>

<|Generate text|button|on_action=generate_text|label= Sageify my code|>

<br/>

---

<br/>

### Generated **Explaination**{: .color-primary}

<|{Explaination}|input|multiline|label=Resulting Explaination|class_name=fullwidth|>

"""


if __name__ == "__main__":
    Gui(page).run(title='Explaination Generation')