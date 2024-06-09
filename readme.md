# EDCaseload

## Table of Contents

1. Introduction
3. Technologies Used
4. Setup and Installation
5. Usage

## Introduction
This is an app built in Django to store the physiotherapy caseload in the ED through a database built in SQLite using Django models, featuring user authentication and complete database manipulation

## Technologies Used
- Backend: Django 
- Frontend: Tailwind CSS
- Database: Django Models, SQLite

## Setup and Installation
### Prerequisites
- Python (>= 3.x)
- Django (>= 3.x)
- Node.js and npm (for Tailwind CSS)
### Installation Steps
Clone the repository:

```bash
git clone https://github.com/Romanief/edcaseload
cd edcaseload
```
Set up a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```
Install the required Python packages:

```bash
pip install -r requirements.txt
```

Install Node.js dependencies:

```bash
npm install
```

Set up the database:

```bash
python manage.py migrate
```

Run the development server:

```bash
python manage.py runserver
```

Compile Tailwind CSS:

```bash
npx tailwindcss -i ./src/input.css -o ./static/css/output.css --watch
```

Usage

Running the Development Server
```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000 in your browser to see the application running.

Running Tailwind CSS
```bash
npx tailwindcss -i ./src/input.css -o ./static/css/output.css --watch
```

Creating a Superuser
```bash
python manage.py createsuperuser
```
Access the Django admin panel at http://127.0.0.1:8000/admin.


## Styling

Tailwind CSS
Tailwind CSS is used for styling the frontend. The main Tailwind CSS file is located at src/input.css.

Example Configuration

```css
/* src/input.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom styles */
```