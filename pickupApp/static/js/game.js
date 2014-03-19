

  $(document).ready(function() { 
  $(".join_button").click(function(e){
    $( "#join_form" ).submit();
  });

  $('#post_photos').click(function(){
      $('#photosModal').modal('show');
    });
  $("select").imagepicker();

  $('#post_photos').click(function(){
    $('#friendsModal').modal('show');
  });
  $("select").imagepicker();

  $(".delete_button").click(function(e){
    $("#delete_form").submit();
  });
});
