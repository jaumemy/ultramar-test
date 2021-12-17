## Backlog

*(17/12/21)*

Make this app reusable **(Done)**

Make tests (backend / ~~frontend~~) **(Done)** 

Make export results to XLS / PDF **(Done)** ~~or import XLS files~~

Make the frontend attractive **(Done)**

Make API REST with Django Rest Framework **(Done)**

Make a little application with Vue / ~~React~~ **(Done)**

  

## Useful info

Once you have cloned the repo you can do this:

  
```bash

# Install dependencies

pip install -r requirements.txt

 # Start the server

python manage.py runserver

# Test the application

python manage.py test

```


##### Urls

To see the **front end** go to [http://localhost:8000/](http://localhost:8000/)              
_*At the time it only lets you read data and download files_        

To  **login** go to [http://localhost:8000/admin](http://localhost:8000/admin)            
_*At the time no login feature has been implemented in the custom front end_              
_*You can use the test user, username=test.user,  password=ultramar_           

To see the **django rest framework api** go to [http://localhost:8000/api](http://localhost:8000/api)            

To see a basic **swagger ui** go to [http://localhost:8000/docs](http://localhost:8000/docs)              



## Considerations
The next assumptions has been made when creating the transport app:     
- A booking can have multiple vehicles, or none        
- A vehicle can be in only one booking simultaneously, or in none       
- A vehicle can be associated/disassociated from a booking at any time         

## Improvements
Some improvements would be the addition of import XLS files feature and improve the front end (both visually and functionally).         


<br>
<br>
<br>



**_2021, Jaume Montané_**