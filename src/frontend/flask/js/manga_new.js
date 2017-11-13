document.getElementById('submit').onclick = function() {
    var new_url = '/manga/create';
    new_url = new_url + '?name=' + document.getElementById('name').value;
    new_url = new_url + '&author=' + document.getElementById('author').value;
    new_url = new_url + '&link=' + document.getElementById('link').value;
    window.location.href = new_url;
};