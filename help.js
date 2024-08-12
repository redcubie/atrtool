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


function onload() {
    populate_Fi();
    populate_Di();
}

$(window).on('load', onload);