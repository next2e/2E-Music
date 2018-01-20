function submit_video(e) {
    $.post("/submit", {"video": $("#url").val()});
    $("#url").val("");
    $("#linkButton").blur();
    alert("Submitted! The song play/appear in the queue once it is loaded.");
}

function submit_search() {
    var query = $("#query").val();
    if (query.length) {
        $.getJSON("/search", {"query": query}, display_results);
    } else {
      $.getJSON("/shuffle", display_results);
    }
}

function delete_song(song_number) {
    $.post("/delete", {"song": song_number})
}

function select_song(song) {
    $.post("/playsong", {"song": song});
}

function display_results(songs) {
    var listing = ''
    songs.forEach(function(song) {
        listing += '<li></span><button onclick="select_song(\'' + song + '\')" ';
        listing += 'class="select-song">Add</button> ';
        listing += song.substring(0, song.lastIndexOf('.'));
        listing += '</span></li>';
    })
    $("#search-results").html(listing);
}

$(function() {
  $.getJSON("/shuffle", display_results);
  $("#add-song").on("click", submit_video);
  $("#submit-search").on("click", submit_search);
  $("#quietButton").on("click", function(e) {
    $("#quietButton").blur();
    $.get("/quiet");
  });
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
  $("#shuffle").on("click", function(e) {
    $("#shuffle").blur();
    $.getJSON("/shuffle", display_results);
  });
  $("#toggle-search").on("click", function(e) {
      if ($('#search-container:visible').length) {
          $('#search-container').hide("slow");
      } else {
          $('#search-container').show("slow");
      }
      $("#search-arrow").toggleClass("glyphicon-chevron-up");
      $("#search-arrow").toggleClass("glyphicon-chevron-down");
      $("#toggle-search").blur();
  });
  $('#url').keypress(function(e) {
    if (e.keyCode == 13) {
      submit_video();
      e.preventDefault();
    }
  });
  $('#query').keypress(function(e) {
    if (e.keyCode == 13) {
        submit_search();
      e.preventDefault();
    }
  });

  setInterval(function() {
    $.getJSON("/queue", function(q) {
        things = '';
        $("#playing").html('<p>'+q[0]+'</p>');

        for(var a=1; a<q.length; a++) {
            things += '<li><span>'
            things += '<button onclick="delete_song(' + a + ')" class="delete"> Delete </button>'
            things += q[a] + '</span></li>'
        }
        $("#queue").html(things);
    });
  }, 1000);
});
