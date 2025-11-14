## Online Event Ticketing System
By Mikayla Hubbard & Luanne Plemmons

**Frontend / Backend:** Django  
**Data:** SQL type (mySQL)

## Functional Requirements
*1. User Roles:* Customer, Administrator.  
*2. Authentication:* Login system with role-based access.  
*3. Customer Features:*
- Browse list of events and available seats.
- Book tickets for chosen event.
   - Cancel booking before the event date.
   - View booking history.
  
*4. Administrator Features:*  
   - Add, update, or delete events.
   - Set ticket prices and seat limits.
 

## Non-Functional Requirements
- Security: Password protection and safe data handling.
- Reset Password (optional)
- Usability: Simple and intuitive booking interface.
- Reliability: Prevent overbooking and ensure accurate transactions.
- Performance: Support at least 200 concurrent bookings.

## Extended Features (Optional)
- Seat map visualization for selection.
- Payment gateway simulation.
- Email confirmation for bookings.

## Landing Page:
- Simple “This is who we are”
- Login/Register (Section to define account type - administrator or customer)

## Customer View:
- Book New event (list of events & details)
- Each event card -> displays individual event info -> book event button & form (potential email confirmation) & some sort of payment type
- Payment portal (future feature)
- Current bookings (list & current details) 
	- unregister button -> removes booking
- History of bookings (list)
- Logout (button -> popup -> “Are you sure you want to logout?”)
- Person icon -> click -> list of personal details (future feature)
	- potential for editing info (future feature)
	- potential for changing password (ff)

## Administrator View:
- Upcoming events (list)
	- List of events (reports of ticket sales)
- for each event -> details page (Editing button, Delete button, only if you are the creator
- Add events (form)
	- Title
	- Description
	- Picture
	- Date/time (prevent double booking)
	- Set ticket prices
	- Number of seats
	- Location (building, room) (prevent double booking)
	- More details (optional)
- History of events (list)
- Logout (button -> popup -> “Are you sure you want to logout?”)
- Person icon -> click -> list of personal details (future feature)
	- Potential for editing info (future feature)
	- Potential for changing password (future feature)

## Forms:
Login/Register  
Logout  
Editing  
Registering for a booking  
Canceling booking  
Creating a booking (list of seats)  
Deleting booking  
Contact Us  

## Views And Templates:

* = on navbar

- landing page

	- the only page a non-logged in viewer can see
	- Explains the app and prompts to either login or register

- Register page
- login page


- For User:
  - home *
  - Upcoming Events - events they haven't signed up for *
  - Current bookings - events they are signed up for *
  - Individual Event - details of the specific event
  - Logout button (not a view) *

- For Manager:
  - home *
  - upcoming events *
  - Create New event
  - Edit event
 
# How to run the project (Dev.)

## 1. Download a local copy of the project**

		wget https://github.com/LuannePlem/OnlineEventTicketingSystem.git

## 2. Set up the Database (This bit is complicated, sorry)**

   		https://docs.djangoproject.com/en/5.2/ref/databases/ 

   So you have 3 options:

   1. Use Django's Automatic Database
   2. Create and connect your own SQL database
   3. Create a **completely Identical** mySQL database that matches the code in Github
  
**Option 1**

Use the automatic Django database.
In `OTS_MAIN/OTS/settings.py`, change the database settings to look like this:
```
   DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```
Then run the following:
```
	python manage.py makemigrations
	python manage.py migrate
```
**Option 2**

Creating your own SQL Database however you would like.
Then, in `OTS_MAIN/OTS/settings.py`, edit the database settings
```
	DATABASES = {
	      'default': {
	          'ENGINE': 'django.db.backends.mysql', # Replace mySQL with the type of SQL you are using
	          'NAME': 'OTS_db',  # Replace with your MySQL database name
	          'USER': 'shared_user',    # Replace with your MySQL username
	          'PASSWORD': 'SuperSecretPassword123?', # Replace with your MySQL password
	          'HOST': 'localhost',       # Or your MySQL server's IP/hostname
	          'PORT': '3306',           # Default MySQL port
	      }
	}
```
Then run the following:
```
	python manage.py makemigrations
	python manage.py migrate
```

**Option 3**

Create a new SQL database ensuring that it's properties match the settings in 
`OTS_MAIN/OTS/settings.py` ***exactly***

Then run the following:
```
	python manage.py makemigrations
	python manage.py migrate
```


### 4. Run the server**

	Ensure you are in the OTS_MAIN Folder

   		python manage.py runserver
   or
   
   		python3 manage.py runserver
  

