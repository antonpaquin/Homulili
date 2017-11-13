document.getElementById('login').onclick = function() {
    var uname = document.getElementById('uname').value;
    var token = document.getElementById('token').value;
    document.cookie = "uname=" + uname + ";";
    document.cookie = "token=" + token + ";";
    window.location.href = '/login';
};
