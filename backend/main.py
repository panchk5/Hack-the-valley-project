# Import from standard library
import logging

# Import from 3rd party libraries
from taipy.gui import Gui, notify

# Import modules
import connect

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
    """Generate Explanation text."""
    state.Explanation = ""
    state.image = None

    # Check the number of requests done by the user
    if state.n_requests >= 5:
        error_too_many_requests(state)
        return

    # Check if the user has put a Language
    if state.Language == "":
        notify(state, "error", "Please enter a Language")
        return
    state.prompt = f"Explain the following {state.Language} code in simple language so someone without a coding background can understand it. {state.code}"


    # openai configured and check if text is flagged
    openai = connect.Openai()
    flagged = openai.moderate(state.prompt)
    
    if flagged:
        error_prompt_flagged(state, f"Prompt: {state.prompt}\n")
        return
    else:
        # Generate the Explanation
        state.n_requests += 1
        state.Explanation = (
            openai.complete(state.prompt).strip().replace('"', "")
        )

        # Notify the user in console and in the GUI
        logging.info(
            f"Language: {state.prompt}{state.code}\n"
            f"Explanation: {state.Explanation}"
        )
        notify(state, "success", "Explanation created!")
        
# Variables
Explanation = ""
rating = 0
prompt = ""
n_requests = 0

Language = "Python"
code = "x = 1"

image = None

# Called whever there is a problem
def on_exception(state, function_name: str, ex: Exception):
    logging.error(f"Problem {ex} \nin {function_name}")
    notify(state, 'error', f"Problem {ex} \nin {function_name}")

def generate_scalable_rating(state):
    """Generate Scalable Rating Score"""
    state.rating = ""

    # Check the number of requests done by the user
    if state.n_requests >= 5:
        error_too_many_requests(state)
        return
   
    state.prompt = f"Imagine you are a Senior Software developer and are doing some code reviews. Look at the code at the end and evaluate the scalability of the code from a scale of 1-100. Give it a score of 1-100 based on scalable you interpret the code as.{state.code}"
    # openai configured and check if text is flagged
    openai = connect.Openai()
    flagged = openai.moderate(state.prompt)
    
    if flagged:
        error_prompt_flagged(state, f"Prompt: {state.prompt}\n")
        return
    else:
        # Generate the Rating
        state.n_requests += 1

        state.rating = openai.complete(state.prompt)
        
        

        # Notify the user in console and in the GUI
        logging.info(
            f"Rating: {state.rating}\n"
        )
        notify(state, "success", "Rating created!")


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

This mini-app generates code Explanations using OpenAI's [Davinci model](https://beta.openai.com/docs/models/overview). Made for HTV 8. You can find the code on [GitHub](https://github.com/panchk5/Hack-the-valley-project).

<br/>

Made By: [Shashwat Murawala](https://www.linkedin.com/in/shashwatmurawala/), [Franklin Ramirez](https://www.linkedin.com/in/franklin-ramirez611/), [Krish Panchal](https://www.linkedin.com/in/panchk5/), and [Savvy Liu](https://www.linkedin.com/in/qi-liu-08556790/).

<br/>

<|layout|columns=1 1 1|gap=30px|class_name=card|
<Language|
## **Language**{: .color-primary}

<|{Language}|selector|lov={programming_languages}|dropdown|label=Language|>
|Language>
|>

<code|
## Enter **Code**{: .color-primary}

<|{code}|input|multiline|class_name=fullwidth|>
|code>

<|Generate text|button|on_action=generate_text|label= Sageify my code|>
<|Generate Rating|button|on_action=generate_scalable_rating|label=Generate Rating|>

<br/>

---

<br/>

### Generated **Explanation**{: .color-primary}

<|{Explanation}|input|multiline|label=Resulting Explanation|class_name=fullwidth|>

### Generated **Scalability Rating**{: .color-primary}

<|{rating}|input|multiline|label=Scalability Rating|class_name=fullwidth|>

"""


if __name__ == "__main__":
    Gui(page).run(title='ScriptSage')