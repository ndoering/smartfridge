# Distribution of tasks
The following tasks with corresponding responsibilities were identified:

#### Documentation
+ continuously update the documentation (e.g. requirements.md) to the current state
+ also check for spelling, typos etc.
+ *responsible*: all

#### Labeling
+ all available images must be labeled to be sent to the ML API
+ what food is on the image, what is its ripeness
+ *responsible*: all

#### ML API
+ service: [Clarifai](https://www.clarifai.com/)
+ *responsible*: Nils, Jörn

#### Middleware
+ main programming language: Python 3
+ functionalities:
  - take and access photos
  - image processing pipeline (e.g. resolution, separation)
  - Cloud API call, upload, and receive response
  - send data to backend (database)
  - trigger push notification (to slack)
+ *responsible*: all

#### Database
+ implement a database that stores pictures and text
+ connects to middleware and interface
+ preferably sqlite
+ *responsible*: Chris, Liuba

#### Web Interface
+ Webserver Apache & PHP5
+ basic HTML/CSS interface that shows image, notifications and date
+ *responsible*: Jörn, Liuba
