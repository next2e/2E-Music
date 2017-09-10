$(function() {
  $("#linkButton").on("click", function(e) {
    $.post("/submit", {"video": $("#url").val()});
    alert("Submitted! The song play/appear in the queue once it is loaded.");
  });
  $("#volup").on("click", function(e) {
    $.get("/volup");
  });
  $("#voldown").on("click", function(e) {
    $.get("/voldown");
  });
  $("#skipButton").on("click", function(e) {
    $.get("/skip");
  });

  setInterval(function() {
    $.getJSON("/queue", function(q) {
        things = '';
        $("#playing").html('<p>'+q[0]+'</p>');

        for(var a=1; a<q.length; a++) {
            things += '<li><span>'+q[a]+'</span></li>'
        }
        $("#queue").html(things);
    });
  }, 1000);
});
