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