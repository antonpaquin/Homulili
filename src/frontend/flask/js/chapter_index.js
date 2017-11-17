function do_delete(elem, chapter_id) {
    var button = elem.children[0];
    var confirm = elem.children[1];

    elem.classList.add("focus");

    confirm.onclick = function() {
        confirm.setAttribute('onclick', null);
        elem.setAttribute('onclick', null);
        confirm.setAttribute('onblur', null);

        button.value = "Deleting...";

        elem.classList.remove("focus");

        var req = new XMLHttpRequest();
        req.open('GET', '/chapter/delete_target?chapter_id=' + chapter_id);
        req.onload = function() {
            finish_delete(elem, chapter_id);
        };
        req.send();
    };

    confirm.onblur = function () {
        confirm.setAttribute('onclick', null);
        elem.classList.remove("focus");
    };
}

function finish_delete(elem, chapter_id) {
    var button = elem.children[0];
    var confirm = elem.children[1];
    var row = elem.parentElement.parentElement;

    row.classList.add('deleted');

    button.value = "Deleted";

    var btn_rename = document.getElementById('btn-rename-' + chapter_id);
    var btn_resort = document.getElementById('btn-resort-' + chapter_id);
    btn_rename.setAttribute('onclick', null);
    btn_resort.setAttribute('onclick', null);
}

function do_rename(elem, chapter_id) {
    var button = elem.children[0];
    var text = elem.children[1];

    elem.classList.add("focus");

    text.onkeydown = function() {
        if (!(event.key === 'Enter')) {
            return;
        }

        var name = text.value;

        button.value = "Processing...";

        elem.classList.remove("focus");

        console.log('Do send rename request ' + chapter_id + ' ' + name);
        var req = new XMLHttpRequest();
        req.open('GET', '/chapter/rename_target?chapter_id=' + chapter_id + '&name=' + name);
        req.onload = function() {
            finish_rename(elem, chapter_id, name);
        };
        req.send();
    };

    text.onblur = function () {
        text.setAttribute('onkeydown', null);
        elem.classList.remove("focus");
    };
}

function finish_rename(elem, chapter_id, name) {
    var button = elem.children[0];
    var text = elem.children[1];
    var name_field = document.getElementById("chapter-link-" + chapter_id);

    button.value = "Rename";
    name_field.innerText = name;
}

function do_resort(elem, chapter_id) {
    var button = elem.children[0];
    var sort_inp = elem.children[1];

    elem.classList.add("focus");

    sort_inp.onblur = function() {
        elem.classList.remove("focus");
    };

    sort_inp.onkeydown = function() {
        if (!(event.key === 'Enter')) {
            return;
        }

        var sort_key = sort_inp.value;
        button.value = "Processing...";

        elem.classList.remove("focus");

        console.log('Do send resort ' + chapter_id + ' ' + sort_key);
        var req = new XMLHttpRequest();
        req.open('GET', '/chapter/resort_target?chapter_id=' + chapter_id + '&sort_key=' + name);
        req.onload = function() {
            finish_resort(elem, chapter_id, sort_key);
        };
        req.send();
    }
}

function finish_resort(elem, chapter_id, sort_key) {
    var button = elem.children[0];
    var text = elem.children[1];
    var sort_field = document.getElementById("chapter-sortkey-" + chapter_id);

    button.value = "Resort";
    sort_field.innerText = sort_key;
}


(function() {
    for (var ii=0; ii<chapter_ids.length; ii++) {
        var chapter_id = chapter_ids[ii];
        var btn_delete = document.getElementById('btn-delete-' + chapter_id);
        var btn_rename = document.getElementById('btn-rename-' + chapter_id);
        var btn_resort = document.getElementById('btn-resort-' + chapter_id);
        // Holy shit javascript I feel like barfing
        // This is an abomination of a construct
        btn_delete.onclick = (function(elem, chapter_id) {
            return function() {
                do_delete(elem, chapter_id);
            };
        })(btn_delete, chapter_id);
        btn_rename.onclick = (function(elem, chapter_id) {
            return function() {
                do_rename(elem, chapter_id);
            }
        })(btn_rename, chapter_id);
        btn_resort.onclick = (function(elem, chapter_id) {
            return function() {
                do_resort(elem, chapter_id);
            }
        })(btn_resort, chapter_id);
    }
})();
