from taipy import Gui

excitement_page = """
# The Council
## 
### How excited are you ffffto try Taipy? 

<|{excitement}|slider|min=1|max=100|>

My excitement level: <|{excitement}|text|>
"""
excitement = 100

Gui(page=excitement_page).run(use_reloader=True)