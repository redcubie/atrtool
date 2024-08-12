const Fi_list =
    [
        { "val": 0b0000, "F": 372, "fmax": 4 },
        { "val": 0b0001, "F": 372, "fmax": 5 },
        { "val": 0b0010, "F": 558, "fmax": 6 },
        { "val": 0b0011, "F": 774, "fmax": 8 },
        { "val": 0b0100, "F": 1116, "fmax": 12 },
        { "val": 0b0101, "F": 1488, "fmax": 16 },
        { "val": 0b0110, "F": 1860, "fmax": 20 },
        { "val": 0b1001, "F": 512, "fmax": 5 },
        { "val": 0b1010, "F": 768, "fmax": 7.5 },
        { "val": 0b1011, "F": 1024, "fmax": 10 },
        { "val": 0b1100, "F": 1536, "fmax": 15 },
        { "val": 0b1101, "F": 2048, "fmax": 20 },
    ];

const Di_list =
    [
        { "val": 0b0001, "D": 1 },
        { "val": 0b0010, "D": 2 },
        { "val": 0b0011, "D": 4 },
        { "val": 0b0100, "D": 8 },
        { "val": 0b1000, "D": 12 },
        { "val": 0b0101, "D": 16 },
        { "val": 0b1001, "D": 20 },
        { "val": 0b0110, "D": 32 },
        { "val": 0b0111, "D": 64 },
    ];


function populate_Fi() {
    Fi_list.forEach((x) => {
        var select = document.getElementById("params_Fi");

        var text = `F=${x.F}, fmax=${x.fmax}MHz`;

        var el = document.createElement("option");
        el.value = x.val;
        el.innerText = text;

        select.appendChild(el);
    });
}

function populate_Di() {
    Di_list.forEach((x) => {
        var select = document.getElementById("params_Di");

        var text = `D=${x.D}`;

        var el = document.createElement("option");
        el.value = x.val;
        el.innerText = text;

        select.appendChild(el);
    });
}

function calc_baud(Fi, Di){
    var info1 = Fi_list.find((x) => (x.val == Fi));
    var info2 = Di_list.find((x) => (x.val == Di));

    var F = info1.F;
    var fmax = info1.fmax * 1e6;
    var D = info2.D;

    var baud = (fmax * D) / F;

    return baud.toFixed(0);
}

function params_changed(ev) {
    var Fi_el = document.getElementById("params_Fi");
    var Di_el = document.getElementById("params_Di");

    var Fi = Fi_el.value;
    var Di = Di_el.value;
    
    var maxbaud = calc_baud(Fi, Di);

    var text_el = document.getElementById("baud_text");
    text_el.innerText = `${maxbaud} bits/s max`;
}

function add_baud_calc() {
    var targets = ["#params_Fi", "#params_Di"];

    targets.forEach((x) => {
        $(x).on("change", params_changed).trigger("change");
    });
}

function add_enablers() {
    var enable_targets =
        [
            { "target": "#params_active", "text": ["#params_active~.form-check-label"], "inputs": ["#params_Fi", "#params_Di"] },
            { "target": "#egt_active", "text": ["#egt_active~.form-check-label"], "inputs": ["#egt"] },
            { "target": "#negotiate_mode_active", "text": ["#negotiate_mode_active~.form-check-label", "#use_speed_param_active~.form-check-label", "#preferred_proto_active~.form-check-label"], "inputs": ["#negotiate_mode", "#use_speed_param", "#preferred_proto"] },
            { "target": "#clockstop_active", "text": ["#clockstop_active~.form-check-label", "#class_active~.form-check-label"], "inputs": ["#clockstop", "#class_a_enable", "#class_b_enable", "#class_c_enable"] },
            { "target": "#hist_active", "text": ["#hist_active~.form-check-label"], "inputs": ["#histtext"] },
        ];

    var text_disable_class = "text-disable";

    enable_targets.forEach((x) => {
        $(x.target).on("change", (e) => {
            var active = e.target.checked;

            x.text.forEach((sel) => {
                var el = document.querySelector(sel);
                if (!active) {
                    el.classList.add(text_disable_class);
                }
                else {
                    el.classList.remove(text_disable_class);
                }
            });

            x.inputs.forEach((sel) => {
                var el = document.querySelector(sel);
                el.disabled = !active;
            });
        }).trigger("change");
    });
}


function onload() {
    populate_Fi();
    populate_Di();
    add_baud_calc();
    add_enablers();
}

$(window).on('load', onload);