# PAU Maintenance System

## Overview

The PAU Maintenance System is a web application designed to manage maintenance tasks efficiently. This system allows users to create, assign, and track maintenance jobs within an organization. It also supports user roles and permissions, feedback collection, and email notifications for task updates.

## Table of Contents

1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Setup Instructions](#setup-instructions)
   - [Local Development](#local-development)
   - [Production](#production)
4. [Environment Variables](#environment-variables)
5. [Creating Superuser](#creating-superuser)
6. [Tailwind CSS Setup](#tailwind-css-setup)
7. [Email Configuration](#email-configuration)
8. [Important Notes](#important-notes)

## Features

- User Authentication and Role Management
- Task Creation and Assignment
- Feedback Collection
- Email Notifications
- Role-Based Permissions
- Task Status Tracking

## Technologies Used

- Django
- PostgreSQL
- Tailwind CSS
- JavaScript
- HTML/CSS

## Setup Instructions

### Local Development

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/pau-maintenance-system.git
   cd pau-maintenance-system
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**

   Ensure you have PostgreSQL installed and running. Create a database and update the `.env` file with your database credentials.

5. **Create a `.env` file in the root directory with the following content:**

   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   ALLOWED_HOSTS=localhost, 127.0.0.1

   DATABASE_NAME=your_database_name
   DATABASE_USER=your_database_user
   DATABASE_PASSWORD=your_database_password
   DATABASE_HOST=localhost
   DATABASE_PORT=5432

   EMAIL_HOST=smtp.your_email_provider.com
   EMAIL_HOST_USER=your_email@example.com
   EMAIL_HOST_PASSWORD=your_email_password
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   ```

6. **Apply database migrations:**

   ```bash
   python manage.py migrate
   ```

7. **Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

### Production

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/pau-maintenance-system.git
   cd pau-maintenance-system
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**

   Ensure you have PostgreSQL installed and running. Create a database and update the `.env` file with your database credentials.

5. **Create a `.env` file in the root directory with the following content:**

   ```env
   SECRET_KEY=your_secret_key
   DEBUG=False
   ALLOWED_HOSTS=your_production_domain

   DATABASE_NAME=your_database_name
   DATABASE_USER=your_database_user
   DATABASE_PASSWORD=your_database_password
   DATABASE_HOST=your_database_host
   DATABASE_PORT=5432

   EMAIL_HOST=smtp.your_email_provider.com
   EMAIL_HOST_USER=your_email@example.com
   EMAIL_HOST_PASSWORD=your_email_password
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   ```

6. **Apply database migrations:**

   ```bash
   python manage.py migrate
   ```

7. **Collect static files:**

   ```bash
   python manage.py collectstatic
   ```

8. **Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

9. **Configure your web server (e.g., Gunicorn, Nginx) to serve the application.**

## Environment Variables

Ensure the `.env` file includes the following variables:

```env
SECRET_KEY=your_secret_key
DEBUG=True or False
ALLOWED_HOSTS=localhost, 127.0.0.1 or your production domain

DATABASE_NAME=your_database_name
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_HOST=localhost or your database host
DATABASE_PORT=5432

EMAIL_HOST=smtp.your_email_provider.com
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

## Creating Superuser

After setting up the project, create a superuser by running:

```bash
python manage.py createsuperuser
```

Follow the prompts to set up your superuser account.

## Tailwind CSS Setup

Tailwind CSS is used for styling the application. To spin up Tailwind CSS, follow these steps:

1. **Install Tailwind CSS:**

   ```bash
   npm install tailwindcss
   ```

2. **Initialize Tailwind CSS:**

   ```bash
   npx tailwindcss init
   ```

3. **Configure Tailwind in `tailwind.config.js`:**

   ```javascript
   module.exports = {
     purge: ['./templates/**/*.html', './static/js/**/*.js'],
     darkMode: false, // or 'media' or 'class'
     theme: {
       extend: {},
     },
     variants: {
       extend: {},
     },
     plugins: [],
   }
   ```

4. **Run Tailwind CLI to build styles:**

   ```bash
   npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch
   ```

## Email Configuration

Ensure you have configured your email settings in the `.env` file:

```env
EMAIL_HOST=smtp.your_email_provider.com
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

Update the email URLs in the email templates to match your production domain.

## Important Notes

- Update the URLs in the email templates to match your production domain.
- Ensure the SMTP credentials are set up correctly in the `.env` file.
- Test the email functionality to confirm that emails are being sent and received as expected.

By following these instructions, you should be able to set up and run the PAU Maintenance System both locally and in production. If you encounter any issues or have any questions, please refer to the documentation or reach out to the development team.
