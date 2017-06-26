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

  //gets gl file
  $(function() {
    $('#filesubmit').click(function() {
      event.preventDefault();
      var form_data = new FormData($('#uploadform')[0]);
      $.ajax({
        type: 'POST',
        url: '/uploadajax',
        data: form_data,
        contentType: false,
        processData: false,
        dataType: 'json'
      }).done(function(data, textStatus, jqXHR) {
        console.log(data);
        console.log(textStatus);
        console.log(jqXHR);
        console.log('Success!');
        $("#resultFilename").text(data['name']);
        $("#resultFilesize").text(data['size']);
      }).fail(function(data) {
        alert('error!');
      });
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
      var array = []
      array = $("input[name='aoCB']:checked").map(function() {
        return this.value;
      }).get();
      $.getJSON('/_process_advanced', {
          advanced_select: JSON.stringify(array)
        },
        function(data) {
          console.log(data.test);
        });
      return false;
    });
  });


});
