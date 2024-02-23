Currently the app does not work as intended. I was unable to get a containerized broker image (Eclipse Mosquitto) to work so I elected to 
connect to an existing free mqtt broker I found on the website, emqx.io, which does not work for the purposes this project was created for,
but I wanted to have at least something to show, that sort of works.  

Right now, the containerized app for an mqtt client subscribing to a topic and sending messages to that topic works within the container.
I thought of using a local database file instead of a separate containerized database image, but as it turns out, it only works when run locally.
I am still working on this project to implement MongoDB docker image so that it actually works as intended, a fully containerized app, with a 
containerized mqtt broker image, database image, and app.

**How to run the containerized app:**
First, you need an installation of Docker on your device. Follow instructions here: https://docs.docker.com/get-docker/
Then you need an installation of Python (I believe, not 100% sure)
**1) Clone the repository to a folder of your choice or create a new one for it**
**2) navigate to the folder in cmd**
**3) Run the command "docker build -t mqttassignment"**
The container should now be available in docker desktop UI to run and tinker with.


