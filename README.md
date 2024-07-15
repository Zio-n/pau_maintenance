# PAU Maintenance System

## Overview

The PAU Maintenance System is a web application designed to manage maintenance tasks efficiently. This system allows users to create, assign, and track maintenance jobs within an organization. It allows the user to see their shifts. It also supports user roles and permissions, feedback collection, and email notifications for task updates.

## Table of Contents

1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Setup Instructions](#setup-instructions)
   - [Local Development](#local-development)
   - [Production](#production)
4. [Environment Variables](#environment-variables)
5. [Creating Superuser](#creating-superuser)
6. [Email Configuration](#email-configuration)
7. [Important Notes](#important-notes)

## Features

- User Authentication and Role Management
- Task Creation and Assignment
- Shift view
- Feedback Collection
- Email Notifications
- Role-Based Permissions
- Task Status Tracking

## Technologies Used

- Django
- Sqlite - Local
- Tailwind CSS
- JavaScript
- HTML/CSS

## Setup Instructions

### Local Development

1. **Clone the repository:**

   ```bash
   git clone git@github.com:Zio-n/pau_maintenance.git
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

8. **Run Tailwind**
   ```bash
   python manage.py tailwind start
   ```

9. **Run the development server:**

   ```bash
   python manage.py runserver
   ```

### Production

1. **Clone the repository:**

   ```bash
   git clone git@github.com:Zio-n/pau_maintenance.git
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
7. Build Tailwind
   ```bash
   python manage.py tailwind build
   ```

8. **Collect static files:**

   ```bash
   python manage.py collectstatic
   ```

9. **Create a superuser:**

   ```bash
   python manage.py createsuperuser
   ```

10. **Configure your web server (e.g., Gunicorn, Nginx) to serve the application.**

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
