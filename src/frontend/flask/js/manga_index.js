function do_delete(elem, manga_id) {
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
        req.open('GET', '/manga/delete_target?manga_id=' + manga_id);
        req.onload = function() {
            finish_delete(elem, manga_id);
        };
        req.send();
    };

    confirm.onblur = function () {
        confirm.setAttribute('onclick', null);
        elem.classList.remove("focus");
    };
}

function finish_delete(elem, manga_id) {
    var button = elem.children[0];
    var confirm = elem.children[1];
    var row = elem.parentElement.parentElement;

    row.classList.add('deleted');

    button.value = "Deleted";

    var btn_rename = document.getElementById('btn-rename-' + manga_id);
    btn_rename.setAttribute('onclick', null);
}

function do_rename(elem, manga_id) {
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

        console.log('Do send rename request ' + manga_id + ' ' + name);
        var req = new XMLHttpRequest();
        req.open('GET', '/manga/rename_target?manga_id=' + manga_id + '&name=' + name);
        req.onload = function() {
            finish_rename(elem, manga_id, name);
        };
        req.send();
    };

    text.onblur = function () {
        text.setAttribute('onkeydown', null);
        elem.classList.remove("focus");
    };
}

function finish_rename(elem, manga_id, name) {
    var button = elem.children[0];
    var text = elem.children[1];
    var name_field = document.getElementById("manga-link-" + manga_id);

    button.value = "Rename";
    name_field.innerText = name;
}

function do_create(elem) {
    var button = elem.children[0];
    var cancel = elem.children[1];

    var inputs = document.getElementById("create-inputs");
    var name_inp = document.getElementById("btn-create-name");
    var author_inp = document.getElementById("btn-create-author");
    var link_inp = document.getElementById("btn-create-link");

    if (!elem.classList.contains("focus")) {
        elem.classList.add("focus");
        inputs.classList.add("active");

        name_inp.focus();
    } else {
        elem.classList.remove("focus");

        name_inp.value = "";
        author_inp.value = "";
        link_inp.value = "";

        inputs.classList.remove("active");
    }
}

function finish_create(elem, manga_id, name, author) {
    console.log('Recv: ' + elem + ' ' + manga_id + ' ' + name + ' ' + author);

    var inputs = document.getElementById("create-inputs");
    var name_inp = document.getElementById("btn-create-name");
    var author_inp = document.getElementById("btn-create-author");
    var link_inp = document.getElementById("btn-create-link");

    elem.classList.remove("focus");
    inputs.classList.remove("active");

    var new_row = document.createElement('tr');

    new_row.innerHTML = '' +
        '<td>' + manga_id + '</td>' +
        '<td>' +
            '<a id="manga-link-' + manga_id + '" href="/chapter/index?manga_id=' + manga_id + '">' + name + '</a>' +
        '</td>' +
        '<td>' +
            '<div id="btn-delete-' + manga_id + '" class="btn btn-delete">' +
                '<input type="button" class="passive" value="Delete">' +
                '<input type="button" class="active" value="Confirm?">' +
            '</div>' +
        '</td>' +
        '<td>' +
            '<div id="btn-rename-' + manga_id + '" class="btn btn-rename">' +
                '<input type="button" class="passive" value="Rename">' +
                '<input type="text" class="active">' +
            '</div>' +
        '</td>' +
    '';

    // Fucking web dev, why is a table not exactly a table
    var table = document.getElementById('manga-table').children[0];
    table.appendChild(new_row);

    var btn_delete = document.getElementById('btn-delete-' + manga_id);
    var btn_rename = document.getElementById('btn-rename-' + manga_id);
    btn_delete.onclick = (function(elem, manga_id) {
        return function() {
            do_delete(elem, manga_id);
        };
    })(btn_delete, manga_id);
    btn_rename.onclick = (function(elem, manga_id) {
        return function() {
            do_rename(elem, manga_id);
        }
    })(btn_rename, manga_id);

    name_inp.value = "";
    author_inp.value = "";
    link_inp.value = "";

}

(function() {
    var elem = document.getElementById('btn-create');
    var name_inp = document.getElementById("btn-create-name");
    var author_inp = document.getElementById("btn-create-author");
    var link_inp = document.getElementById("btn-create-link");

    function setfocus() {
        this.classList.add("focus");
    }
    function clearfocus() {
        if (this.value === "") {
            this.classList.remove("focus");
        }
    }
    function try_submit() {
        if (event.key === 'Enter') {
            if (link_inp.value !== "") {
                var name = name_inp.value;
                var author = author_inp.value;
                var link = link_inp.value;

                var req = new XMLHttpRequest();
                req.open('GET', '/manga/create_target?name=' + name + '&link=' + link + '&author=' + author);
                req.onload = function() {
                    finish_create(elem, req.responseText, name_inp.value, author_inp.value);
                };
                req.send();
            } else {
                link_inp.focus();
            }
        }
    }

    name_inp.onfocus = setfocus;
    name_inp.onblur = clearfocus;
    name_inp.onkeydown = try_submit;
    author_inp.onfocus = setfocus;
    author_inp.onblur = clearfocus;
    author_inp.onkeydown = try_submit;
    link_inp.onfocus = setfocus;
    link_inp.onblur = clearfocus;
    link_inp.onkeydown = try_submit;
})();

(function() {
    for (var ii=0; ii<manga_ids.length; ii++) {
        var manga_id = manga_ids[ii];
        var btn_delete = document.getElementById('btn-delete-' + manga_id);
        var btn_rename = document.getElementById('btn-rename-' + manga_id);
        btn_delete.onclick = (function(elem, manga_id) {
            return function() {
                do_delete(elem, manga_id);
            };
        })(btn_delete, manga_id);
        btn_rename.onclick = (function(elem, manga_id) {
            return function() {
                do_rename(elem, manga_id);
            }
        })(btn_rename, manga_id);
    }
    var btn_create = document.getElementById('btn-create');
    btn_create.onclick = function() {
        do_create(btn_create);
    };
})();
