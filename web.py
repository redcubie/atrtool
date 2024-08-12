from pyscript import window,document

from atrtool import *
from web2 import *
import web2

import traceback

def validate_text(event = None):
    global atr_obj
    textbox = document.getElementById("hextext")
    text_data = textbox.value

    char_error = False
    try:
        bdata = bytes.fromhex(text_data)
    except:
        char_error = True
    
    if char_error:
        textbox.classList.add("text-danger")
        textbox.classList.remove("text-bg-warning")
        return
    else:
        textbox.classList.remove("text-danger")
    
    parse_error = False
    try:
        web2.atr_obj = ATR.from_bytes(bdata)
        ui_update_all()
    except:
        window.console.error(traceback.format_exc())
        parse_error = True
    
    if parse_error:
        textbox.classList.add("text-bg-warning")
    else:
        textbox.classList.remove("text-bg-warning")


validate_text() # reset all fields based on default text

#loading finished
from js import hideLoadingModal
hideLoadingModal()
