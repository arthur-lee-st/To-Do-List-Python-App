# To-Do-List-Python-App

This is my first web app written using Python Flask.

Users may create an account and log in. Once logged in, they may add tasks to their to do list, with options to edit or delete. They will also see current weather info right above.

If users mistype their login info and thus fail to log in, a message will be displayed to let them know, signaling them to try again.

Python Flask Jinja Json API Authentication Sqlite HTML CSS Docker

https://github.com/arthur-lee-st/To-Do-List-Python-App/assets/56611771/6e40e09a-754a-4b0b-b487-07c428fb9fc3

____________________________________________________________________________________________________________________

How to run:
   
    In the terminal, 
       1. build docker image, type "docker image build -t to_do_app ."
       2. run docker image, type "docker run -p 5000:5000 -d to_do_app"
    Open a browser, then type in "localhost:5000"

____________________________________________________________________________________________________________________

How to stop:
   
    In the terminal, 
       1. type "docker ps" to get container id
       2. type "docker stop <insert container id>"
