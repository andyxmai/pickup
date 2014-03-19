$(document).ready(function() {   
    $.backstretch([
        "/static/img/header1.jpg",
        "/static/img/header2.jpg"
        
        ], {
          fade: 400,
          duration: 5000
    });
    $('#request_button').click(function(){
      $('#requestModal').modal('show');
    });

    $('#signup_submit').click(function(){
      $('#signup_form').submit();

    });
    $('#signin_submit').click(function(){
      $('#signin_form').submit();

    });
    $('#request_submit').click(function () {
          var btn = $(this);
          btn.button('loading');
      });
    $("a[href^='#main']").on('click', function(e) {
       // prevent default anchor click behavior
       e.preventDefault();
       // store hash
       var hash = this.hash;
       // animate
       $('html, body').animate({
           scrollTop: $(this.hash).offset().top
         }, 500, function(){
           // when done, add hash to url
           // (default click behaviour)
           window.location.hash = hash;
         });
    });
    $("a[href^='#bottom']").on('click', function(e) {
       // prevent default anchor click behavior
       e.preventDefault();
       // store hash
       var hash = this.hash;
       // animate
       $('html, body').animate({
           scrollTop: $(this.hash).offset().top
         }, 500, function(){
           // when done, add hash to url
           // (default click behaviour)
           window.location.hash = hash;
        });
    });
    $("a[href^='#featured-clients']").on('click', function(e) {
       // prevent default anchor click behavior
       e.preventDefault();
       // store hash
       var hash = this.hash;
       // animate
       $('html, body').animate({
           scrollTop: $(this.hash).offset().top
         }, 500, function(){
           // when done, add hash to url
           // (default click behaviour)
           window.location.hash = hash;
        });
    });
    $('#notification').click(function(){
      $.ajax({
        type: "POST",
        url: "/remove_notifications/",
        data: { 
          'csrfmiddlewaretoken':'{{csrf_token}}' 
        },
        success: function(data) {
          $( "span.badge" ).remove();
        },
      });
    });
    $('#search').catcomplete({
      source: '/search',
      minLength: 1,
      select: function(event, ui) {
        if (ui.item.category == "People") {
          location.href = '/user/'+ui.item.id;
        } else if (ui.item.category == "Games"){
          location.href = '/game/'+ui.item.id;
        } else {
          location.href = '/sport/'+ui.item.value;
        }
      },
      open: function(event, ui) {
        $(".ui-autocomplete").css("z-index", 10000);
      },
      messages: {
        noResults: '',
        results: function() {}
      }
    });
    // $('#search').typeahead([
    //   {
    //     name: 'People',
    //     valueKey: 'name',
    //     remote: {
    //       url: '/searchpeople?query=%QUERY',
    //     },
    //     header: '<h4 class="searchchoices">People</h4>'
    //   },
    //   {
    //     name: 'Games',
    //     valueKey: 'name',
    //     remote: {
    //       url: '/searchgame?query=%QUERY',
    //     },
    //     header: '<h4 class="searchchoices">Games</h4>'
    //   }
    // ]).on('typeahead:selected', function (obj, datum) {
    //     if (datum['type'] == 'user') {
    //       window.location.href = "/user/"+datum['id'];
    //     } else {
    //       window.location.href = "/game/"+datum['id'];
    //     } 
    //     //console.log(datum);
    // });
  });

  $.widget( "custom.catcomplete", $.ui.autocomplete, {
    _renderMenu: function( ul, items ) {
      var that = this,
        currentCategory = "";
      $.each( items, function( index, item ) {
        if ( item.category != currentCategory ) {
          ul.append( "<li class='ui-autocomplete-category'>" + item.category + "</li>" );
          currentCategory = item.category;
        }
        that._renderItemData( ul, item );
      });
    }
  });

  //Home Work Carousel
  var owl = $("#work-carousel");

  owl.owlCarousel({
  items : 2, //10 items above 1000px browser width
  itemsDesktop : [1000,2], //5 items between 1000px and 901px
  itemsDesktopSmall : [900,2], // betweem 900px and 601px
  itemsTablet: [600,1], //2 items between 600 and 0
  itemsMobile : [0,1], // itemsMobile disabled - inherit from itemsTablet option
  navigation : false,
  pagination : true,
  autoHeight : true
  });