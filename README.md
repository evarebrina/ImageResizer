ReadMe
-
>ImageResizer is an asynchronous web service for resizing images. It allows to:
>- Set a task for resizing an image
>- Get a result of the task

#### 1. Setting a task
To set a task you need to make GET request to specified URL:

`/api/resize/&PARAMETERS`

Where PARAMETERS are:
 - image_url - a valid url to jpeg or png image
 - width - desired width of the image
 - height - desired height of the image
 
 In reply to such a request you will receive a reply in JSON format.  
 When task was ran successfully server returns a JSON object with status and task id fields:
 
 ```
 {
    'status': 'ok',
    'task_id': '92a50e4d-42e3-4106-98b8-f27eac4b57e9'
 }
 ```
  
Example of error JSON response:
 ```
 {
    'status': 'error',
    'error_code': 'wrong_width',
    'message': 'Width is not an integer'
 }
 ```
 
#### 2. Getting a result
 To get a result of the running task you need to make GET request to specified URL:
 
 `/api/details/TASK_ID`
 
 Where TASK_ID is an id provided in JSON object by the server after successfully running the task.
 
 When the id is correct server returns a JSON object with status field
 and fields depending on the status
 
 Example of JSON response:
 ```
 {
    'status': 'pending'
 }
 ```
 Possible JSON fields:
 
 Status value | Other values
 ------ | ------
 `pending` | ~
 `successful` | `url` - url to the sized image
 `failed`| `error_code` - code of the error `message` - message for the error


Original and sized images are stored on the sever for at least 10 minutes from the moment
of setting the task.

  Service contains user interface which uses the service API and runs on '/'
  
  ###Running the project
  
  You need python3 for this project. To run run the following commands:
```
virtualenv -p python3 ImageResizer
cd ImageResizer
. bin/activate
git clone https://vadimrebrin/ImageResizer.git ImageResizer
cd ImageResizer
pip install -r requirements.txt
python3 manage.py runserver
```
These will run Django server with the ImageResizer project