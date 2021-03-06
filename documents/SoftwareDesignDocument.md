# Software Design Document - SmartFridge

Names: Liuba, Nils, Jörn, Chris


<div style="page-break-after: always;"></div>


## Revision History

| Version | Date       | Commentary                |
|---------|------------|---------------------------|
| 0.0     | 2017-12-19 | Initial Template          |
| 1.0     | 2018-01-26 | Detailed description      |
| 2.0     | 2018-02-16 | More detailed description |


<div style="page-break-after: always;"></div>


## TABLE OF CONTENTS
1. [Introduction](#1-introduction)
    1. [Purpose](#11-purpose)
    1. [Scope](#12-scope)
    1. [Overview](#13-overview)
    1. [Reference Material](#14-reference-material)
    1. [Definitions and Acronyms](#15-definitions-and-acronyms)
1. [System Overview](#2-system-overview)
1. [System Architecture](#3-system-architecture)
    1. [Architectural Design](#31-architectural-design)
    1. [Decomposition Description](#32-decomposition-description)
    1. [Design Rationale](#33-design-rationale)
1. [Data Design](#4-data-design)
    1. [Data Description](#41-data-description)
    1. [Data Dictionary](#42-data-dictionary)
1. [Component Design](#5-component-design)
1. [Human Interface Design](#6-human-interface-design)
1. [Requirements Matrix](#7-requirements-matrix)
1. [Appendices](#8-appendices)

<div style="page-break-after: always;"></div>


## 1. Introduction


### 1.1 Purpose
This software design document describes the architecture and system design of
the SmartFridge project that accompanies the Systems and Software Engineering
class.


### 1.2 Scope
The software serves as a prototype or MVP (minimum viable product) to the
overarching idea of a system that tracks content inside a consumer fridge. As
such its scope is reduced to identify bananas and evaluate their ripeness. This
is embedded in a notification system for a hypothetical end user.

This prototype is built to conveniently adopt more fruits and other products.


### 1.3 Overview
This document is subdivided into 6 parts: system overview, system architecture,
data design, component design, human interface design and a requirements matrix.


### 1.4 Reference Material
The project has a [Wiki](https://github.com/ndoering/smartfridge/wiki) that
includes the up to date reference material.


## 2. System overview

### Web interface

The website provides the main interaction for the SmartFridge. The user can
request a photo from here to inspect the current state of the contents of the
fridge. The displayed image is accompanied by the state of the freshness of the
fruits within the image in form of a list.  Furthermore, a log is provided to
browse previous states of the fridge.


### Notification via Slack channel

If bad food is recognized in the fridge this is reported not only on the website
but also immediately in a predefined Slack channel. The user can therefore use
the Slack app to get the notifications asynchronously.


### Classification of the freshness of fruits

Images are sent to a cloud service to be classified by a machine learning
application. This is done periodically and on user demand.


### Database storage for later use

All images and the classifications received from the cloud service are stored
for displaying it on the website and later logging purposes. This is facilitated
by an on-site database server.


## 3. System architecture


### 3.1 Architectural Design
The prototype of the SmartFridge mainly consists of three layers, following the
MVC (Model-View-Controller) architecture. The model consists of the SQL-Database
server in the backend of the prototype, storing the images and their
classifications. The view is implemented by a webserver providing the website
displaying the current state of the fridge and by the notifications sent to the
Slack channel. The controlling part consists of a python program (middleware)
which regularly takes images of the fridge's content, preprocesses them, sends
them to Clarifai for classification and to the database for storage.

#### System architecture overview
![Interactions within the system](Components2.png)


### 3.2 Decomposition Description

#### Model - Database

We use a *MySQL* database server as the model for our application. This standard
database is installed directly on the Raspberry Pi and runs as a standalone
server in background. We connect to the database with the
*mysql-connector-python* module. This module is provided by the MySQL project.

The database is comprised of two tables, *fridgelog* and *all_fruits*. The first
table contains all the raw images, their timestamps and an optional note. The
second table stores parts of the raw camera image, only featuring one fruit
within. This feature is currently not implemented. For each of these parts the
classification (label) is stored, along with the confidence and an optional
note. These part images are referenced via a foreign key to the corresponding
*fridgelog* entry. Therefore, a retrieval all parts of one image and their
respective classifications is possible.


#### View - Webserver

The webserver is a standard *Apache HTTP* webserver. It is provided by the
operating systems package manager. It runs as a standalone service and provides
the website for the SmartFridge.

The website itself is built in *PHP*, *HTML* and *CSS* and optimized for
responsiveness to make it independent of the user's device type. The main
drivers during development are ease of use and simplicity.  It provides a
current image and the corresponding classifications, which are taken from the
database. The website works autonomously and will not be triggered
asynchronously from the controller.

It also provides a button that triggers the controller, currently using an
operating-system-level signal, which is called via the *pkill* command. This
signal induces the controller to provide a new image and classifications, which
will be stored in the database. The website takes the new image and displays it
accompanied by its classifications.


#### Controller - Python middleware

![Processing within the middleware](middleware.png)

The controller takes the images of the content of the fridge. This is done via
the camera module attached to the Raspberry Pi and the *picamera* python
module. The images are created as binary representations of *JPEG* images.

The images are then handed over to the image processing pipeline. This pipeline
is a modular chain of processing functions. The type of processors can be
defined via the global configuration file. The pipeline takes one image at a
time, processes it sequentially and returns the transformed image.

Thereafter, the transformed image is handed to the Clarifai connection
module. This module sends an API call containing the image to Clarifai to have
it classified. The model used for classification can be chosen through the
global configuration. Currently a custom visual recognition model that has been
trained with a series of banana images is used.  The connecting module receives
the classification within seconds after sending.

Afterwards the image and its classification are handed over to the database to
be stored.


##### Image processing pipeline

The image processing pipeline is modularly built and can be configured to needs
at hand. The global configuration file specifies the number, type and order of
the processors. Each processor is a separate stage in the pipeline.

![Overview of the image processing pipeline](image-pipeline.png)

Each processor is an object providing exactly one function. This *process()*
function takes an image, transforms it and returns it. This SISO (single input,
single output) function is chained together in a list of functions that provides
the resulting transformation. Therefore, even complex transformations can be
created from simple steps.

For the prototype there are two rudimentary examples for presentation purposes,
the *Dummy* and the *GreyScale* processor. A *Dummy* stage simply returns the
image and forwards it. A *GreyScale* stage converts the colors of the image to a
greyscale. It uses *OpenCV* and the *opencv-python* module for this task. Other
processors that could be build into the pipeline in the future include
downscaling and segmentation of fruits.


### 3.3 Design Rationale

#### MVC architecture

The MVC pattern was chosen to reduce the cohesion between parts of the
program. In this design the technologies used can be changed without affecting
other, more stable parts of the program.

Therefore, we have chosen an standalone database server, which is connected via
a single python module. The module can be changed out completely and therefore
facilitate a change in the storage backend.

Furthermore, the webserver, which provides the view is only loosely coupled with
the controller and the model. The connections are provided by standard tools of
the operating system itself.

Therefore, each part of the system can be exchanged or transferred to other
computers. The only part that necessarily must run on the Raspberry Pi is the
image collection using the hardware camera. This part can easily be extracted
from the controller and run as a separate, standalone server. All the other
parts can be migrated to more powerful machines to accommodate higher processing
needs.


#### Image processing pipeline

The pipeline structure, often called Pipes-and-Filter architecture, facilitates
a simple exchange of the stages. This means the pipeline can be adapted to
unique needs for image preprocessing.

The processors in the pipeline are separate objects, that should not and do not
share state. This simplifies possible parallel handling of multiple images in
future versions. Since they are separate objects they could also be exchanged at
runtime. Consequently, one only needs to know whether the stage currently
processes an image and if not, it can be removed and replaced by another
processor.


#### Image classification provider

The image classification is handled by a low-cost provider (Clarifai). This
helps to rapidly deliver a prototype. For future versions the machine learning
can be managed by another provider or by another program developed by us.

Clarifai was chosen because of three reasons. Firstly, it provides a simple
Python module, that is freely available via the PyPi packaging system. If
necessary, we also could reach Clarifai via REST calls. Secondly, the first
testing results looked promising. We got reasonable classifications with a high
confidence from Clarifai. Furthermore, the spread in confidence between the
highest ranking class and the next lower ranking class is significant, so we can
easily distinguish and compute the resulting class. Finally, Clarifai provides a
free-of-cost plan for testing purposes.


## 4. Data Design

### 4.1 Data Description

Currently Smart Fridge classifies exclusively bananas, due to the project's time and 
ressource contraints. Nevertheless, the data design allows to specify further fruit 
to be added lateron. Hence, two tables are provided:

Table 'fridgelog' stores within each entry one image containing (soon) several sorts 
of fruit, along with the corresponding timestamp 'capturetime' and the primary key 
'fid'.

Table 'allfruits' refers the 'fridgelog' table by using fid as foreign key additionaly
to its primary key 'afid'. The actual edibility is kept by the integer value 'class'
which currently ranges from one (fresh) to five (spoiled). Moreover, the prediction
confidence is stored within the float value 'confidence'. Additionally, 'note' serves 
as 'string'-datatype that is soon intended to store the fruits' types.

Consequently, from one picture, several fruits will be extracted and preprocessed (via
picture pipeline) and classified. The results will be spllit to n entries in 'allfruits'
which refer to one single entry in 'fridgelog'. 

#### Fridgelog

| Name        | Description       |
|-------------|-------------------|
| fid         | ID of image       |
| capturetime | Time of capture   |
| full_image  | BLOB of the image |

#### Allfruits

| Name       | Description                     |
|------------|---------------------------------|
| fid        | ID of image                     |
| afid       | associated image from fridgelog |
| class      | classification from ML          |
| confidence | confidence for class            |
| note       | optional note (fruit type)     |

#### ER Diagram

![ER](ER.png)

### 4.2 Data Dictionary
Due to the dynamic nature of *Python*, data types are not fixed.

## 5. Component design

### cli_parser
This module takes the input of the commandline and parses it. It stores the path
of the configuration file.

### configuration_management
This module uses the *Python* stdlib parses for *ini* files. This reads the
configuration file and stores the information of the configuration in a
two-dimensional *dict*.

### sql_connector
This module facilitates the access to the database to store the images taken by
the camera.

### slack_connector
This module pushes notifications to a preconfigured Slack channel. The channel
and the credentials are set in the configuration file.

### clarifai_connector
This module sends the taken image to the *Clarifai* webservice via a REST
call. It awaits the response and returns a json string with the classification.

### image_pipeline
This module takes an image and processes it through a series of image
processors. The sequence of processors is configured in the systems
configuration. The image is handed to the first processor and returned from it
after processing. Afterwards the resulting image is handed to the next processor
until the sequence reaches its end. The final image is returned.

### camera
This module uses the *picamera* module to take an image from the camera.

### web_interface
This module takes the newest images and classifications from the database and
displays it. It also provides a button to signal the middleware to take a new
image. The website reloads to show the newest classified image.


## 6. Human Interface Design

At the current stage the User Interface enables users to check their groceries'
state conveniently via smartphone or desktop computer. The content's edibility is 
visualized in three ways: Actual images of the fridge's shelf, a time-series chart
displaying the edibility classes continuously from 1 (fresh) to 5 (spoiled), as well 
as a page showing a plain logging-table which cronologicaly displays the Database 
entries.

These are the basic attributes:

- Edibility Class
  - Fresh
  - Neutral-Fresh
  - Neutral
  - Neutral-Bad
  - Bad
- Prediction Confidence
  - It determines the degree, how 'sure' the system estimates the edibility by
   checking the picture.
- The corresponding timestamp

### User Interface Overview

#### Home

![Home-Page](ui_home.PNG)

The Home page displays both, the latest picture with corresponding data, as well
as past-images. By clicking the arrow on the right and left, the user swipes trough 
the image content forward and backward. Underneath the gallery, an update button 
triggers the latest picture from the fridge's shelf along with the classified edibility
data.

#### Statistics

![Statistics](ui_statistics.PNG)

The chart displays the edibility in a time-series fashion, representing the edibility
as steady values between 1 (fresh) and 5 (spoiled).

#### Log

![Log](ui_log.PNG)

The log represents the saved data in compact table, resembling the database design.

## 7. Requirements matrix

| Module             | Requirements        |
|--------------------|---------------------|
| camera             | 1.1                 |
| image_pipeline     | (1.3), (1.5), (2.1) |
| clarifai_connector | 2.2, 2.3, 2.4, 2.5  |
| slack_connector    | 3.3                 |
| sql_connector      | 1.2, 1.4, 3.1       |
| web_interface      | 3.2                 |
| smartfridge        | 3.3                 |

Entries in parenthesis were cut due to the timeline.

### 7.1 Python

We use *Python* in version 3.6.

### 7.2 Python modules

| Module                 | Version  |
|------------------------|----------|
| clarifai               | 2.0.32   |
| mysql-connector-python | 8.0.5    |
| slackclient            | 1.1.0    |
| opencv-python          | 3.4.0.12 |
| confiparser            | 3.5.0    |
