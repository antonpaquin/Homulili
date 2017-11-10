(function() {
    var buttons = document.getElementsByTagName('input');
    for (var i=0; i<buttons.length; i++) {
        if (!('intent' in buttons[i].attributes)) {
            continue;
        }
        var intent = buttons[i].attributes.intent.value;
        if (intent === 'delete') {
            buttons[i].onclick = function() {
                var chapter_id = this.attributes.key.value;
                var req = new XMLHttpRequest();
                req.open('GET', '/chapter/delete_target?chapter_id=' + chapter_id);
                req.send();
            }
        } else if (intent === 'rename') {
            buttons[i].onclick = function() {
                var chapter_id = this.attributes.key.value;
                var req = new XMLHttpRequest();
                var name = document.getElementById('rename-' + chapter_id).value;
                req.open('GET', '/chapter/rename_target?chapter_id=' + chapter_id + '&name=' + name);
                req.send();
            }
        } else if (intent === 'resort') {
            buttons[i].onclick = function() {
                var chapter_id = this.attributes.key.value;
                var req = new XMLHttpRequest();
                var name = document.getElementById('resort-' + chapter_id).value;
                req.open('GET', '/chapter/resort_target?chapter_id=' + chapter_id + '&sort_key=' + name);
                req.send();
            }
        }
    }
})();
