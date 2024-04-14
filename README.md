# Django Application Template

Welcome to my Django Boilerplate repository! This boilerplate provides a well-organized structure for kickstarting your Django applications. It comes packed with a plethora of features, including a fully-featured authentication system, custom middleware for handling response formats, custom exception handlers, renderers, paginator, user model, permissions, utilities, validators, wrappers, managers, serializers, signals for user profile creation, and much more.<br><br>

## Features

- **Well-organized structure:** The repository is structured in a clean and organized manner, making it easy navigate, maintain and manage for local, testing and production stages.
- **Authentication system:** A fully-featured authentication system is included and it comes with a custom user model and model manager for enhanced flexibility and customization. This authentication system uses a jwt and otp authentication and verification system.
- **Renderers:** Custom renderer also made available to format responses according to your application's needs if you decide not to use the custom middleware.
- **Custom exception handlers:** Easily manage exceptions within your Django application with custom exception handlers if you decide not to use the middleware provided.
- **Middleware:** A custom middleware is provided for handling API responses, ensuring that the application's responses maintain a standard format for both responses and exceptions.
- **Wrappers:** Custom wrapper function included to revert back to default response handling systems and ignore middleware. Can be implemented as decorator on view function.
- **Paginator:** Pagination functionality is integrated and supports the middleware functionality to handle large datasets efficiently.
- **Permissions:** Custom permission for allowing access to views based on the user and user profile status. This can be customized to fit application requirements.
- **Utilities:** Utility functions are provided to send mails and mail attachments.
- **Validators:** Custom validators help ensure data integrity and consistency.
- **Signals:** Signals are set up for user profile creation, to automate user profile creation upon user registration.<br><br>

## Getting Started

To get started with the Django Boilerplate, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/django-boilerplate.git
   ```

   <br>

2. **Create virtual environment:**
   Create a virtual environment to keep your project isolated

   ```bash
   python -m venv venv
   ```

   <br>

3. **Install dependencies:**
   Fill in the project dependencies as required. The requirements folder contains text file with dependencies for local, tests and development environment all inheriting from base.txt. Customize as you see fit.

   ```bash
   pip install -r local.txt
   ```

   <br>

4. **Set local environment variables:**
   This template has been setup to use python-decouple to manage env variables so all you have to do is go to .env file and set the necessary env variables. You can continue add more as you see fit

   ```bash
    CONFIG_MODE=local
    SECRET_KEY=your_secrey_key
    DEFAULT_FROM_EMAIL=Mail <no-reply@example.com>
    EMAIL_HOST_USER=user@example.com
    EMAIL_HOST_PASSWORD=userpassword123
   ```

<br>

5. **Configure settings:**
   Configure settings for the project. Local, test and production settings all inherit from the base settings and the mode can be set from the .env file i.e once you set CONFIG_MODE=local, it will automatically make use of local.py as settings. Other config mode are test and production. Base.py has also been set up such that if CONFIG_MODE is either local or test, DEBUG=True and for production, DEBUG=False. Customize all settings as you see fit to meet application requirements.

6. **Run migrations:**

   ```bash
   python manage.py makemigrations
   ```

   <br>

   ```bash
   python manage.py migrate
   ```

7. **Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

8. **Start the development server:**

   ```bash
   python manage.py runserver
   ```

9. **Begin developing your application:**
   You're all set! Start building your Django application using this boilerplate as a foundation.

Feel free to customize this template further to suit your specific needs and preferences.
