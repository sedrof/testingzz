


$(document).ready(function(){
    $('#id_state').change(function() {
          var selected = $(this).val();
          if(selected == 'VIC') {
            $('#id_Address').val('10 Melbourne Street');
    //  to fill in more than one field:  $('#id_blah').val('other val');
          }
          else if(selected == 'WA') {
            $('#id_Address').val('10 West Australia Street');
          }
          else if(selected == 'SA') {
            $('#id_Address').val('10 South Australia Street');
          }
          else if(selected == 'NSW') {
            $('#id_Address').val('Sydney');
          }
          else if(selected == 'QLD') {
            $('#id_Address').val('10 Queensland Street');
          }
        });
      });