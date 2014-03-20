
$(document).ready(function() {

    var activeGame;
    $(".delete_button").click(function(e) {
        activeGame = this.id.match(/\d+/);
        console.log("ACTIVE GAME: "+activeGame);
        $('#delete_confirm').modal('show');
    });

    $('#delete_confirm_button').click(function(e) {
        console.log("DELETING GAME: "+activeGame);
        $('#delete_form').submit();
    });

    $(".join_button").click(function(e){
            $( "#join_form_"+this.id.match(/\d+/)).submit();
    });

    $('#post_photos').click(function(){
            $('#photosModal').modal('show');
    });

    $("select").imagepicker();

});