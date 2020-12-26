# How To Run
------------------------------------------------------------------------
- Install dependency with `pip install -r requirements.txt`
- run django make migrations `python manage.py makemigrations`
- run django migrations `python manage.py migrations`
- create django superuser with `python manage.py createsuperuser`
- run django server with `python manage.py runserver`
- Test the API as follows

- Sign up the user with `signup` API first and get the token

- User API
----------
1. http://127.0.0.1:8000/signup/
2. http://127.0.0.1:8000/login/
3. http://127.0.0.1:8000/exam/start/
4. http://127.0.0.1:8000/exam/submit/
    
- Admin API
------------
1. http://127.0.0.1:8000/question/upload/
2. http://127.0.0.1:8000/question/list/
3. http://127.0.0.1:8000/question/update/<int:que_id>/
4. http://127.0.0.1:8000/question/delete/<int:que_id>/,
5. http://127.0.0.1:8000/result/list/


For POST APIs use the below body template

# API
----------------------------------------------------------------------
1. Sign up POST API
    `
    {
        "username": "user"
        "password": "password"
    }
    `
    

2. Login POST API
    get the token from response and use in the all subsequent request as follows
    `Authorization Token <key>` in the header

3. store result API (Submit exam) POST API
    body:
    `
    [
        {
            "id": 7,
            "question": "This is test question",
            "que_type": "organizational",
            "selected_option": "strongly_agree"
        },
        {
            "id": 6,
            "question": "What is your last name",
            "que_type": "communicational",
            "selected_option": "agree"
        },
        {
            "id": 5,
            "question": "What is your name",
            "que_type": "helping_others",
            "selected_option": "agree"
        }   
    ]
    `
-------------------------------------------------------------------------

# Note
    
3. All admin API must to be tested with django admin