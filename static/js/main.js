$(function() {
  $("#button").on("click", function(e) {
    $.post("/submit", {"video": $("#input").val()});
  });
  $("#volup").on("click", function(e) {
    $.get("/volup");
  });
  $("#voldown").on("click", function(e) {
    $.get("/voldown");
  });
  $("#delet").on("click", function(e) {
    $.get("/delet");
  });

  setInterval(function() {
    $.getJSON("/queue", function(q) {
      things = '';
      for(var a=0; a<q.length; a++) {
        things += '<p>'+q[a]+'</p>'
      }
      $("#queue").html(things);
    });
  }, 1000);
});
