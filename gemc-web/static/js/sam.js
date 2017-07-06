//jquery functions
$(document).ready(function() {

  //This saves the user's experiment description and name
  $(function() {
    $('#utsv').click(function() {
      $.getJSON('/_process_username', {
          uexpname: $('input[name="falcon"]').val(),
        },
        function(data) {
          console.log(data.yyy);
        });
      return false;
    });
  });

  //This saves the user's experiment description and name
  $(function() {
    $('#uasv').click(function() {
      $.getJSON('/_process_abstract', {
          uexpab: $('#bluejay').val(),
        },
        function(data) {
          console.log(data.nnn);
        });
      return false;
    });
  });


  //gets gl file
  $(function() {
    $('#filesubmit').click(function() {
      $('#usergldisp').empty()
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
        $("#usergldisp").append("<ul class='list-group'> <li class='list-group-item list-group-item-success'> <b> Generator Library File: </b>" + data.name + "</li> </ul>");
      }).fail(function(data) {
        alert('error!');
      });
    });
  });

  //This loads the option to save experiment selection and presents more info and options
  $(function() {
    $('#userec').click(function() {
      $('#userdsdisp').empty()
      $('#needthisbutton').empty();
      $.getJSON('/_process_description', {
        experiment_select: $("input[name='expradio']:checked").parent('label').text(),
      }, function(data) {
        $("#des").text(data.result);
        $("#needthisbutton").append("<button class='btn btn-danger center-block' data-toggle='modal' data-target='#myModalAO'>Advanced Options</button>");
        $("#userdsdisp").append("<ul class='list-group'> <li class='list-group-item list-group-item-success'> <b> Experiment Choice: </b>" + $("input[name='expradio']:checked").parent('label').text() + "</li> </ul>");
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

  $(function() {
    $('#loadinggiftrigger').click(function() {
      $('#loading').append("<img src='static/images/ajax-loader.gif' alt ='Loading GIF'>");
      $('#loading').append("<h3>gemc is running on the server, awaiting results<h3>");
    });
  });

});
