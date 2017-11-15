(function() {
    var inputs = document.getElementsByTagName('input');
    for (var i=0; i<inputs.length; i++) {
        if (!('intent' in inputs[i].attributes)) {
            continue;
        }

        var intent = inputs[i].attributes.intent.value;
        if (intent === 'delete') {
            inputs[i].onclick = function() {
                var page_id = this.attributes.key.value;
                var req = new XMLHttpRequest();
                req.open('GET', '/page/delete_target?page_id=' + page_id);
                //req.send();
                console.log('DELETE: ' + page_id);
            }

        } else if (intent === 'rechapter') {
            inputs[i].onclick = function() {
                var page_id = this.attributes.key.value;
                var after_split = false;
                var split_ids = [];
                var ids = document.getElementsByTagName('idcontainer');
                var newchapter_name = document.getElementById('name-' + page_id).value;
                for (var j=0; j<ids.length; j++) {
                    if (ids[j].attributes.key.value === page_id) {
                        after_split = true;
                    }
                    if (after_split) {
                        split_ids.push(ids[j].attributes.key.value);
                    }
                }
                var req = new XMLHttpRequest();
                req.open('POST', '/page/rechapter_target');
                req.setRequestHeader('Content-Type', 'application/json');
                req.send(JSON.stringify({
                    manga_id: document.getElementById('manga_id').value,
                    sort_key: document.getElementById('sort_key').value,
                    name: newchapter_name,
                    page_ids: split_ids,
                }));
            }

        } else if (intent === 'chapter-rename') {
            inputs[i].onclick = function () {
                var chapter_id = this.attributes.key.value;
                var new_name = document.getElementById('chapter-rename').value;
                var req = new XMLHttpRequest();
                req.open('GET', '/chapter/rename_target?chapter_id=' + chapter_id + '&name=' + new_name);
                req.send();
            }

        } else if (intent === 'chapter-resort') {
            inputs[i].onclick = function() {
                var chapter_id = this.attributes.key.value;
                var sort_key = document.getElementById('chapter-resort').value;
                var req = new XMLHttpRequest();
                req.open('GET', '/chapter/resort_target?chapter_id=' + chapter_id + '&sort_key=' + sort_key);
                req.send();
            }
        }
    }
})();