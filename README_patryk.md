# jbl-chat

Endpoints:
    - /chat/login/' [POST] anyallow
    - /chat/logout/' [POST] authenticated
    - /chat/users/' [GET] authenticated - display list of all user except request user
    - /chat/message/<int:receiver_id>/' [POST] authenticated - sending msg to user data = {"mesage": "text"}
    - /chat/message/<int:receiver_id>/' [GET] authenticated - display all messages with receiver

For test app you comment

`python jbl_chat/manage.py test chat`