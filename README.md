
# Squad Spot

#### Repository Name: nfx-saas-backend

## Introduction:

Squad Spot is an innovative SaaS (Software as a Service) solution designed to streamline administrative tasks. With the power of Django's robust admin panel, Squad Spot serves as the central hub for both internal Squad Spot operations and as a dedicated Company Admin Panel for organizations that subscribe to our SaaS offering.

This versatile platform empowers organizations to efficiently manage their administrative tasks, enhancing productivity and enabling seamless collaboration within the Squad Spot ecosystem. Whether you're a part of the Squad Spot team or an organization benefiting from our SaaS services, Squad Spot simplifies the administrative processes, making your experience smooth and efficient.



## Installation and Configuration

Before you begin, ensure you have met the following requirements:

- Python (version 3.8.10)
- PostgreSQL (version 12.16)

### Step 1: Clone the Repository
git clone https://github.com/Nickelfox/nfx-saas-backend.git

### Step 2: Create a Virtual Environment
python -m venv venv

### Step 3: Activate the Virtual Environment (Windows)
venv\Scripts\activate

### Step 3: Activate the Virtual Environment (macOS and Linux)
source venv/bin/activate

### Step 4: Install Dependencies
pip install -r requirements.txt


### Step 5: Configure Environment Variables
##### 1. Create a `.env` file in the root directory of your project (if it doesn't already exist).
##### 2. Open the `.env` file and add the following environment variables:

#### Database configuration
DATABASE_URL=postgres://yourusername:yourpassword@localhost:5432/yourdbname

#### Django secret key
SECRET_KEY=your_secret_key_here

#### Debug mode (Set to True for development, False for production)

DEBUG=True

#### Mention Host endpoint (do not include an appending slash "/" in the end)
HOST_URL=

#### Mention Company Admin endpoint
COMPANY_ADMIN_URL=

Replace yourusername, yourpassword, yourdbname, and your_secret_key_here with your actual database credentials and Django secret key. You can generate a secret key using Django's secrets module or use any secure method.

Save and close the .env file.



### Step 6: Apply Database Migrations
python manage.py makemigrations

python manage.py migrate

### Step 7: Start the Server
python manage.py runserver

## Usage

- Create a superuser and login
    
    `python manage.py createsuperuser`

- enter email and password.
    
    **`Start the development server`**
        
        python manage.py runserver

- goto Squad Spot Admin panel and login there. 

- Create and Invite Company and internal admins.

- Once the invite_link in either case is accessed, admin user will be shown a password generation form. 

- On generating password, admin user will be shown log in redirecting link through which admin user can goto their admin and panel and login.

-As per the access role defined, they will be able to access and perform actions in squad spot panel.

- A superuser is the user created by django createsuperuser command and has access to everything in Squad Spot Admin panel.

- A company_owner is the admin user that has access to everything in their Company Admin panel.

## Features

Squad Spot offers a range of powerful features to streamline your SaaS user management and administration. Here are some of the key functionalities:

1. **Django Admin Panel Integration**: Utilize the Django admin panel as an efficient administrative interface for managing your Squad Spot data effortlessly.

2. **Company Admin Panel**: Squad Spot includes a dedicated Company Admin Panel, allowing organizations and subscribers to control and customize their experience within the SaaS platform.

3. **User Management**: Seamlessly manage user accounts, permissions, and access control to ensure a secure and tailored experience for each admin user.

4. **Data Security**: Prioritize data security with PostgreSQL as the backend database and robust encryption mechanisms.

## Database Schema

Squad Spot uses a relational database schema managed by Django. Below is an overview of the key database tables and their fields:

#### `Common Fields`

- `id`: Primary key.
- `created_at`: Timestamp for creation.
- `updated_at`: Timestamp for the last update.
- `deleted_at`: Timestamp for deletion (optional).


#### `Company`
    `Specifically for Squad Spot Admin panel`
- `name`: Name of the company.
- `owner_name`: Name of the company owner.
- `owner_email`: Email of the company owner.
- `is_active`: Indicates if the company is active(default=False).
- `invite_link`: Unique invite link.
- `invite_type`: Type of the invite (here it is Company Owner).

#### `Invitation`

- `fullname`: Full name of the invited user.
- `email`: Unique email of the invited user.
- `invite_link`: Unique invite link.
- `invite_type`: Type of the invite (here it can be "Company" member / "Internal" member).
- `company_id`: UUID field that stores company's id (optional).
- `is_active`: Indicates if the invitation is active(default=True).
- `role`: Foreign key to `RoleAccessrole` (optional).

#### `RoleAccessrole`

- `name`: Unique name for the role.
- `description`: Description of the role (optional).
- `role_permissions`: JSON field for role-specific permissions.
- `company_id`: UUID field that stores company's id (optional).

#### `UserUser`

- `full_name`: Full name of the user.
- `email`: Unique email of the user.
- `phone_number`: Phone number of the user (optional).
- `password`: User password (optional).
- `designation`: User designation (optional).
- `is_active`: Indicates if the user is active.
- `is_super_user`: Indicates if the user is a superuser.
- `is_company_owner`: Indicates if the user is a company owner.
- `is_staff`: Indicates if the user is staff.
- `company`: Foreign key to `CompanyCompany` (optional).
- `role`: Foreign key to `RoleAccessrole` (optional).

#### `Client`
    `Specifically for Squad Company Admin panel`
- `name`: Unique name for the client.
- `company_id`: UUID field that stores company's id (optional).

This overview provides the details of database tables and their fields used in Squad Spot.

## Code Flow and Customization

Squad Spot is designed to be flexible and customizable to meet the specific needs of your SaaS project. This section provides an overview of the code flow, the project directory structure, and guidance on how to customize and extend the application.

### Project Directory Structure

Squad Spot follows a typical Django project directory structure. Here are some key directories and files:

- **`squad_spot/`**: This is the Django project's root directory.

- **`apps/`**: Custom Django apps are organized here. You can create your own apps or extend existing ones. This consist of `user`, `company`, `role`, `invitation`and `client`.

- **`common/`**: This has the common used codes in here. This consist of `models.py` having common fields and configuration, `constants.py` having all constants of the project and `helpers.py` having functions and code that are commonly used in the project.

- **`squad_spot/settings.py`**: Django settings file where you can configure various project settings, including database connections, middleware, and third-party integrations.

- **`squad_spot/urls.py`**: URL routing configuration for the project. Also the routes of Squad Spot Admin and Company Admin are defined here. 

- **`custom_static/`**: Static files such as CSS, JavaScript, and images can be placed here for customization. In here all django admin override css files are placed.

- **`templates/`**: HTML templates used for rendering views and all custom templates for admin are placed here.

- **`manage.py`**: Django management script for various tasks like running the development server, applying migrations, and more.

### Code Flow

1. **Company**:
        `for Squad Spot Admin Panel`
   - On adding a company (subscribed orgnisation), a company instance is created with an invite link.
   - Using this invite link the company owner gets onboarded and redirected to their respective Company Admin Panel login.
   - The invite_link once used gets empty and is_active become True on company instance.

2. **Invitation**:
    - This manages admin invitation as per the Panel in use respectively (admin member of Squad Spot Admin Panel and company admin in case of a Company Admin Panel).
    - On adding an invitation, an instance is created with an access role (selected while adding invitation) and also generates an invite link.
   - Using this invite link the admin gets onboarded and redirected to their respective Admin Panel login.
   - The is_active become False once the admin used the invite_link on invitation instance.

3. **Role**:
   - Access control and permissions are managed through the `AccessRole` model, which defines module-specific permissions.
   - The role_permissions lists are specific for Squad Spot and Company Admin Panel.
   - These are maintained in `common/helpers.py` file.

### Customization

#### Custom Files and Roles

Squad Spot provides flexibility through custom files and routes:

1. **Custom Django Admin**: 
    - The two admin panels sites are defined and customized on `custom_admin.py`.
    - There are Indvidual Model Admin classes for each Admin Panel in their respective admin.py files


2. **Dynamic Company Admin Route**: 
- The dynamic routing is handled ny subdomain concept. The subdomain assigned to each company is their company name.

- The Rediection of Subdomain and routing validaytions between Squad Spot and Company Admin panels are maintained as a custom middleware in `squad_spot/subdomain_middleware.py`.

3. **Route Customization**: 
- The routes for both Squad Spot and Company Admin Panel can be customised by updating SQUAD_SPOT_ADMIN_ROUTE_NAME and COMPANY_ADMIN_ROUTE_NAME.

- Make sure that the .env file's COMPANY_ADMIN_URL matches the COMPANY_ADMIN_ROUTE_NAME.


## Tech Stack

**Server:** Python, Django, PostgreSql

