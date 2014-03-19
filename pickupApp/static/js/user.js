
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


    $.getScript('//connect.facebook.net/en_US/all.js', function(){
        FB.init({
            appId      : '{{facebookID}}',
            channelUrl : '{{websiteURL}}',
            status     : true,
            xfbml      : false
        });

        FacebookPhotoSelector.setFacebookSDK(FB);
    });

    $('#facebook_photo_selector').facebookPhotoSelector({
        onFinalSelect : function(photos)
        {
            //console.log(photos);
            if (photos.length) {
                var photo_url = photos[0];
                $.ajax({
                type: "POST",
                url: "/upload_profile_photo/",
                data: { 
                    'photo_url': photo_url,
                    'csrfmiddlewaretoken':'{{csrf_token}}' 
                },
                success: function(data) {
                    window.location.href = "/profile"
                },
              });
            }
        }
    });

    $(".follow").click(function(){
        $.ajax({
            type: "POST",
            url:"/toggle_follow/",
            data: {
                'csrfmiddlewaretoken':'{{csrf_token}}',
                'player' : "{{player.username}}"
            },
            success: function(data){
                if(data == "Yes"){
                    $(".follow").html("UnFollow");
                }else{
                    $(".follow").html("Follow");
                }
            }
        });
    });
});