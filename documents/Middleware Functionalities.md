# Middleware Functionalities Pseudo Code
The document shall serve as a basis for later discussions. I suggest the following template to describe our code functions.

###Program Part Name.

######function_name
Purpose:
Argument:
Return Value:
Algorithm:

----------------------------------

###Creation of a model with a Machine Learning Cloud Service

###Support script within the operating system
Purpose: Capturing Images on a regular basis. (For instance every hour). It's a shell script which runs aside our core program in order to be more robust.

###Core Middleware Application

Initializations:
+ Create database connection

######ask_mlcloud
Purpose: For each new image, the function calls the ML-service to check its edibility.
Argument: One Image.
Return Value: Probability of the fridges content's freshness.
Algorithm:
+ Check for latest picture
+ Use specific web API call and send the image to the provider
+ Receive answer (chance of edibility) 
+ return chance of edibility

######log_edibility
Purpose: The function logs the actual edibility state to a database (whose shape and technology has to be designed yet).
Argument: ask_mlcloud return value, timestamp, picture name
Return Value: void
Algorithm:
+ Create database connection
+ Log edibility result, timestamp, picture name

