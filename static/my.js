'use strict';

$('#save').on("click", function (e) {
    e.preventDefault();
    $.getJSON('/saveplaylist',
        function (data) {
            //do nothing
        });
    console.log("saved playlist");

    this.disabled = true;
    this.innerHTML = "Playlist Saved in Spotify!";
    this.style.backgroundColor = "gray";
    this.style.border = "none";
    return false;
});

$("#generate").on("click", function () {
    var loading = document.getElementById("loading");
    loading.style.display = "inline";
    return true;
});