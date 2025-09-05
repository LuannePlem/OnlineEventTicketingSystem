## Online Event Ticketing System
By Mikayla Hubbard & Luanne Plemmons

**Frontend:** React  
**Backend:** Django  
**Data:** SQL type  

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
   - Generate reports of ticket sales.

## Non-Functional Requirements
- Security: Password protection and safe data handling.
- Reset Password (optional)?
- Usability: Simple and intuitive booking interface.
- Reliability: Prevent overbooking and ensure accurate transactions.
- Performance: Support at least 200 concurrent bookings.

## Extended Features (Optional)
- Seat map visualization for selection.
- Payment gateway simulation.
- Email confirmation for bookings.

## Landing Page:
- “This is who we are”
- Login/Register (Section to define account type - administrator or customer)

## Customer View:
- Book New event (list of events & details)
- Click on event -> individual event page (price) -> book event button & form (potential email confirmation) & some sort of payment type
- Payment portal (future feature)
- Current bookings (list & current details) 
	- unregister button -> popup => “Are you sure you want to unregister?”
- History of bookings (list)
- Logout (button -> popup -> “Are you sure you want to logout?”)
- Person icon -> click -> list of personal details
	- potential for editing info (future feature)
	- potential for changing password (ff)

## Administrator View:
- Upcoming events (list)
	- List of events (reports of ticket sales)
- click on event -> details page (Editing button, reports of ticket sales)
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
- Person icon -> click -> list of personal details
	- Potential for editing info (future feature)
	- Potential for changing password (future feature)

## Forms:
Login/Register
Logout
Editing
Registering for a booking
Canceling booking
Creating booking (list of seats)
Deleting booking
Contact Us
