$('#mselect').multiselect({
    searchField: false,
    splitRatio: 0.5,
    availableListPosition: 'left',
});

var click_lock = false;
setTimeout(
    (function() {
        $('.option-element').click(function (e) {
            if (click_lock) {
                return;
            }
            click_lock = true;
            var elems = document.getElementsByClassName('option-element');
            var switch_after = false;
            var switch_batch = false;
            var elems_to_click = [];
            for (var i=0; i<elems.length; i++) {
                if (switch_after && switch_batch === elems[i].classList.contains('option-selected')) {
                    elems_to_click.push(elems[i]);
                }
                if (elems[i] === this) {
                    switch_after = true;
                    switch_batch = elems[i].classList.contains('option-selected');
                }
            }
            for (i=elems_to_click.length-1; i>=0; i--) {
                elems_to_click[i].click();
            }
            click_lock = false;
        });
    }),
    10 // Fuck javascript and fuck javascript widgets
);


document.getElementById('submit').onclick = function() {
    var move_elems = document.getElementsByClassName('option-selected');
    var move_ids = [];
    for (var i=0; i<move_elems.length; i++) {
        move_ids.push(move_elems[i].innerText.trim());
    }
    var req = new XMLHttpRequest();
    req.open('POST', '/page/rechapter_target');
    req.setRequestHeader('Content-Type', 'Application/JSON');
    req.send(JSON.stringify({
        manga_id: document.getElementById('manga_id').value,
        name: document.getElementById('name').value,
        sort_key: document.getElementById('sort_key').value,
        page_ids: move_ids
    }));
};
