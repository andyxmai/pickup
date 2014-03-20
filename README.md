ReqTime
==============
![ReqTime Icon](http://reqtime.herokuapp.com/static/img/logo-main.png)
> ###Your hub for pickup sports


```
Authors:
- Andy Mai <andymai@stanford.edu>
- Claire Negiar <cnegiar@stanford.edu>
- Ethan Myers <eymyers@stanford.edu>
- Joe Abbott <jrabbott@stanford.edu>
- Kennan Murphy-Sierra <kennan@stanford.edu>
Date: March 20, 2014
Version: 1.0
```


About
---------------------

ReqTime is a social network for pick-up sports that enables you easily create, find, and join games being played near you. The motivation behind this app is based on logistic challenges we have faced organizing pickup games and tracking expected attendance.


Packages Used
---------------------

##### Activity Stream (News Feed)

The Activity Stream package used was from user, justquick, on github.  The package wraps the Django functionality of ***send***, ***signal***, and more to create an easy to use activity stream.  The activity stream is used to track the actions of all users.  The user chooses to follow another user.  The users news feed is filled with actions the user’s followees performed as well as any game created.

<https://github.com/justquick/django-activity-stream>

Note: After installing activity stream locally, the file "/Library/Python/Python#/site-packages/actstream/urls.py" was modified by removing ".defaults".  


##### Notifications

A notifications package from the github user, brantyoung, was used to keep track of user-generated notifications on the app. Examples of notifications include users joining and leaving games, a new game created, new follower, etc. 

The notifications package is called using the following line:
notify.send(request.user,recipient=game.creator, verb=verb, description=description), where request.user is the User objects that initiated the notification for which game.creator (a different User object) will receive. Verb is the content of the notification, and description is the link associated with the notification. 

<https://github.com/brantyoung/django-notifications>


##### Instagram API

The Instagram API was used to connect users to their Instagram accounts. By linking to their Instagram accounts, users can post and share photos on game pages. Once the user has authorized ReqTime on Instagram, an authenticity token is given back to our site that we can then use to access the user’s Instagram data. 

The Instagram API page also links to a python library with built-in functions to fetch photos and videos. The following two lines illustrate how to get the five most recent Instagram photos of a user:

api = InstagramAPI(access_token=access_token)
recent_media, next = api.user_recent_media(count=5)

##### Google Visualization

The Google Visualization API was use to make pie charts on the Analytics page for information such as the breakdown by sports of the games a user has played, or the breakdown by sports of all the sports being played by users on the app. 

##### Google Maps API

The Google Maps API was used to show the location of the different games being played, and to have clickable icons for each game, with custom sports icons so that people can then access the individual game pages. It was also used for pop-ups displaying information about each game and the number of people who can sign up for each game. We used javascript to add filtering functionality based on the type of sport, so that only the icons for the checked sports are visible at any given time. 

##### Facebook API
The Facebook API was used for users to select and upload profile pictures. All of the code is done on the client side and nothing is stored in our backend. We first send Facebook our App ID, and after the user has authorized our app, we then fetches all of the user’s pictures on Facebook. We then put the pictures in an image picker for the user to select.

The code to access the API is located inside the "script" tag in user.html

##### Image Picker / Gallery
The Image Picker is used in conjunction with the Instagram API to allow users to select pictures to post on game pages. It is a jQuery plugin that takes a list of photos and renders a multiselect with each option being the actual photo. 

#### JQuery Autocomplete
A plugin to autocomplete user’s input using a dataset queried from the server. The package is especially useful for search to show potential results before a user has finished typing the entire query term. 

Our Own Implementation
---------------------

##### Recommendation
The code for the game recommendation engine is located in get_game_recommendations within views.py. The method takes considers several factors and assigns a score to each factor for every game. In the end, the games with the highest scores will be recommended to the user. 

The main factor is to check if the game is the sport that the user likes. It also checks for the location of the game to determine how close the venue is to the user. The closer it is to the user, the higher score the game will get. The method will also look at all the players in the game. The more players with similar skill levels as the user, the higher score the game will get. 

For now, the scores are assigned somewhat arbitrarily. As more data is generated in our app, we can eventually move to a machine learning model where the scores will be learned programmatically.

Main Webpages (Flow)
--------------
#### Analytics (analytics.html)
The analytics page helps users visualize the breakdown of the sports they have played, and those played by the Reqtime community as a whole, by sport. It also gives information on the most popular sport for each location. 

#### Navbar (base.html)
The base.html is the base template from which all of the view templates in our app will inherit. It contains the navbar that all pages will inherit. 

#### Creating a Game (create_game.html)
Displays the form for which users can create games. 

#### Registering (first_login*.html)
Upon signing up for an account, we will ask the new user a few questions about their favorite sports and their skill levels in those sports. The data is used for recommending games to the user later. 

#### Game Pages (game.html)
- Photos
    A user can connect to instagram so as to post pictures of the game. The pictures can be visualized through the Image Gallery API

- Comments
    There is also space for posting and visualizing comments on the page, so as to facilitate coordination and logistics between users. This may, for example, be used by the different members of the group to decide on who will be bringing what equipment, or send any other important messages (e.g. decide on a color to wear for each team). 

#### Getting Instagram Photos (get_instagram_photos.html)
Displays the list of instagram photos in a user-friendly manner and allows the user to select one.  Upon selection, the photo will be added to the game page.

#### Home Page (home.html)
- Maps / Game Filtering
    A user can use the map to locate a game next to where he is, and filter games by sports based on his interest levels. Pop-up dialog boxes allow users to see the time and number of players for each game, and links to the actual game page itself. 
- News Feed
- Search
- Recommendations

#### Landing Page (index.html)
Host the user upon visit. Allows for sign in, sign up, and browsing information.

#### Invite Friends to Game (invite_friends.html)
If a user is the creator of a game, he will be able to invite other ReqTime users to join his game. The selected users will receive a notification about the game invitation, and will then be able to join the game if they so wish. 

#### Sport (sport.html)
Displays all the games associated with the particular sport. Gives users who are searching for games of a specific sport to see all the upcoming games. 

#### Sports (sports.html)
A gateway page that guides users to all the sports that are played on ReqTime. 

#### User Profile (user.html)
Page that displays players of Reqtime. When the player is the loggedin user, this page becomes the profile page that allows for photo upload and Instagram access, in addition to the user’s game history and upcoming games. For other players, it displays information such as their upcoming and past games. 

Database Overview
-----------------
####User
Django’s built-in user authentication model. It stores users’ basic information such as first name, last name, username, email, and encrypted password.

####Location
Stores location name such as Wilbur Field and the latitude and longitude coordinates for displaying on Google Maps.

####Sport
Stores the sport’s name and a list of users who specified the sport as one of their favorites.

####Game
Once a user creates a game, the following information is stored. Name of the game, description of the game, start time, maximum number of players, ID of the creator, location of the game, users who have signed up for the game, and the type of sport.

####Comment
Stores the text a user writes to comment on a game as well as the timestamp and the IDs of the associated game and user.

####InstagramInfo
An extension of the User model. It has a one-to-one relationship with the User model and contains all the necessary Instagram information such as access tokens to fetch the user’s game photos.     

####GamePhoto
Stores the link to the thumbnail and standard size of the photo as well as the ID of the associated game.

####UserInfo
An extension of the User model that stores information not already contained in the built-in Django user authentication model. It stores the user’s profile picture and geolocation.
    
####UserSportLevel
Stores the skill level of the user’s favorite sport. The information is saved for the recommendation component to better suggest games to users. 

Initial Database
------------------
The initial_data.json file in pickupApp/fixtures contains all the initial data that we put into the database. These data include the type of sports that are played on Reqtime, as well as a few dummy games in order to show the full interface of the app for the demo. 

The file gets triggered when we run migration on the app. Django will automatically load the data due to a naming convention of initial_data. 

Repo Overview
-------------
```
.  
├── README.md  
├── db.sqlite3 (Should not see this, local database)
├── manage.py  
├── notes.txt  (Notes/Instructions concerning any tools with django)
├── pickup/  
│   ├── __init__.py  
│   ├── settings.py (Contains the configurations for the app)
│   ├── urls.py (Controls the routing)
│   ├── wsgi.py  
├── pickupApp/  
│   ├── __init__.py  
│   ├── admin.py
│   ├── constants.py  (File containing constants)
│   ├── fixtures/  (This contains the initial data to populate the database with)
│   │   └── initial_data.json  
│   ├── forms.py (Holds the template for all the forms)
│   ├── middleware/  
│   │   └── request.py  
│   ├── models.py  (This holds all the models/database relations used)
│   ├── static/  
│   │   ├── css/  (Holds all the css styling for the web pages)
│   │   ├── favicon.ico  
│   │   ├── fonts/  
│   │   ├── images/  
│   │   ├── img/  
│   │   └── js/  (Holds all the javascript code for the web pages.  Each webpage has a corresponding js file.  They have the same name.)
│   ├── templates  (Descriptions of the webpages are above)
│   │   ├── about.html  
│   │   ├── analytics.html  
│   │   ├── base.html  
│   │   ├── create_game.html  
│   │   ├── first_login.html  
│   │   ├── first_login2.html  
│   │   ├── game.html  
│   │   ├── game_update_form.html  
│   │   ├── get_instagram_photos.html  
│   │   ├── home.html  
│   │   ├── index.html  
│   │   ├── invite_friends.html  
│   │   ├── notUsed/  
│   │   ├── recommendations.html  
│   │   ├── sport.html  
│   │   ├── sports.html  
│   │   └── user.html  
│   ├── tests.py    
│   └── views.py  (This is the main controller)
└──  requirements.txt  (Contains all modules Heroku need to install for deployment)
```




