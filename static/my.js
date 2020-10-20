'use strict';

// $(function () {
$('#pls').on("click", function (e) {


    e.preventDefault();
    $.getJSON('/saveplaylist',
        function (data) {
            //do nothing
        });
    // $('button').off("click")
    console.log("saved playlist");

    this.disabled = true;
    this.innerHTML = "Playlist Saved in Spotify!";
    this.style.backgroundColor = "gray";
    this.style.border = "none";
    return false;
});



// });