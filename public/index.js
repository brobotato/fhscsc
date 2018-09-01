$(document).ready(function() {

var UpdateMessages = function() {
  $.getJSON("/submit", function(data) {
    $.each( data, function(index, val) {
      $("#message-" + (index+1).toString()).fadeOut(function() {
        $(this).text(val).fadeIn();
      });
    });
  });
};

UpdateMessages();

$("#submit").click(function(e) {
  $.post("/submit", {"text": $("input[name='input']").val()})
    .done(function() {
      UpdateMessages();
    });
  e.preventDefault();
});

});