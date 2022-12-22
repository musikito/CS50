# MUSICAN


A family music player and playlist maker system using Django.
This is the final project for CS50's Web Programming with Python(Django), SQLite3, JavaScript, Bootstrap and wavesurfer-js.</br>
## How to run the project
In order to run the app we need to activate a virtual enviroment. In this case we use <b>virtualenv</b>.
### Setup and activate virtualenv

virtualenv env <br/>
. env/bin/activate

## Install requirements

pip install -r requirements.txt

## Setup Django

./manage.py makemigrations musican</br>
./manage.py migrate</br>
./manage.py runserver</br>
### Admin user(for admin panel)
User: Admin</br> 
Password: Pass@123
### Regular user
User: User<br>
Password: Pass@123

# Then visit http://localhost:8000


## Distinctiveness and Complexity
This project is different fro the ones thaught in the course in that it's use an external library(wavesurfer-js) to play MP3s and playlists made wtih those MP3s.
It uses differents Models to track what Songs belong to what Artist and to wich Playlist(s).</br>
Also feature a Genre part that group Songs by its Genre.</br>
There's a very close relationship between all the Models(tables) in the DB making it easy to add/remove features in the future like an option to add albums or publish playlists.

The site is fully responsive and mobile friendly, the Navbar have the menu for logged out users, while th Sidebar is only available for logged in users.

<b>The administrator(thru the Admin panel) is the one that can edit and alter the data.</b> 

There's a feature that if images aren't provided for Song,Genre or Artist, a default one will be provided.</br>
The project have a message bus as well a full breadcrumb feature(you can accesss all the features from everywhere in the site).

By using an external library for the player, we cut the development time and alos used the APIs for that library.

Also the app run in a virtual enviroment to prevent clashes or errors with differents versions of libs. and softwares.

## App structure
The  App directory is called Musican and is located under the Capstone  directory.
### Static
In the static directory are located the CSS and local JS files.</br>
- `static\musican\images`, we find the images for the app.</br>
- `static\musican\images\songs`, folder for the uploaded MP3s.</br>
- ` player.js`: This is the local Javascript file that control the player and alos act as the DOM manipulator.</br>
- `styles.css`: This file holds the styles of the entire app.

### Frontend
The frontend part of the app is located in the musican/templates/musican folder it have the following files:
#### For the logged out/not register users:
- `layout.html`: In this file contain the code hat will be inherited by the other .html files.
      In here we load our .css, .js files as well any library thru a CDN.
    
- `index.html`:
     This is the home/landing file, from here the user can login/logout as well register.
     Thru the Navbar, the logged out user can listen to songs and navigate to the artists, genres. They also can login or register.
- `login.html`: Login/logout functionality.
- `register.html`: Register a new user functionality.
- `artist_list.html`: List all the artists in the DB by images. When the user click on the image, it'll bring that artist info page.
- `artist.html`: Show info about the artist from the list. This include main pict. small bio and list of songs.
- `genre_list.html`:  List all the genress in the DB by images. When the user click on the image, it'll bring that genre info page.
- `genre.html`: List all the genres available(with images), when the user click on one, this will list all the songs under that genre.

#### For the logged in users:
- `create_artist.html`: In this page, thru a form, the user can add a new artist. They can provide a image as well a small bio. It also have an option to list the artist as 'featured'.
- `create_genre.html`: In this page, thru a form, the user can add a new genre. They can provide a image as well a small description.
- `create_song.html`: In this page, thru a form, the user can add a new song. In here the user will provide an image or cover, the source MP3, what artist and genre it belongs too. If these infos aren't known, a default will be provide by the system. It also have an option to list the song as 'featured'.
- `playlist.html`: This page will feature all the songs that the user add to his/her personalized playlist. It will play all the songs in it in order or the user can choose from a list. Because time constrains, I coulnd't implement a shuffle or next/previous functionality.

### Backend
The backend is located at the root of the app. It comprises of the following files:
- `admin.py`: Functionality for the administrator(s).
- `forms.py`: Group all the forms used in the app.
- `models.py`: Have all the connections and API calls to the DB to be provided to the views.
- `views.py`: The connector between the frontend and the backend.


## Setup and activate virtualenv

virtualenv env <br/>
. env/bin/activate

## Install requirements

pip install -r requirements.txt

## Setup Django

./manage.py makemigrations musican
./manage.py migrate
./manage.py runserver
User: Admin
Email: test@test.com
Password: Pass@123

# Then visit http://localhost:8000
