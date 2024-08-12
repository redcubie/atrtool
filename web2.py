from pyscript import document, window
from js import jQuery
from pyodide.ffi.wrappers import add_event_listener

from atrtool import *

atr_obj: ATR


_updaters = []
def updater(selectors: list[str]) -> callable:
    """
    Decorator function to gather object update listeners.
    """
    def add_updater(func: callable):
        global _updaters

        _updaters.append({"func": func, "selectors": selectors})

        return func
    
    return add_updater

def apply_updaters():
    global _updaters

    for info in _updaters:
        selectors = info["selectors"]
        func = info["func"]

        for sel in selectors:
            el = document.querySelector(sel)
            add_event_listener(el, "change", func)


# call from all field update handlers after modifying data structure
def update_text():
    global atr_obj
    textbox = document.getElementById("hextext")

    data = atr_obj.to_bytes()

    textbox.value = data.hex()

from js import params_changed
def ui_update_all():
    global atr_obj
    ui_update_params()
    ui_update_hist()
    params_changed(None) # update baud display
    ui_update_protos()

def ui_update_params():
    global atr_obj
    
    el = document.querySelector("#bitorder")
    if atr_obj.TS.bitorder == TS.BitOrder.LSB_first:
        el.value = "normal"
    elif atr_obj.TS.bitorder == TS.BitOrder.MSB_first:
        el.value = "reverse"
    

    check_el = document.querySelector("#params_active")
    if "TA1" in atr_obj.params:
        check_el.checked = True
        inst = atr_obj.params["TA1"]

        Fi_el = document.querySelector("#params_Fi")
        Di_el = document.querySelector("#params_Di")

        Fi_el.value = inst.Fi
        Di_el.value = inst.Di
    else:
        check_el.checked = False
        pass # maybe reset data to default value
    jQuery("#params_active").trigger("change")


    check_el = document.querySelector("#egt_active")
    if "TC1" in atr_obj.params:
        check_el.checked = True
        inst = atr_obj.params["TC1"]

        data_el = document.querySelector("#egt")
        data_el.value = inst.N
    else:
        check_el.checked = False
        pass # maybe reset data to default value
    jQuery("#egt_active").trigger("change")
    

    check_el = document.querySelector("#negotiate_mode_active")
    if "TA2" in atr_obj.params:
        check_el.checked = True
        inst: TA2 = atr_obj.params["TA2"]

        nego_el = document.querySelector("#negotiate_mode")
        speed_el = document.querySelector("#use_speed_param")
        proto_el = document.querySelector("#preferred_proto")

        if inst.specific_mode:
            nego_el.value = "false"
        else:
            nego_el.value = "true"

        if inst.use_param:
            speed_el.value = "true"
        else:
            speed_el.value = "false"

        proto_el.value = inst.T
    else:
        check_el.checked = False
        pass # maybe reset data to default value
    jQuery("#negotiate_mode_active").trigger("change")


    # T=15 also defines global interface characteristics
    if 15 in atr_obj.protocols:
        prot = atr_obj.protocols[15]
        from atrtool.protocols import Teq15
        prot: Teq15

        check_el = document.querySelector("#clockstop_active")
        if prot.clock_stop is not None:
            check_el.checked = True

            clkstp_el = document.querySelector("#clockstop")
            clockstop = prot.clock_stop
            if clockstop == Teq15.ClockStop.NOT_SUPPORTED:
                clkstp_el.value = "none"
            elif clockstop == Teq15.ClockStop.STATE_H:
                clkstp_el.value = "high"
            elif clockstop == Teq15.ClockStop.STATE_L:
                clkstp_el.value = "low"
            elif clockstop == Teq15.ClockStop.NO_PREFERENCE:
                clkstp_el.value = "either"

            card_classes = prot.card_class
            a_el = document.querySelector("#class_a_enable")
            b_el = document.querySelector("#class_b_enable")
            c_el = document.querySelector("#class_c_enable")

            a_el.checked = Teq15.CardClass.CLASS_A in card_classes
            b_el.checked = Teq15.CardClass.CLASS_B in card_classes
            c_el.checked = Teq15.CardClass.CLASS_C in card_classes
        else:
            check_el.checked = False
            pass # maybe reset data to default value
        jQuery("#clockstop_active").trigger("change")

        # # for SPU byte
        # check_el = document.querySelector("#SPU_active")
        # if prot.card_class is not None:
        #     check_el.checked = True

        #     clock_el = document.querySelector("")
            
        # else:
        #     check_el.checked = False
        #     pass # maybe reset data to default value
        # jQuery("#SPU_active").trigger("change")

def ui_update_hist():
    global atr_obj

    data = atr_obj.hist_bytes
    check_el = document.querySelector("#hist_active")
    data_el = document.querySelector("#histtext")
    if data:
        check_el.checked = True
        data_el.value = data.hex()
    else:
        check_el.checked = False
        data_el.value = ""
    jQuery("#hist_active").trigger("change")

def ui_update_protos():
    global atr_obj

    things = [
        {"num": 0, "func": ui_update_proto_Teq0},
        {"num": 1, "func": ui_update_proto_Teq1},
    ]

    for info in things:
        num = info["num"]
        func = info["func"]
        check_sel = f"#Teq{num}_check"

        check_el = document.querySelector(check_sel)
        if num in atr_obj.protocols:
            check_el.checked = True
            func()
        else:
            check_el.checked = False

        jQuery(check_sel).trigger("change")

def ui_update_proto_Teq0():
    global atr_obj
    pass

def ui_update_proto_Teq1():
    global atr_obj
    pass


@updater(["#bitorder"])
def ui_rev_update_bitorder(event):
    global atr_obj
    el = document.querySelector("#bitorder")
    value = el.value

    if value == "normal":
        atr_obj.TS.bitorder = TS.BitOrder.LSB_first
    elif value == "reverse":
        atr_obj.TS.bitorder = TS.BitOrder.MSB_first

    update_text()

@updater(["#params_active", "#params_Fi", "#params_Di"])
def ui_rev_update_params(event):
    global atr_obj
    check_el = document.querySelector("#params_active")
    active = check_el.checked

    if active:
        Fi_el = document.querySelector("#params_Fi")
        Di_el = document.querySelector("#params_Di")

        Fi = int(Fi_el.value)
        Di = int(Di_el.value)

        obj = TA1()
        obj.Fi = Fi
        obj.Di = Di
        atr_obj.params["TA1"] = obj
    else:
        atr_obj.params.pop("TA1")

    update_text()

@updater(["#egt_active", "#egt"])
def ui_rev_update_params(event):
    global atr_obj
    check_el = document.querySelector("#egt_active")
    active = check_el.checked

    if active:
        el = document.querySelector("#egt")

        val = int(el.value)

        obj = TC1()
        obj.N = val
        # atr_obj.params.update({"TC1": obj})
        atr_obj.params["TC1"] = obj
    else:
        atr_obj.params.pop("TC1")

    update_text()

@updater(["#negotiate_mode_active", "#negotiate_mode", "#use_speed_param", "#preferred_proto"])
def ui_rev_update_negotiate(event):
    global atr_obj
    check_el = document.querySelector("#negotiate_mode_active")
    active = check_el.checked

    if active:
        nego_el = document.querySelector("#negotiate_mode")
        speed_el = document.querySelector("#use_speed_param")
        proto_el = document.querySelector("#preferred_proto")

        nego_val = bool(nego_el.value)
        speed_val = bool(speed_el.value)
        proto_val = int(proto_el.value)

        obj = TA2()
        obj.specific_mode = not nego_val
        obj.use_param = speed_val
        obj.T = proto_val
        atr_obj.params["TA2"] = obj
    else:
        atr_obj.params.pop("TA2")

    update_text()

@updater(["#clockstop_active", "#clockstop", "#class_a_enable", "#class_b_enable", "#class_c_enable"])
def ui_rev_update_Teq15(event):
    global atr_obj
    check_el = document.querySelector("#clockstop_active")
    active = check_el.checked

    if active:
        clkstp_el = document.querySelector("#clockstop")
        if clkstp_el.value == "none":
            clockstop = Teq15.ClockStop.NOT_SUPPORTED
        elif clkstp_el.value == "high":
            clockstop = Teq15.ClockStop.STATE_H
        elif clkstp_el.value == "low":
            clockstop = Teq15.ClockStop.STATE_L
        elif clkstp_el.value == "either":
            clockstop = Teq15.ClockStop.NO_PREFERENCE
        else:
            raise ValueError

        a_el = document.querySelector("#class_a_enable")
        b_el = document.querySelector("#class_b_enable")
        c_el = document.querySelector("#class_c_enable")

        card_classes = Teq15.CardClass(0)
        if a_el.checked:
            card_classes |= Teq15.CardClass.CLASS_A
        if b_el.checked:
            card_classes |= Teq15.CardClass.CLASS_B
        if c_el.checked:
            card_classes |= Teq15.CardClass.CLASS_C
        
        obj = Teq15()
        obj.clock_stop = clockstop
        obj.card_class = card_classes
        atr_obj.protocols[15] = obj
    else:
        atr_obj.protocols.pop(15)

    update_text()

@updater(["#hist_active", "#histtext"])
def ui_rev_update_hist(event):
    global atr_obj
    check_el = document.querySelector("#hist_active")
    active = check_el.checked

    if active:
        data_el = document.querySelector("#histtext")
        
        data = bytes.fromhex(data_el.value)

        atr_obj.hist_bytes = data
    else:
        atr_obj.hist_bytes = b''

    update_text()
