/**
 * Created by matbur on 10.12.16.
 */

var num = $('#num');
var num_val = $('#num_val');
const hidden = 'hidden';
const max_move = 16;
var tab = [[], []];
var is_z = $('#is_z');
var value_pattern = /value="\d+"/;
var empty_value = 'value=""';

for (let i = 0; i < max_move; i++) {
    tab[0][i] = $('#0_' + i);
    tab[1][i] = $('#1_' + i);
}

$('.table0').removeClass(hidden);
var table1 = $('.table1');
is_z.change(function () {
    table1.toggleClass(hidden, !this.checked);
    if (!this.checked) {
        for (let i = 0; i < max_move; i++) {
            let c = tab[1][i].find("td:eq(2)");
            let content = c.html();
            c.html(content.replace(value_pattern, empty_value));
        }
    }
});

var previous = 0;
num.change(function () {
    let val = this.value;
    console.log(num_val.html());
    num_val.html(val);
    console.log(typeof  num_val.html());
    if (val < previous) {
        for (let i = val; i < max_move; i++) {
            let c = tab[0][i].find("td:eq(2)");
            let content = c.html();
            c.html(content.replace(value_pattern, empty_value));

            c = tab[1][i].find("td:eq(2)");
            content = c.html();
            c.html(content.replace(value_pattern, empty_value));
        }
    }
    let val_z0 = 0;
    for (let i = 0; i < max_move; i++) {
        let c = tab[0][i].find("td:eq(2)");
        let is_not_null = /value=.(\d+)./.exec(c.html()) !== null;
        if (is_not_null && i + 1 > val_z0) {
            val_z0 = i + 1;
        }
    }
    let val_z1 = 0;
    for (let i = 0; i < max_move; i++) {
        let c = tab[1][i].find("td:eq(2)");
        let is_not_null = /value=.(\d+)./.exec(c.html()) !== null;
        if (is_not_null && i + 1 > val_z1) {
            val_z1 = i + 1;
        }
    }
    if (val_z1 !== 0 && table1.hasClass(hidden)) {
        is_z.trigger('click');
    }
    let max = Math.max(val_z0, val_z1);
    if (max > val) {
        val = max;
        this.value = max;
    }

    for (let i = 0; i < val; i++) {
        tab[0][i].removeClass(hidden);
        tab[1][i].removeClass(hidden);
    }
    for (let i = val; i < max_move; i++) {
        tab[0][i].addClass(hidden);
        tab[1][i].addClass(hidden);
    }
    previous = val;
});

if (num.value === undefined) {
    num.trigger('change');
}

if (num_val.html() === '4') {
    num.trigger('change');
}

