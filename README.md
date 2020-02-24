# BookExplorer

Made for Engineering 551 - Advanced Geospatial Topics Winter 2020  
Lab 1 - Flask, SQL, ORMs, APIs    

## Features 

* Login/ Logout & Account Registration: Users are able to register for an account and login/out after registration. The registration page will check to see if the username is used or not (which will result in an error message if they try to use it).

* Book Search: Users can search books by author, title, year, and ISBN. The search function will return all like terms the user entered into the search bar. An error message will be displayed if no books are found.  

* Book Review: Users can submit reviews for books and see other user submitted reviews/ ratings. Users can also see the average Goodreads rating and average user rating on the book page.

* API Access: Users can access the API by using the route /api/<isbn> which will return a json containing book title, year, author, ISBN, average rating, and number of ratings. 
  
**Link to demo:** https://youtu.be/Xp3_-3hHb5A

## Instructions to Run the Website
* Flask: To install the required python packages, we can run the command "pip3 install -r requirements.txt" while in the /backend folder. To set our environmental variables we can run the command "source ./set_variables.sh" to execute a simple shell script. Run the command "flask run" to start the flask app.

* Vue: While in the /bookexplorer folder, run the command "npm install" to install all the required dependencies used in this project. Once that is finished installing, run the command "npm run serve". This will host the website on your local machine and you can access it by going to "localhost:8080" which is the default address.  

## File Explanation 
* .gitignore - This file is used to ignore directories or files when pushing/ committing changes. In this case we are ignoring node modules that have been installed for the website. To install these dependencies and modules, we can use the command "npm install".

* package.json/ package-lock.json - These files describe what dependencies and modules that the website uses.

* /backend - This folder contains all the components for the backend that is made using Flask (application.py). Here we also have a "import.py" which imports all the books found in books.csv into my postgres database.

* /bookexplorer - This folder contains all the frontend components of the website. The frontend is developed using the vue.js framework. The folder /public contains the index.html that will load for users to see. the index.html uses vue components in the /src folders. There are three main vue components. App.vue which is th main vue application that uses BExplorer.vue and login.vue. login.vue contains the UI for the log-in screen while BExplorer.vue contains the book search and review submission functionality of the website.   
