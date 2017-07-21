//jquery functions
$(document).ready(function() {

  //This gets the user's experiment title and abstract
  $(function() {
    $('#saveTitleandAbstract').click(function() {
      $('#loading').empty();
      $.getJSON('/_name_&_abstract', {
					title: $('#experimentName').val(),
					abstract: $('#experimentAbstract').val(),
        },
        function(data) {
          console.log(data.t);
					console.log(data.a);
          $('#loading').append("<h2>Uplod your generator library file, and click Lock In.</h2>");
        });
      return false;
    });
  });

	//This handles the gl file upload
	$(function() {
	 $('#filesubmit').click(function() {
		 $('#GLdisplay').empty()
     $('#loading').empty();
		 var form_data = new FormData($('#glupload')[0]);
		 $.ajax({
			 type: 'POST',
			 url: '/_gl_upload',
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
			 $("#GLdisplay").append("<ul class='list-group'> <li class='list-group-item list-group-item-success'> <b> Generator Library File: </b>" + data.name + "</li> </ul>");
       $('#loading').append("<h2>Select your experiment, click next, accsess advanced options if desired, then click Lock In.</h2>");
		 }).fail(function(data) {
			 alert('error!');
		 });
	 });
 });

 //This saves experiment option, loads the experiment description
$(function() {
	$('#experiment_select').click(function() {
    $('#loading').empty();
		$('#experiment_description').empty()
		$('#button_for_ao').empty();
		$('#DSdisplay').empty()
		$.getJSON('/_ec', {
			x_sel: $("input[name='expradio']:checked").parent('label').text(),
		}, function(data) {
			$("#experiment_desctiption").text(data.edes);
			$("#button_for_ao").append("<button class='btn btn-danger center-block' data-toggle='modal' data-target='#myModalAO'>Advanced Options</button>");
			$("#DSdisplay").append("<ul class='list-group'> <li class='list-group-item list-group-item-success'> <b> Experiment Choice: </b>" + $("input[name='expradio']:checked").parent('label').text() + "</li> </ul>");
      $('#loading').append("<h2>All set to GO!</h2>");
		});
		return false;
	});
});

//This function loads the advanced options for an experiment
$(function() {
	$("#div_for_ao").click(function() {
		$('#checkboxes_for_ao').empty();
		$.getJSON('/_display_ao', function(data) {
			$(data.advanced).each(function(index, value) {
				if (value.present === 'yes') {
					$('#checkboxes_for_ao').append("<input name='aoCB' type='checkbox'" + "value='" + value.name + "'" + "checked='checked'>" + value.name + "</input>" + "</br>");
				} else {
					$('#checkboxes_for_ao').append("<input name='aoCB' type='checkbox'" + "value='" + value.name + "'>" + value.name + "</input>" + "</br>");
				}
			});
		});
	});
});

//This processes form for advanced options
$(function() {
	$('#savebutton_for_ao').click(function() {
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
	$('#go').click(function() {
    $('#loading').empty();
		window.location.replace('/go');
		$('#loading').append("<img src='/static/images/ajax-loader.gif' alt ='Loading GIF'>");
		$('#loading').append("<h3>gemc is running on the server, awaiting results<h3>");
	});
});

});
