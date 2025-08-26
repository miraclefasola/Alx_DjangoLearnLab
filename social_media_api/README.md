User Authentication System (Django)
1. Setup

Clone the repository and create a virtual environment:

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt


Apply migrations:

python manage.py makemigrations
python manage.py migrate


Run server:

python manage.py runserver

2. User Model

We use a custom user model (CustomUser) that extends Django’s AbstractUser.

email is unique and used as the USERNAME_FIELD for login.

bio, profile_picture, and followers fields extend functionality.

followers is a self-referential ManyToManyField with symmetrical=False, so following is one-way like Twitter.

3. Registration & Authentication
Register

We use a RegisterForm (extends UserCreationForm) and a Register view (CreateView) to handle user signup.

After successful signup, users are redirected to the login page.

Validation is built-in (unique email, username).

Login & Logout

Uses Django’s built-in LoginView and LogoutView.

Templates: accounts/login.html.

Token Authentication

A Token is created automatically for each new user using a signal (post_save).

Endpoint: /api-token-auth/ (works with Postman using email/username + password).

4. Custom Authentication Backend

We support login via username OR email.

5. Profile Management
Profile View

Displays the logged-in user and their follower count.

Profile Update

Users can update their first name, last name, email, bio, and profile picture.
Only the logged-in user can edit their own profile.

6. Password Management

We use Django’s built-in views:

reset_password/ → Request reset

reset_password_sent/ → Confirmation sent

reset/<uidb64>/<token>/ → Confirm reset

reset_password_complete/ → Done

password_change/ → Change password while logged in


API Documentation: Posts & Comments

Base URL: /api/
Authentication is required for all operations via Token Authentication:

Authorization: Token <your_token_here>

Posts Endpoint (/api/post/)
1️⃣ List Posts

Method: GET
Description: Retrieve all posts (paginated, 3 per page).

Request:

GET /api/post/
Authorization: Token your_token_here


Response:

{
  "count": 12,
  "next": "http://localhost:8000/api/post/?page=2",
  "previous": null,
  "results": [
    {
      "author": "john_doe",
      "title": "My First Post",
      "content": "This is the content of the post.",
      "created_at": "2025-08-26T16:00:00Z",
      "updated_at": "2025-08-26T16:05:00Z"
    }
  ]
}

2️⃣ Retrieve Post

Method: GET
Description: Get details of a single post by ID.

Request:

GET /api/post/1/
Authorization: Token your_token_here


Response:

{
  "author": "john_doe",
  "title": "My First Post",
  "content": "This is the content of the post.",
  "created_at": "2025-08-26T16:00:00Z",
  "updated_at": "2025-08-26T16:05:00Z"
}

3️⃣ Create Post

Method: POST
Description: Create a new post. author is automatically set to the logged-in user.

Request:

POST /api/post/
Authorization: Token your_token_here
Content-Type: application/json

{
  "title": "New Post Title",
  "content": "Post content goes here."
}


Response:

{
  "author": "john_doe",
  "title": "New Post Title",
  "content": "Post content goes here.",
  "created_at": "2025-08-26T17:00:00Z",
  "updated_at": "2025-08-26T17:00:00Z"
}


⚠ Only the author can update or delete their post.

4️⃣ Update Post

Method: PUT or PATCH
Description: Update an existing post (author-only).

Request:

PUT /api/post/1/
Authorization: Token your_token_here
Content-Type: application/json

{
  "title": "Updated Title",
  "content": "Updated content."
}


Response:

{
  "author": "john_doe",
  "title": "Updated Title",
  "content": "Updated content.",
  "created_at": "2025-08-26T16:00:00Z",
  "updated_at": "2025-08-26T17:15:00Z"
}

5️⃣ Delete Post

Method: DELETE
Description: Delete a post (author-only).

Request:

DELETE /api/post/1/
Authorization: Token your_token_here


Response:

204 No Content

Comments Endpoint (/api/comment/)
1️⃣ List Comments

Method: GET
Description: List all comments (paginated, 5 per page). Filter by post with query parameter /api/comment/?post=1.

Request:

GET /api/comment/
Authorization: Token your_token_here


Response:

{
  "count": 7,
  "next": null,
  "previous": null,
  "results": [
    {
      "author": "jane_doe",
      "post": 1,
      "content": "Nice post!",
      "created_at": "2025-08-26T16:10:00Z",
      "updated_at": "2025-08-26T16:10:00Z"
    }
  ]
}

2️⃣ Create Comment

Method: POST
Description: Add a comment to a post. author is automatically set to the logged-in user.

Request:

POST /api/comment/
Authorization: Token your_token_here
Content-Type: application/json

{
  "post": 1,
  "content": "This is a comment."
}


Response:

{
  "author": "jane_doe",
  "post": 1,
  "content": "This is a comment.",
  "created_at": "2025-08-26T17:05:00Z",
  "updated_at": "2025-08-26T17:05:00Z"
}


⚠ Only the comment author can update or delete their comment.

3️⃣ Update Comment

Method: PUT or PATCH

Request:

PATCH /api/comment/1/
Authorization: Token your_token_here
Content-Type: application/json

{
  "content": "Updated comment content."
}


Response:

{
  "author": "jane_doe",
  "post": 1,
  "content": "Updated comment content.",
  "created_at": "2025-08-26T16:10:00Z",
  "updated_at": "2025-08-26T17:10:00Z"
}

4️⃣ Delete Comment

Method: DELETE

Request:

DELETE /api/comment/1/
Authorization: Token your_token_here


Response:

204 No Content
