# Firestore cloud functions 



##### Introduction 
Cloud Firestore (In Beta at time of writing) is a flexible, scalable database for mobile, web, and server development from Firebase and Google Cloud 
Platform. Like Firebase Realtime Database, it keeps your data in sync across client apps through realtime listeners and 
offers offline support for mobile and web so you can build responsive apps that work regardless of network latency or 
Internet connectivity. 

More info: https://firebase.google.com/docs/firestore/


use cases for cloud functions:
1. Notify users when something happens
2. realtime maintainance and cleanup
3. execute extensive tasks which cannot be done on the client
4. integrate with third party services
4. increment/decrement counters upon some event 

More info: https://firebase.google.com/docs/functions/use-cases

##### Announcement
Google finally announced support for python 3.7 runtime although the docs aren't updated yet.

##### Scenerio
Consider the following structure
```
finalDb/
      account_1/
            projects/
                    closedTaskCount (integer)
                    createedTime (timestamp)
                    creator (string)
                    deleted (boolean)
                    description (string)
                    projectDueDate (timestamp)
                    projectTags (map)
                    startDate (timestamp)
                    taskCount (integer)
                    
            tasks/
                    attachments (map)
                    createdTime (timestamp)
                    creator (string)
                    deleted (boolean)
                    dueDate (timestamp)
                    lastUpdatedTime (timestamp)
                    project (string)
                    owner (string)
                    status (string)
                    subTasks (map)
                    tags (map)
                    taskName (string)
                    taskUsers (map)
                    
            messages/
            tags/
            users/
            activities/
            .....
            
           
      account_2/
      account_3/
      .....
      account_n/
```

##### Description
1. users can create tasks with 5 statuses : open, closed, pause, yet to start, suspended
2. A task can exist independently without being included in the project
3. closed task count is incremented when task changes its state from open to closed and decremented when its state changes
from closed to open
4. taskcount is incremented/decremented whenever a new task is added or removed respectively


##### Goal

To increment/decrement the counters i.e; taskCount and closedTaskCount in projects collection whenever a task is 
created and references a project


##### Reason to use cloud function
To achieve consistency across all clients using transactions.
Whenever a user makes changes, it must be consistent across all users and since transactions fail to execute whenver a
device is offline, cloud functions are used to keep sanity with the value of counters when the device is online.

More info on transactions: https://firebase.google.com/docs/firestore/manage-data/transactions


##### Trigger a firestore cloud function
The Cloud Functions for Firebase SDK exports a functions.firestore object that allows you to create handlers tied to specific events.
Cloud Firestore supports create, update, delete, and write events.

More info: https://firebase.google.com/docs/firestore/extend-with-functions


##### Steps to create a cloud function in python 3.7
1. Goto google cloud console > cloud functions
2. Click on create function
3. Fill in function details such as function name, RAM.
4. Select appropriate Trigger (in this case: cloud firestore)
5. Select event type (create, update or delete or write)
6. Provide a Document path to listen to changes.
   In this case: finalDb/{orgId}/tasks/{taskId}
7. select source code type (inline editor/zip)
8. Select runtime as python 3.7
9. Provide the entry point i.e the function to start execution.
