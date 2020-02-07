#!/bin/sh
# Shell script to set the environmental variables for the flask application
export FLASK_ENV=development
export FLASK_APP=application.py
export DATABASE_URL="postgres://yjgedtdqfmlqyi:ed20bcf4553937fc4966cf6be7e07091d15f61e2ae1185bc61890af320db7c73@ec2-54-92-174-171.compute-1.amazonaws.com:5432/d4cd015h5c3uie"
echo Variables Set!
