# Requirements Specification for Project 'SmartFridge'
by Melanie, Liuba, Nils, Jörn, Chris   
based on [IEEE SRS Template](http://www.ccc.cs.uni-frankfurt.de/wp-content/uploads/2016/11/srs_template-ieee.doc)

### Table of contents
1. [Introduction](#1introduction)
    1. [Purpose](#11purpose)
    1. [Intended Audience and Reading Suggestions](#12intended-audience-and-reading-suggestions)
    1. [Product scope](#13product-scope)
1. [Overall Description](#2overall-description)
    1.	[Product Perspective](#21product-perspective)
    1.	[Product Functions](#22product-functions)
    1.	[User Classes and Characteristics](#23user-classes-and-characteristics)
    1.	[Operating Environment](#24operating-environment)
    1.	[Design and Implementation Constraints](#25design-and-implementation-constraints)
    1.	[User Documentation](#26user-documentation)
    1. [Assumptions and Dependencies](#27assumptions-and-dependencies)
1.	[External Interface Requirements](#3external-interface-requirements)
    1.	[User Interfaces](#31user-interfaces)
    1.	[Hardware Interfaces](#32hardware-interfaces)
    1.	[Software Interfaces](#33software-interfaces)
    1.	[Communications Interfaces](#34communications-interfaces)
1.	[System Features](#4system-features)
    1.	[Data acquisition and storage](#41-data-acquisition-and-storage)
    1. 	[Detection and tracking of food aging process](#42-detection-and-tracking-of-food-aging-process)
    1.	[Notification of critical food status](#43notification-of-critical-food-status)
1.	[Other Nonfunctional Requirements](#5other-nonfunctional-requirements)
    1.	[Performance Requirements](#51performance-requirements)
    1. 	[Safety Requirements](#52safety-requirements)
    1.	[Security Requirements](#53security-requirements)
    1.	[Software Quality Attributes](#54software-quality-attributes)
    1.	[Business Rules](#55business-rules)
1. 	[Product Vision and further scenarios](#56product-vision-and-further-scenarios)
    1.	[Easier Input for food data](#57easier-input-for-food-data)
    1.	[Recommendations for groceries and recipes](#58recommendations-for-groceries-and-recipes)
    1.	[Delivery service connection and automatic orders](#59Delivery-service-connection-and-automatic-orders)
    1.	[Voice assistant integration (Siri and Alexa)](#60siri-and-alexa)
    1.	[Social food sharing platform](#61social-food-sharing-platform)
    1.	[Data exchange with other kitchen machines](#62data-exchange-with-other-kitchen-machines)
    1.	[Rethinking the interior fridge design](#63rethinking-the-interior-fridge-design)


<div style="page-break-after: always;"></div>

## Revision History
| Version | Date       | Commentary                |
|---------|------------|---------------------------|
| 1.0     | 2017-11-18 | Initial Draft             |
| 2.0     | 2017-11-29 | Updated with Use Cases    |
| 3.0     | 2018-01-02 | Updated with higher goals |

<div style="page-break-after: always;"></div>

## 1.	Introduction
##### 1.1	Purpose
This document specifies the software requirements for the SmartFridge
project (no release number yet). It describes the entire system.

##### 1.2	Intended Audience and Reading Suggestions
This document is intended for the class of Systems and Software
Engineering (WS 2017/2018) at University of Frankfurt. It should be
read in whole as each section is relevant for the students' task.

##### 1.3	Product Scope
A device that determines the freshness of food in a fridge. It can
optionally be used to track and show the current fridge content. Since
we aim to deliver a proof of concept prototype, the examined fruits
and vegetables will initially be bananas and tomatoes.

<div style="page-break-after: always;"></div>

## 2.	Overall Description
##### 2.1	Product Perspective
The described product is a university class project. It can serve as
an add-on to fridges already equipped with "smart" technology like a
touchpad and internet connection. It can also be used as a stand-alone
product. It has a prototype nature and will not be ready to be
shipped.

##### 2.2	Product Functions
The system's basic functionalities will be:
+ Tracking of freshness and edibility of fruits and vegetables within
  refrigerators via optical recognition of the food items' changing
  color and shape.
+ Reporting regarding the current status of these food items via a
  web-based user interface.
	+ Prediction of a 'best before date'
	+ Statistical overview via one basic chart visualization.

Please take note of the following graphic for the concept.

![High Level Flow Chart](flowdiagram_highlevel.png)

<div style="page-break-after: always;"></div>

##### 2.3	User Classes and Characteristics
We strive for user-centric systems. Hence we elaborated several user
groups that share the following attitudes:

+ Early adopters. (Technology-savvy and curious users...)
	+ are open-minded and willing to try out unfamiliar products
	+ are likely to provide valuable feedback on functionalities that might be improved or added
	+ appreciate the new product experience as individual benefit
	+ User group importance: high
+ Conscious about food consumption. Users...
	+ want to have an detailed and exact overview of their food consumption
	+ care about food not being wasted
	+ are most likely to be a long-time user if they are satisfied
	+ benefit the product provides: logs of food consumption
	+ User group importance: high
+ Housewives / Homemakers
	+ are in charge of grocery shopping
	+ like to show off new kitchen equipment to peers (marketing)
	+ benefit the product provides: notifies/reminds on what food needs to be bought
	+ User group importance: medium

##### 2.4	Operating Environment
The software will run on a Raspberry Pi 3 Model B with a 1.2GHz Quad
Core ARM Cortex-A53, 1 GB LPDDR2 RAM and a WLAN module. Its operating
system is Raspbian Stretch (Kernel version 4.9) currently accessible
[here](https://www.raspberrypi.org/downloads/raspbian/) and installed
on a 16GB SD card.  Attached to it is a camera module with a 5MP
sensor that is able to take pictures with a resolution of 2592 x 1944
(4:3).

A power bank is used for energy supply.

The hardware will operate within the fridge to reduce the overhead of
cabling.

##### 2.5	Design and Implementation Constraints
+ the RaspberryPi's limited RAM and CPU power might hamper the image processing
+ the knowledge of used programming language(s) might be insufficient
+ the camera module has no auto focus
+ the inside of the fridge is usually not illuminated while the fridge is closed
+ putting the Pi into the fridge for a longer period will be harmful due to humidity and temperature

##### 2.6	User Documentation
Currently no user documentation is planned. We aim to build a user
interface that is user friendly enough to be self-explanatory.

##### 2.7	Assumptions and Dependencies
It is assumed that some open-source machine learning libraries and
packages are available to facilitate the development and coding
process.

<div style="page-break-after: always;"></div>

### 3.	External Interface Requirements

##### 3.1	User Interfaces
The web-based user interface enables the user to view the content of
his refrigerator shelf via a browser. The user may enter additional
data about the food manually or by scanning the barcode, if there is
additional data available the program analyzes this data. The user can
view an up-to-date picture of his fridge content. Additionally in a
later release there will be charts visualizing the average time a food
category stays edible in this fridge comparing it to mean values. This
information is also presented in the form of recommendations like
turning the temperature up or down. The system also includes a social
feature, which enables the user to challenge himself with connected
users (disciplines could be maximum days before something goes bad or
health challenges like 3 fruits eaten a day) and to function as a food
sharing platform. For the food sharing the user can select items which
are then visible to users in the area.

![User Interface](GUI.PNG)

##### 3.2	Hardware Interfaces
The camera is attached to the CSI-2 (Camera Serial Interface Type 2)
of the Raspberry Pi via cable. The power bank is plugged in to the
micro-USB port of the Raspberry Pi. Output will be displayed over
Wi-Fi on user devices with a browser.  TBD - A Barcode Scanner will be
necessary.

##### 3.3	Software Interfaces
The backbone of our system will be a picture recognition and freshness
prediction software. The output regarding status and predictions will
be accessible via a web-based user interface. Hence, for the sake of
efficiency it is feasible to host this website on a local web service
within the Raspberry Pi along with our analytics software.

##### 3.4	Communications Interfaces
The Raspberry Pi is equipped with a Wi-Fi interface. Thus it is able
to offer the web interface provided by a local web server service via
a local Wi-Fi connection. In order to provide a high radio
accessibility range, the Raspberry Pi might be connected to a local
access point. Alternatively, it could also be configured as access
point itself and deliver a one-to-one connection with the end user
device, such as a smartphone or laptop computer.

<div style="page-break-after: always;"></div>

### 4.	System Features
This section describes the functionalities the system provides. It
features the use-cases in the following diagram: 
![Use Cases](UseCasesSmartFridge.PNG)

#### 4.1 Data acquisition and storage

###### 4.1.1	Description and Priority
The camera module placed inside the fridge takes a picture of food
items on one shelf.

Priority: high

###### 4.1.2	Stimulus/Response Sequences
*   User puts fruits in the fridge
*   User activates the SmartFridge software by accessing the user interface via web browser.

###### 4.1.3	Functional Requirements
- REQ-1.1: Take picture within fixed environment
- REQ-1.2: Store images durably
- REQ-1.3: Define region-of-interest (ROI) for each image
- REQ-1.4: Provide access to images and metadata (e.g. timestamps, ID, type of fruit, ROI,...) to other processes
- REQ 1.5: Create timeseries of images for unique fruits

#### 4.2 Detection and tracking of food aging process

###### 4.2.1	Description and Priority
The pictures of the food are categorized by their state of freshness. If there are not enough current pictures, it updates this information to the website.
*   The analytics software must consist of components that can provide the following tasks:
	* Taking pictures with the camera
	* Recognize the food items to be tracked
	* Recognize the aging process with picture analytics techniques (which need to be further elaborated)
	* Predict the food's edibility
	* Constantly improving the prediction process: The user must be able to give simple feedback, if the predicted freshness deviates from its actual state of freshness.
*   A Database about different states of freshness must be accessible.   

Priority: high

###### 4.2.2	Stimulus/Response Sequences
*   The images, taken in 4.1, trigger this process.

###### 4.2.3	Functional Requirements
- REQ 2.1: Extract features from ROIs of timeseries of images
- REQ 2.2: Build aging models for different type of fruits
- REQ 2.3: Compute state of age for individual fruit stored
- REQ 2.4: Update model with user input (e.g. "still fresh", "not fresh anymore", ...)
- REQ 2.5: Update notification database

Priority: low

#### 4.3	Notification of critical food status

###### 4.3.1	Description and Priority
If the food has matured significantly the user gets alerted.   

Priority: medium

###### 4.3.2	Stimulus/Response Sequences
*   The outcomes of 4.2 trigger this event.

###### 4.3.3	Functional Requirements
The notification system (or the website) must be implemented.

- REQ 3.1: Create database for fruits in fridge
- REQ 3.2: Watch database for updates
- REQ 3.3: Notify frontend (e.g. website, RSS-feed, ...)

<div style="page-break-after: always;"></div>

### 5.	Other Nonfunctional Requirements

##### 5.1	Performance Requirements
- REQ N1.1: Modular setup to facilitate separation of computing and
  data acquisition
- REQ N1.2: Reduce energy consumption to less than 25% of the energy
  consumption of the fridge
- REQ N1.3: Minimize exhaust heat that would increase the fridge cooling

##### 5.2	Safety Requirements
- REQ N2.1: Prevent shortlinks within electronics in the fridge environment
- REQ N2.2: Prevent condensation within power supply

##### 5.3	Security Requirements
The data regarding the fridge content must be only accessible by the
fridge-owner.

- REQ N3.1: Prevent unauthorized access to stored data
- REQ N3.2: Prevent unauthorized access to computing hardware
- REQ N3.3: Prevent unauthorized access to connected networks and computers

##### 5.4	Software Quality Attributes
The software must consume few enough resources to work on a
system-on-chip. If this is unattainable, the software must be portable
to a different environment. To prevent a bad user experience it also
must deliver results quickly.

##### 5.5	Business Rules
- REQ N5.1: User controls data storage and usage

### 6. Product Vision and further scenarios
Even though the SmartFridge project is still in a very early stage
with limited functional capabilities, we share a long-term vision of a
of a socially connected food management platform. Our proof-of-concept
highlights that a software project can rely in decisive parts on the
usage of external webservices. Hence, we expect further opportunities
for more sophisticated scenarios that go far beyond our current
scope. Following, our list of further ideas should illustrate some of
the most likely features we aim to implement next.

##### 6.1	Easier Input for food data
Bearing in mind the current ease of image recognition services, we see
significant potential in better user experience by scanning the actual
product barcode. SmartFridge could be able to determine the actual
grocery items, along with their price and best before dates. Hence, it
could determine specific patterns concerning the edibility of fruits
from specific origins. A desirable scenario would be information about
the actual value of current groceries inside the fridge and elaborated
statistical insights on the amount of food that spoiled.

##### 6.2   Recommendations for groceries and recipes
We also believe that the main purpose of data analytics is to make
users aware of things they would not realize on the spot. Hence,
SmartFridge should extensively deliver recommendations concerning the
users' nutritional habits and suggest possible improvements. By
granting access to users' personal calendars, or even fitness
wearables, the quality of recommendations could be adjusted even more
precisely according to the actual health state.

##### 6.3   Delivery service connection and automatic orders
In the advent of grocery delivery services such as Amazon fresh,
SmartFridge could automate the entire grocery shopping process. Users
would benefit by saving their time from crowded supermarkets and
stressful queuing. Moreover, SmartFridge could forecast precisely the
amount of food needed and reduce the amount of spoiled food.

##### 6.4   Voice assistant integration (Siri and Alexa)
Although voice-based assistants currently show many signs of a classic
hype, we believe that in the long term voice assistants will be a
central part of many people's lives. Hence, we aim to integrate
SmartFridge soon with the capabilities to allow voice assistants
insights into our system. Necessary interfaces will be provided.

##### 6.5   Social food sharing platform
SmartFridge could be integrated into food sharing platforms. Users
could allow to share data on current groceries that are unlikely to be
eaten and share these information with nearby SmartFridge users in
town. Since cooking is among the most social activities, we believe a
related social platform offers high potential to save food and bring
people together.

##### 6.6   Data exchange with other kitchen equipment
Kitchen machines like Thermomix show the trend towards cooking
automation. Connecting these tools with SmartFridge could bring new
opportunities for connected cooking.

##### 6.7   Rethinking the interior fridge design
Once the entire grocery order process chain and the actual cooking
becomes more and more automated it might be appropriate to rethink the
actual interior design of a refrigerator. There might be ways to
improve the cooling efficiency. Moreover, we could think of automating
the refilling process as well.
