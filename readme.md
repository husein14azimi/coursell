### comment api endpoints (drf-comments python package)

List Comments: `GET /comments/`

Create Comment: `POST /comments/`

Retrieve Comment: `GET /comments/<id>/`

Update Comment: `PUT /comments/<id>/`

Delete Comment: `DELETE /comments/<id>/`


### how to create and get comments:

* creation:
    * send a post request to `comments/` url.
    * write the json object in the request body.
* list:
    * send a get request to `/comments/?content_type=<model_name>&object_pk=<pk>`