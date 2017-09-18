function submit_video(e) {
    $.post("/submit", {"video": $("#url").val()});
    $("#url").val("");
    $("#linkButton").blur();
    alert("Submitted! The song play/appear in the queue once it is loaded.");
};

function delete_song(song_number) {
    $.post("/delete", {"song": song_number})
    alert("Deleted! The song will disappear once the queue is reloaded.")
}

$(function() {
  $("#linkButton").on("click", submit_video);
  $("#random").on("click", function(e) {
    $("#random").blur();
    $.get("/random");
  });
  $("#volup").on("click", function(e) {
    $("#volup").blur();
    $.get("/volup");
  });
  $("#voldown").on("click", function(e) {
    $("#voldown").blur();
    $.get("/voldown");
  });
  $("#skipButton").on("click", function(e) {
    $("#skipButton").blur();
    $.get("/skip");
  });
  $('#url').keypress(function(e) {
    if (e.keyCode == 13) {
      submit_video();
      e.preventDefault();
    }
  });

  setInterval(function() {
    $.getJSON("/queue", function(q) {
        things = '';
        $("#playing").html('<p>'+q[0]+'</p>');

        for(var a=1; a<q.length; a++) {
            things += '<li><span>'
            things += '<button onclick="delete_song(' + a + ')" class="delete hvr-shutter-out-horizontal"> Delete </button>'
            things += q[a] + '</span></li>'
        }
        $("#queue").html(things);
    });
  }, 1000);
});
