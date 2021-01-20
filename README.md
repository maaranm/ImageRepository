<p align="center">
  <h3 align="center">Image Repository by Maaran Murugathas</h3>
  <p align="center">
    This is a Python and Django program which allows users to locally host an image repository
    <br>
  </p>
</p>


## Table of contents

- [Quick start](#quick-start)
- [Features](#features)
- [Screenshots](#screenshots)

## Quick start
This guide assumes that you already have Python 3.6.x installed
1. Clone the github repo
2. Install dependencies from the ```requirements.txt``` using ```pip install -r requirements.txt```
3. Install mysql
4. Create a database in mysql and make a new user with access to the database
5. In the ```settings.py``` file modify lines 80-84 with the appropriate information from the newly created mysql database
6. From the root directory of the project in a terminal or command prompt window run ```manage.py runserver```
7. In a web browser navigate to localhost:8000/pictures
8. The default page allows you to upload images, clicking View All shows all uploaded images and Search for Object allows you to find images containing an object

Please note that the uploaded images are processed in the background to extract features. This may take anywhere from 30 seconds to several minutes depending on the computer hardware. Testing was done using a Nvidia GTX 1080.

## Features
### Current
* Upload images with names
* View all uploaded images
* Uses TensorFlow trained model to extract objects found in uploaded images to allow users to search for objects and display images with specified object in view
### Upcoming
* Label and search by people (eg. find images with Maaran)
* Search by upload name

## Screenshots
## Uploading an image
![alt text](https://github.com/maaranm/ImageRepository/blob/develop/images/Cafe%20Upload.png?raw=true)

## Viewing all uploaded images
![alt text](https://github.com/maaranm/ImageRepository/blob/develop/images/View%20all.png?raw=true)

## Searching for an object
![alt text](https://github.com/maaranm/ImageRepository/blob/develop/images/search.png?raw=true)

## Display images with searched object
![alt text](https://github.com/maaranm/ImageRepository/blob/develop/images/annotated.png?raw=true)
