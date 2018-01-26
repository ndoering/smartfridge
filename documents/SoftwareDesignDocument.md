# Software Design Document - Smartfridge

Names: Melanie, Liuba, Nils, Jörn, Chris

<div style="page-break-after: always;"></div>
\newpage


## Revision History

| Version | Date       | Commentary           |
|---------|------------|----------------------|
| 0.0     | 2017-12-19 | Initial Template     |
| 1.0     | 2018-01-26 | Detailed description |

<div style="page-break-after: always;"></div>
\newpage

## TABLE OF CONTENTS
1. [Introduction](#1-introduction)

	1.1 [Purpose](#11-purpose)

	1.2 [Scope](#12-scope)

	1.3 [Overview](#13-overview)

	1.4 [Reference Material](#14-reference-material)

	1.5 [Definitions and Acronyms](#15-definitions-and-acronyms)

2. [System overview](#2-system-overview)

3. [System architecture](#3-system-architecture)

	3.1 [Architectural Design](#31-architectural-design)

	3.2 [Decomposition Description](#32-decomposition-description)

	3.3 [Design Rationale](#33-design-rationale)

4. [Data design](#4-data-design)

	4.1 [Data Description](#41-data-description)
		
	4.2 [Data Dictionary](#42-data-dictionary)

5. [Component design](#5-component-design)

6. [Human interface design](#6-human-interface-design)

	6.1 [Overview of User Interface](#61-overview-of-user-interface)

    6.2 [Screen Images](#62-screen-images)

	6.3 [Screen Objects and Actions](#63-screen-objects-and-actions)

7. [Requirements matrix](#7-requirements-matrix)

8. [Appendices](#8-appendices)

<div style="page-break-after: always;"></div>
\newpage

## 1. Introduction


### 1.1 Purpose
~~Identify the purpose of this SDD and its intended audience. (e.g. “This
software design document describes the architecture and system design of
XX.”).~~

This software design document describes the architecture and system design of
the SmartFridge project that accompanies the Systems and Software Engineering
class.


### 1.2 Scope
~~Provide a description and scope of the software and explain the goals,
objectives and benefits of your project. This will provide the basis for the
brief description of your product.~~

The software serves as a prototype or MVP (minimum viable product) to the
overarching idea of a system that tracks content inside a consumer fridge. As
such its scope is reduced to identify two distinct fruits (bananas and tomatoes)
and evaluate their ripeness. This is embedded in a notifaction system for a
hypothetical enduser.

This prototype is built to be easily adapted to more fruits and other
products.


### 1.3 Overview
~~Provide an overview of this document and its organization.~~

This document is subdivided into 6 parts: system overview, system architecture,
data design, component design, human interface design and a requirements matrix.


### 1.4 Reference Material
~~This section is optional.  List any documents, if any, which were used as
sources of information for the test plan.~~


### 1.5 Definitions and Acronyms
~~This section is optional.  Provide definitions of all terms, acronyms, and
abbreviations that might exist to properly interpret the SDD. These definitions
should be items used in the SDD that are most likely not known to the
audience.~~


## 2. System overview
~~Give a general description of the functionality, context and design of your
project. Provide any background information if necessary.~~


Accomplishments from user perspective:
- provide a web interface for the user to interact:
  - show a recent picture of the inside of the fridge
  - show a message about the state of the fridge content
- take a picture and send it to a cloud machine learning application; can be
  done periodically and on user demand
  - based on the response:
    - bad food: send a notification to a designated slack channel
    - everything ok: stay idle

### Web interface

### Notification via Slack channel

### Classification of the freshness of fruits

### Database storage for later use


## 3. System architecture


### 3.1 Architectural Design
~~Develop a modular program structure and explain the relationships between the
modules to achieve the complete functionality of the system. This is a high
level overview of how responsibilities of the system were partitioned and then
assigned to subsystems. Identify each high level subsystem and the roles or
responsibilities assigned to it. Describe how these subsystems collaborate with
each other in order to achieve the desired functionality. Don’t go into too much
detail about the individual subsystems. The main purpose is to gain a general
understanding of how and why the system was decomposed, and how the individual
parts work together. Provide a diagram showing the major subsystems and data
repositories and their interconnections. Describe the diagram if required.~~

The prototype of the SmartFridge mainly consists of the layers,
following a MVC (Model-View-Controller) architecture. The model
consists of the SQL-Database server in the backend of the prototype,
storing the images and their classifcations. The view is implemented
by a webserver providing the website displaying the current state of
the fridge and by the notitfations sent to the Slack channel. The
controlling part consists of a python programm which regularly takes
images of the fridge contents, preprocesses them, sends them to
Clarifai for classification and to the database for storage.

#### System architecture overview
![Interactions within the system](Components.png)


### 3.2 Decomposition Description
~~Provide a decomposition of the subsystems in the architectural
design. Supplement with text as needed. You may choose to give a functional
description or an object­oriented description.  For a functional description,
put top­level data flow diagram (DFD) and structural decomposition diagrams. For
an OO description, put subsystem model, object diagrams, generalization
hierarchy diagram(s) (if any), aggregation hierarchy diagram(s) (if any),
interface specifications, and sequence diagrams here.~~


#### Model - Database

We use a *MySQL* database server as the model for our application. This
standard database is installed directly on the Raspberry Pi and runs
as a standalone server in background. We connect to the database with
the *mysql-connector-python* module. This module is provided by the
MySQL project.


#### View - Webserver



#### Controller - Python middleware

![Processing within the middleware](middleware.png)

The controller takes the images of the content of the fridge. This is
done via the camera module attached to the Raspberry Pi and the
*picamera* python module. The images are created as binary
representations of *JPEG* images.

The images are then handed over to the image processing pipeline. This
pipeline is a modular chain of processing functions. The type of
processors can be defined via the global configuration
file. The pipeline takes one image at a time, processes it
sequentially and returns the transformed image.

Thereafter, the transformed image is handed to the Clarifai connection
module. This module sends the image to Clarifai in order to have if
classified. The model used for classification can be chosen throug the
global configuration. The connecting module receives the
classification within seconds after sending.

Afterwards the image and the classification is handed over to the
database to be stored.


##### Image processing pipeline

The image processing pipeline is modularly built the be configured to
needs at hand. The global configuration file specifies the number,
type and order of the processors. Each processor is a seperate stage
in the pipeline.

![Overview of the image processing pipeline](image-pipeline.png)

Each processor is an object providing exactly one function. This
*process()* function takes an image, transforms it and returns
it. This SISO (single input, single output) function is chained
together in a list of functions that provides the resulting
transformation. Therefore even complex transformations an be created
from simple steps.

For the prototype there are two rudimentary examples for presentation
purposes, the *Dummy* and the *GreyScale* processor. A *Dummy* stage
simply returns the image and forwards it. A *GreyScale* stage converts
the colors of the image to a greyscale. It uses *OpenCV* and the
*opencv-python* module for this task.


### 3.3 Design Rationale
~~Discuss the rationale for selecting the architecture described in
3.1 including critical issues and trade/offs that were considered. You
may discuss other architectures that were considered, provided that
you explain why you didn’t choose them.~~


#### MVC architecture

The MVC pattern was chosen to reduce the cohesion between parts of the
program. In this design the technologies used can be changed without
affecting other, more stable parts of the program.

Therefore we have chosen an standalone database server, which is
connected via a single python module. The module can be changed out
completely and therefore facilitate a change in the storage backend.

Furthermore, the webserver, which provides the view is only loosely
coupled with the controller and the model. The connections are
provided by standard tools of the operating system itself.

Therefore, each part of the system can be exchanged or transfered to
other computers. The onyl part that necessarily has to run on the
Raspberry Pi is the image collection using the hardware camera. This
part can easily be extracted from the controller and run as a
seperate, standalone server. All of the other parts can be migrated to
more powerful machines to accomodate higher processing needs.


#### Image processing pipeline

The pipeline structure, often called Pipes-and-Filter architecture,
facilitates a simple exchange of the stages. Therefore the pipeline
can be adapted to different needs for image preprocessing.

The processors in the pipeline are seperate objects, that should not
and do not share state. This simplifies possible parallel handling of
multiple images in future versions. Since they are seperate objects
they could also be exchanged at runtime. Therefore, one only has to
whether the stage currently processes an image and if not, it can be
removed and replaced by another processor.


#### Image classification provider

The image classification is handled by a low cost provider
(Clarifai). This helps us to deliver a prototype faster. For future
versions this can be provided by another provider or by another
program developed by us.

Clarifai was chosen because of three reasons. Firstly, it provides a
simple Python module, that is freely available via the PyPi packaging
system. If necessary, we also could reach Clarifai via REST
calls. Secondly, the first testing results looked promising. We get
reasonable classifications with a high confidence from
Clarifai. Furthermore, the spread in confidence between the highest
ranking class and the next lower ranking class is significant and
therefore we can easy distinguish and compute the resulting
class. Lastely, Clarifai provides a free-of-cost plan for testing
purposes.


## 4. Data design


### 4.1 Data Description
Explain how the information domain of your system is transformed into data
structures.  Describe how the major data or system entities are stored,
processed and organized. List any databases or data storage items.


### 4.2 Data Dictionary
Alphabetically list the system entities or major data along with their types and
descriptions. If you provided a functional description in Section 3.2, list all
the functions and function parameters. If you provided an OO description, list
the objects and its attributes, methods and method parameters.


## 5. Component design
In this section, we take a closer look at what each component does in a more
systematic way. If you gave a functional description in section 3.2, provide a
summary of your algorithm for each function listed in 3.2 in procedural
description language (PDL) or pseudocode. If you gave an OO description,
summarize each object member function for all the objects listed in 3.2 in PDL
or pseudocode. Describe any local data when necessary.


## 6. Human interface design


### 6.1 Overview of User Interface
Describe the functionality of the system from the user’s perspective. Explain
how the user will be able to use your system to complete all the expected
features and the feedback information that will be displayed for the user.


### 6.2 Screen Images
Display screenshots showing the interface from the user’s perspective. These can
be handdrawn or you can use an automated drawing tool. Just make them as
accurate as possible.  (Graph paper works well.)


### 6.3 Screen Objects and Actions
A discussion of screen objects and actions associated with those objects.


## 7. Requirements matrix
Provide a cross­reference that traces components and data structures to the
requirements in your SRS document.  Use a tabular format to show which system
components satisfy each of the functional requirements from the SRS. Refer to
the functional requirements by the numbers/codes that you gave them in the SRS.


### 7.1 Python


### 7.2 Python modules

| Module                 | Version  |
|------------------------|----------|
| clarifai               | 2.0.32   |
| mysql-connector-python | 8.0.5    |
| slackclient            | 1.1.0    |
| opencv-python          | 3.4.0.12 |
| confiparser            | 3.5.0    |


## 8. Appendices
This section is optional.  Appendices may be included, either directly or by
reference, to provide supporting details that could aid in the understanding of
the Software Design Document.
