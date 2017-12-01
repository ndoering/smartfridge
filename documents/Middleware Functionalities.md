# Smart Fridge application functionalities

We aim to develop our application as a  middleware which is implemented in Python code and executes the core functionalities (described underneath). Apart from that, our backend consists of a SQLite database, along with an apache instance that runs alongside our core application. In order to estimate the fruits edibility, we use cloud service classification. The user interface will be a simple, mobile optimized website that provides all information at a glance.

### Middleware

+ Capturing of images on a regular basis
+ Image processing pipeline
  + Reducing the image resolution
  + Segmentation of fruits to provide more valid input data
+ Uploading the captured images to a classification cloud service
  + Cloud API call
  + Saving the returned edibility information into the database
+ Data Management and database access
  + Picture storage
  + Logging
    + Timestamp
    + Received edibility estimation
    + Number of bananas
    + Number of potatoes
    + Date of appearance / disappearance
+ Web frontend
  + Mobile optimized
  + Simple and clear to use
+ Automatic push notification for 'Slack' messenger platform
  + Database access
  + Slack API Call

### Backend
+ SQLite Database as source for our website
  + Storage of metadata
  + Storage of binary image files
+ Apache Webserver  

----------------------------------

~# Pseudo Code

The pseudo code shall serve as a basis for later discussions. I suggest the following template to describe our code functions.

###### function_name

+ Purpose:

+ Argument:

+ Return Value:

+ Algorithm:

### Support script within the operating system

Purpose: Capturing Images on a regular basis. (For instance every hour). It's a shell script which runs aside our core program in order to be more robust.

### Core Middleware Application

Initializations:
+ Create database connection

###### ask_mlcloud
Purpose: For each new image, the function calls the ML-service to check its edibility.

Argument: One Image.

Return Value: Probability of the fridges content's freshness.

Algorithm:
+ Check for latest picture
+ Use specific web API call and send the image to the provider
+ Receive answer (chance of edibility) 
+ return chance of edibility

###### log_edibility
Purpose: The function logs the actual edibility state to a database (whose shape and technology has to be designed yet).

Argument: ask_mlcloud return value, timestamp, picture name

Return Value: void

Algorithm:
+ Create database connection
+ Log edibility result, timestamp, picture name~
