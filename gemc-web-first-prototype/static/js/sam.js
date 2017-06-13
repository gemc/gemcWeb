//jquery functions
$(document).ready(function(){

  $(function() {
    $('a#process_input').bind('click', function() {
    $.getJSON('/_process_description', {
      experiment_select: $("input[name='expradio']:checked").parent('label').text(),
    }, function(data) {
      $("#result").text(data.result);
    });
    return false;
    });
  });


});
