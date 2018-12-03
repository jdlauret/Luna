var btn = document.getElementById("btn");
var container = document.getElementById("our_container");
var url = 'http://127.0.0.1:8000/Soft_Skills/';

btn.addEventListener("click", function(){
    var ourRequest = new XMLHttpRequest();
    ourRequest.open("GET", url);
    ourRequest.onload = function(){
        console.log(ourRequest.responseText); //Not JSON Formatted
        var ourData = JSON.parse(ourRequest.responseText);
        console.log(ourData);

    };
    ourRequest.send();
});