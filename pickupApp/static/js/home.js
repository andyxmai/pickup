var infowindow=null;
var markers= new Array ();

function initialize() {

  var myLatlng = new google.maps.LatLng(37.422, -122.16);
  var initialLocation;
  var browserSupportFlag = new Boolean();

  var mapOptions = {
    zoom: 14,
    //center: myLatlng
  };

  var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
  
  if(navigator.geolocation) {
    browserSupportFlag = true;
    navigator.geolocation.getCurrentPosition(function(position) {
      initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
      map.setCenter(initialLocation);
      $.ajax({
        type: "POST",
        url: "/store_user_location/",
        data: { 
          'csrfmiddlewaretoken':'{{csrf_token}}', 
          'latitude' : position.coords.latitude,
          'longitude' : position.coords.longitude
        },
        success: function(data) {
        },
      });

      var image = 'http://i.stack.imgur.com/orZ4x.png';
      var userLocationMarker = new google.maps.Marker({
        position: initialLocation,
        map: map,
        icon: image
      });
    }, function() {
      handleNoGeolocation(browserSupportFlag);
    });
  } else {
    browserSupportFlag = false;
    handleNoGeolocation(browserSupportFlag);
  }

  function handleNoGeolocation(errorFlag) {
    if (errorFlag == true) {
      alert("Geolocation service failed.");
      initialLocation = myLatlng;
    } else {
      alert("Your browser doesn't support geolocation. We've placed you in Siberia.");
      initialLocation = myLatlng;
    }
    map.setCenter(initialLocation);
  }

  var locations = new Array();
  var games={};

  var json = '{{games_json|safe}}';
  var json_game_string = JSON.parse(json);
  //console.log(json_game_string);

  var i=0
  for (var key in json_game_string) {
    if (json_game_string.hasOwnProperty(key)) {
      var hash_key = key;
      var object = json_game_string[key];
      var lat = object['location_info']['latitude'];
      var longi = object ['location_info']['longitude'];
      games[hash_key]= object['games']
      locations[i]= new Array();
      locations[i].push(hash_key);
      locations[i].push(lat);
      locations[i].push(longi);
      i+=1;
    }

  }
  
  var marker; 
  var curr_sport;

  var infowindow = new google.maps.InfoWindow;
  
  var games_by_loc = {};

  for (var key in games) {
    if (json_game_string.hasOwnProperty(key)) {
      games_by_loc[key] = [new Array()];
    }
    var i=0;
    for (var key_2 in games[key]) {
      games_by_loc[key][i]=new Array();
      var curr_game = (games[key][key_2]);
      var game_id = curr_game['id'];
      var sport = curr_game['sport'];
      var name = curr_game['name'];
      var remaining= curr_game['curr_num_players'];
      var total = curr_game['max_num_players'];
      if (!total){
        total="Unlimited";
      }
      var game_arr = [sport, game_id,  name, remaining, total ]
      games_by_loc[key][i].push(game_arr);
      i+=1;
    }
  }

  var content_1;
  var content_2; 
  var myIcon;

  for (i = 0; i < locations.length; i++) { 
      loc = locations[i][0]
      for (j=0; j<games_by_loc[loc].length; j++){
        loc_string=games_by_loc[loc][j][0]
        curr_sport= loc_string[0];
        var markerImage;
        markerImage = new google.maps.MarkerImage(
            '/static/images/'+curr_sport+'.png',
            new google.maps.Size(50,50), //size
            null, //origin
            null, //anchor
            new google.maps.Size(50,50) //scale
         );
     
        marker = new google.maps.Marker({
          position: new google.maps.LatLng(locations[i][1] , locations[i][2]+j*0.0002),
          map: map,
          title: curr_sport,
          icon: markerImage
        });
      markers.push(marker);

      google.maps.event.addListener(marker, 'click', (function(marker, i) {
        return function() {
          var content_1 = '<div style="font-weight:bold; text-align:center">' + locations[i][0] + '</div>';
          loc = locations[i][0]
          var content_1 = '<p> <b>'+loc + '</b> </p>';
          for (j=0; j<games_by_loc[loc].length; j++){
            console.log(games_by_loc[loc][j][0]);
            if (games_by_loc[loc][j][0][0]==marker.getTitle()){

              var link = "/game/" + games_by_loc[loc][j][0][1];
              content_1 += '<p>'+ games_by_loc[loc][j][0][0]+ ': '+ '<u> <a href='+link+'>'+ games_by_loc[loc][j][0][2]+'</a></u>' +': ' + games_by_loc[loc][j][0][3]+ '/' + games_by_loc[loc][j][0][4]+ ' players'+ '</p>';
            }
              
          }
          infowindow.setContent(content_1);
          infowindow.open(map, marker);
        }
      })(marker, i));
    }
  }
}
google.maps.event.addDomListener(window, 'load', initialize);

function boxclick(box,category,type) {
  // for (var i=0; i<markers.length; i++) {
  //   markers[i].setVisible(false);
  // }
  show(category, type);
}

function show(category, type) {
  // the ALL checkbox
  if (type=='all'){
    resetCheckboxes();
    if (document.getElementById("all").checked === true){
      for (var i=0; i<markers.length; i++) {
        markers[i].setVisible(true);
      }
    } else  {
      for (var i=0; i<markers.length; i++) {
        markers[i].setVisible(false);
      }
    }
  } else{
    if (document.getElementById("all").checked === true){
      document.getElementById("all").checked = false;
      for (var i=0; i<markers.length; i++) {
        markers[i].setVisible(false);
      }
    }
    console.log("Line 368");
    for (var i=0; i<markers.length; i++) {
      if (markers[i].getTitle() == type){
        if(document.getElementById(type).checked === true) {
          console.log("Type is true");
          markers[i].setVisible(true);
        } else {
          console.log("Type is false");
          markers[i].setVisible(false);
        }
      }
    }
  }      
}

function resetCheckboxes() {
  document.getElementById("basketball").checked = false;
  document.getElementById("football").checked = false;
  document.getElementById("soccer").checked = false;
  document.getElementById("frisbee").checked = false;
  document.getElementById("tennis").checked = false;
  document.getElementById("golf").checked = false;
  document.getElementById("volleyball").checked = false;
}
