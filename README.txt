This is a Django project for Twitter APIs.
Follow the following steps to run the project:
Step 1: Make sure you have Python3 installed in your machine.
Step 2: (Optional) Install and activate a Python3 based virtual environment.
Step 3: Navigate inside the Project directory and Run the command to install all the dependencies:
        pip3 install -r requirements.txt
Step 4: Run the following commands to start the project by migrating the database and running the server as:
        python manage.py makemigrations
        python manage.py migrate
        python manage.py runserver



Descriptions of APIs:

Authentication: I have used JWT based authentication service for Signing in the users to the Project.

To create a new user:
localhost:8000/auth/adduser/
                    Make a POST request with the following data: "email", "first_name", "last_name", "password"
                    Here, the first_name and last_name are optional

                    (If you are logged in) Make a GET request(with JWT token in the header as stated in next point) to check your login details such as email, first_name and last_name.


To login using email and password:

Obtain the JWT token that will be used in the header to provide the access(authentication) to APIs.
localhost:8000/get-jwt-token/
                    To obtain the token, make a POST request to this API with "email" and "password" field in data.

Now copy the token that you obtained and add it in the request Headers with key as "Authorization" and its value as "JWT token_code". Here, token_code is the token that you copied.
With this JWT token in Headers, you can access all the APIs for this particular user.


APIs for Follower related actions:

localhost:8000/user/add_follower/         (Add the JWT token for the User's authentication to this API)
                  Make a GET request to this API to retrieve the list of Followers for the current logged in user.

                  Make a POST request to this API with "follow_email" field in data to follow the user with the given email.
                  Example: "follow_email": "anurag.g16@iiits.in"

                  Make a PUT request to this API with the same "follow_email" field to unfollow the user in follow_email field.

Summary of localhost:8000/user/add_follower/    ---> GET request to retrieve the list of followers, POST request to follow the user with email in "follow_email" field, PUT request to unfollow the user with email in "follow_email" field



To create, read and delete Tweets:

localhost:8000/user/tweet/              (Add the JWT token for the User's authentication to this API)
                  Make a GET request to this API to retrive the user's own tweet, i.e, the tweets that he has created till now.

                  Make a POST request to this API, with "tweet" field in key and tweet text as value, to create a Tweet.
                  Example: "tweet": "Flutter 1.0 is released now!"

                  Make a DELETE request to this API, with "id" field that contains the tweet id, to delete the tweet from the database. You can know the Tweet id for your tweets by making GET request to this API.
                  Example: "id": 5        Here, 5 is the Tweet id.

Summary of localhost:8000/user/tweet/       ---> Get request to retrieve all his tweets, POST request to create a Tweet, DELETE request to delete a Tweet.


To read all the tweets created by the users whom the current user follows(All the tweets that should apper on user's dashboard):

localhost:8000/user/all_tweet/         (Add the JWT token for the User's authentication to this API)
                  Make a GET request to this API to retrive all the tweets created by the users who are followed by current logged in user.
