//jquery functions
$(document).ready(function() {

  $(function() {
    $('a#process_input').bind('click', function() {
      $.getJSON('/_process_description', {
        experiment_select: $("input[name='expradio']:checked").parent('label').text(),
      }, function(data) {
        $("#des").text(data.result);
        $("#advanced").after("<button type='button' class='btn btn-danger center-block'>Advanced Options</button>");
      });
      return false;
    });
  });

  $(function() {
    $("#explock").click(function() {
      $("#i2").attr("src", "static/images/green.png");
    });
  });


});
