$(document).ready(function() { 
  $("select").imagepicker({show_label:true});
  $( "#invite_submit" ).click(function() {
    $( "#invite_friends_form" ).submit();
  });
});