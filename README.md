ReqTime
==============
![ReqTime Icon](http://www.protasker.com/images/time-thumbnail.jpg)
> ###Your hub for pickup sports 


```
Authors: 
- Andy Mai
- Claire Negiar
- Ethan Myers <eymyers@stanford.edu>
- Joe Abbott
- Kennan Murphy-Sierra
Date: March 20, 2014
Version: 1.0
```


About
---------------------
***

Packages Used
---------------------
***

##### Activity Stream (News Feed)
The Acitivty Stream package used was from user, justquick, on github.  The package wraps the Django functionality of ***send***, ***signal***, and more to create an easy to use activity stream.

<https://github.com/justquick/django-activity-stream>

Note: After installing activity stream locally, the file "/Library/Python/Python#/site-packages/actstream/urls.py" was modified by removing ".defaults".  


##### Notifications

##### Instragram API

##### Google Visualization

##### Google Maps API

##### Facebook API

##### Image Picker / Gallery


Main Webpages (Flow)
--------------
***
#### Register
#### Login
#### Home Page
- Maps / Game Filtering
- News Feed
- Search
- Recommendations

#### Game Page
- Photos
- Comments

#### User Page
#### Profile Page
#### Analytics Page
#### Create game
#### JQuery Search feature

Database Overview
-----------------
*** 

Initial Database
------------------
***

Repo Overview
-------------

.  
├── README.md  
├── db.sqlite3 (Should not see this, local database) 
├── manage.py  
├── notes.txt  (Notes/Instructions concerning any tools with django)
├── pickup/  
│   ├── __init__.py  
│   ├── settings.py  
│   ├── urls.py  
│   ├── wsgi.py  
├── pickupApp/  
│   ├── __init__.py  
│   ├── admin.py 
│   ├── constants.py  
│   ├── fixtures/  (This contains the initial data to populate the databse with)
│   │   └── initial_data.json  
│   ├── forms.py  
│   ├── middleware/  
│   │   └── request.py  
│   ├── models.py  (This holds all the models/database relations used)
│   ├── static/  
│   │   ├── css/  (Holds all the css styling for the webpages)
│   │   ├── favicon.ico  
│   │   ├── fonts/  
│   │   ├── images/  
│   │   ├── img/  
│   │   └── js/  (Holds all the javascript code for the webpages. Each webpage has a corresponding js file.  They have the same name.)
│   ├── templates  (Descriptions of the webpages are above)
│   │   ├── about.html  
│   │   ├── analytics.html  
│   │   ├── base.html  
│   │   ├── create_game.html  
│   │   ├── first_login.html  
│   │   ├── first_login2.html  
│   │   ├── game.html  
│   │   ├── game_update_form.html  
│   │   ├── get_instagram_photos.html  
│   │   ├── home.html  
│   │   ├── index.html  
│   │   ├── invite_friends.html  
│   │   ├── notUsed/  
│   │   ├── recommendations.html  
│   │   ├── sport.html  
│   │   ├── sports.html  
│   │   └── user.html  
│   ├── tests.py    
│   └── views.py  (This is the main controller)
└──  requirements.txt  









