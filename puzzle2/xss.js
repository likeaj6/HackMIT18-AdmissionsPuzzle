let url1 = "/beta/signup";
let url2 = "/beta/boost_rating";
var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function () {
    if (this.readyState != 4) return;

    if (this.status == 200) {
        console.log(this.responseText)
        // we get the returned data
    }

    // end of state change: it can be after some time (async)
};
let data = 'username=likeaj6_ee7df2';
var xhr = new XMLHttpRequest();
xhr.open("POST", "/beta/boost_rating/", true);
xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
xhr.setRequestHeader("Content-Length", data.length);
xhr.send(data);

var xhr = new XMLHttpRequest();
xhr.open("POST", url2, true);
xhr.setRequestHeader('Content-Type', 'application/json');
xhr.send(JSON.stringify(data));
