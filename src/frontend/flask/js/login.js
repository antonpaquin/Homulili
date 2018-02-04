document.getElementById('login').onclick = function() {
    var uname = document.getElementById('uname').value;
    var password = document.getElementById('password').value;

    var req = new XMLHttpRequest();
    req.open("POST", "/login/login_target");
    req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    req.onload = function () {
        if (req.status == 200) {
            document.cookie = "uname=" + uname + ";";
            document.cookie = "pass_hash=" + req.responseText + ";";
            window.location = '/manga';
        } else {
            document.getElementById('password').value = '';
        }
    };
    req.send('uname=' + uname + '&password=' + password);
};

document.getElementById('create').onclick = function() {
    var uname = document.getElementById('uname').value;
    var password = document.getElementById('password').value;

    var req = new XMLHttpRequest();
    req.open("POST", "/login/create_target");
    req.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    req.onload = function () {
        if (req.status == 200) {
            document.cookie = "uname=" + uname + ";";
            document.cookie = "pass_hash=" + req.responseText + ";";
            window.location = '/manga';
        } else {
            document.getElementById('uname').value = '';
            document.getElementById('password').value = '';
        }
    };
    req.send('uname=' + uname + '&password=' + password);
};
