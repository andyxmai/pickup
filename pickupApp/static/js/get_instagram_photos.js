$(document).ready(function() { 
  $("select").imagepicker();
  $( "#photos_submit" ).click(function() {
    $( "#post_photos_form" ).submit();
  });
});