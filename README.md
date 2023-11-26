# Search Engine
A simple search engine that crawls webpages and retrieve its content via a user friendly interface or frontend.
The search engine consists of a web crawler,indexing system using the whoosh library and a frontend.

##Project Structure
-crawler.py file: crawls websites and parse html pages
-app.py file: implements a flask web application with a search form and display the results
-whoosh index:diectory to our indexing system

##Getting started
#Prerequisites
python was used to build this project.
created a virtual environment and installed all dependencies using the command.
```bash
pip install -r requirements.txt
```
##Deployment
The search engine was deployed on the university demo server.
An FTP in my case Filezilla to transfer files and putty an ssh client to deploy my project to the server
A wsgi file was created to connect the flask app to the server.

