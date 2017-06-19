//jquery functions
$(document).ready(function() {

  //turns 1st step green on lock in
  $(function() {
    $("#gllock").click(function() {
      $("#i1").attr("src", "static/images/green.png");
    });
  });

  //turns 2nd step green on lock in
  $(function() {
    $("#explock").click(function() {
      $("#i2").attr("src", "static/images/green.png");
    });
  });

  //This loads the option to save experiment selection and presents more info and options
  $(function() {
    $('a#process_input').bind('click', function() {
      $('#needthisbutton').empty();
      $.getJSON('/_process_description', {
        experiment_select: $("input[name='expradio']:checked").parent('label').text(),
      }, function(data) {
        $("#des").text(data.result);
        $("#needthisbutton").append("<button class='btn btn-danger center-block' data-toggle='modal' data-target='#myModalAO'>Advanced Options</button>");
      });
      return false;
    });
  });

  //This gets the pasted generator library text
  $(function() {
    $('#svGLBtn').click(function() {
      $.getJSON('/_process_glinput', {
          glin: $('textarea[name="mytextarea"]').val(),
        },
        function(data) {
          console.log(data.yesss);
        });
      return false;
    });
  });

  //This loads the Advanced Options selections modal
  $(function() {
    $("#nwCol").click(function() {
      $('#acv').empty();
      $.getJSON('/_adv_detect_su', function(data) {
        $(data.advanced).each(function(index, value) {
          if (value.present === 'yes') {
            $('#acv').append("<input name='aoCB' type='checkbox'" + "value='" + value.name + "'" + "checked='checked'>" + value.name + "</input>" + "</br>");
          } else {
            $('#acv').append("<input name='aoCB' type='checkbox'" + "value='" + value.name + "'>" + value.name + "</input>" + "</br>");
          }
        });
      });
    });
  });

  //This opton processes and saves the input form from advanced options
  $(function() {
    $('#svAoBtn').click(function() {
      $.getJSON('/_process_advanced', {
          advanced_select: $('input[name="aoCB"]:checked').serializeArray(),
        },
        function(data) {
          console.log(data.test);
        });
      return false;
    });
  });


});
