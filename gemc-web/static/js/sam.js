//jquery functions
$(document).ready(function() {

  $(function() {
    $('a#process_input').bind('click', function() {
      $.getJSON('/_process_description', {
        experiment_select: $("input[name='expradio']:checked").parent('label').text(),
      }, function(data) {
        $("#des").text(data.result);
        $("#advanced").after("<button type='button' id='advBtn' class='btn btn-danger center-block' data-toggle='modal' data-target='#myModalAO'>Advanced Options</button>");
      });
      return false;
    });
  });

  $(function() {
    $("#explock").click(function() {
      $("#i2").attr("src", "static/images/green.png");
    });
  });


  $(function() {
    $("#nwCol").click(function() {
      $.getJSON('/_adv_detect_su', function(data) {
        $(data.advanced).each(function(index, value) {
          if (value.present === 'yes') {
            $('#adDiv').after("<input name='aoCB' type='checkbox' checked='checked'>" + value.name + "</input>" + "</br>");
          } else {
            $('#adDiv').after("<input name='aoCB' type='checkbox'>" + value.name + "</input>" + "</br>");
          }
        });
      });
    });
  });

  $(function() {
    $('#svAoBtn').click(function() {
      $.getJSON('/_process_advanced', {
        advanced_select: $('#advDet').serializeArray(),
      }, function(data) {
        console.log(data.test);
      });
      return false;
    });
  });


});
