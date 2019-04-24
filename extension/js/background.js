$(document).ready(function () {
    var url;
    url = window.location.href;
    $.ajax({
        url: "http://localhost:8080/index.html",
        type: "GET",
        data: "url="+url,
    });
});


