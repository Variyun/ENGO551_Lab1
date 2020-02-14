# BookExplorer

Made for Engineering 551 - Advanced Geospatial Topics Winter 2020  
Lab 1 - Flask, SQL, ORMs, APIs  

## What is this?
This is a simple web app called BookExplorer. This app allows users to search books by author, title, year, and ISBN. To use this app, users must register for an account (but don't enter in anything serious because I didn't hash your passwords) and log in. Users can see the average ratings of books on Goodreads as well as the average user rating. On BookExplorer you can submit your own reviews and rate all your favorite books!   

**Link to demo:** https://youtu.be/Xp3_-3hHb5A

## Instructions to Run the Website
* Flask: While in the /backend folder, run the command "source ./set_variables.sh". This will run a simple shell script to set the environmental variables. Run the command "flask run" to start the flask app.

* Vue: While in the /bookexplorer folder, run the command "npm install" to install all the required dependencies used in this project. Once that is finished installing, run the command "npm run serve". This will host the website on your local machine and you can access it by going to "localhost:8080" which is the default address.  

## File Explanation 
* .gitignore - This file is used to ignore directories or files when pushing/ committing changes. In this case we are ignoring node modules that have been installed for the website. To install these dependencies and modules, we can use the command "npm install".

* package.json/ package-lock.json - These files describe what dependencies and modules that the website uses.

* /backend - This folder contains all the components for the backend that is made using Flask (application.py). Here we also have a "import.py" which imports all the books found in books.csv into my postgres database.

* /bookexplorer - This folder contains all the frontend components of the website. The frontend is developed using the vue.js framework. The folder /public contains the index.html that will load for users to see. the index.html uses vue components in the /src folders. There are three main vue components. App.vue which is th main vue application that uses BExplorer.vue and login.vue. login.vue contains the UI for the log-in screen while BExplorer.vue contains the book search and review submission functionality of the website.   
