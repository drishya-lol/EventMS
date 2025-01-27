# EventMS

Project I am doing as a part of my internship task with MindRisers.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

EventMS is a project developed as part of an internship task with MindRisers. This project is intended to be a one-stop place for managing, registering, and rating events and vendors involved in the event.

## Features

1. **User Authentication and Access Control**
   - **User Registration, Login, and Logout:**
     - Enable login/logout functionalities using Django’s built-in authentication system.
     - Implement password reset functionality.
   - **Role-Based Access Control:**
     - Define roles such as Admin, Event Planner, Vendor, and Client.
     - Use Django's Group and Permissions to assign access rights based on user roles.
     - Admins have full access, while Event Planners, Vendors, and Clients have restricted views and actions based on role.

2. **Event Management**
   - **Create and Manage Event Listings:**
     - Allow event planners to create detailed event listings with attributes like event name, date, time, location, event description, and maximum attendees.
     - Enable event updates and modifications by the event planner or admin.
   - **Event Search and Filter:**
     - Provide search functionality for clients and attendees to find events based on event type, date, location, or keyword.
     - Implement filters for event categories (weddings, conferences, parties, concerts), pricing, and available seats.
   - **Event Categories:**
     - Define event categories and allow organizers to classify events into multiple categories.

3. **Vendor Management**
   - **Vendor Profiles and Records:**
     - Maintain a database of approved vendors and service providers (e.g., catering, sound systems, decorators).
     - Allow vendors to create and update their profiles, including services offered, pricing, and contact details.
   - **Vendor Assignments:**
     - Assign vendors to specific events based on event needs and schedules.
     - Allow vendors to view their assigned events and manage their availability.
   - **Vendor Performance Tracking:**
     - Track vendor performance metrics such as punctuality, service quality, and client reviews for evaluation.

4. **Attendee Management**
   - **Event Registration:**
     - Allow clients to register for events through a user-friendly interface.
     - Implement form validation to ensure proper input of attendee details (name, email, ticket type, etc.).
   - **Attendee Tracking:**
     - Maintain a record of attendee registrations, including contact information and ticket types.

5. **Ticketing and Payment**
   - **Ticket Sales and Reservations:**
     - Implement online ticket sales for events, allowing clients to purchase or reserve tickets.
     - Create ticket types (e.g., VIP, general admission) and pricing tiers for each event.
     - Generate unique ticket codes for each purchase to facilitate event entry.
   - **Invoicing and Receipts:**
     - Automatically generate invoices and receipts for purchases made by clients.
     - Allow users to download or print their invoices and payment confirmations.
   - **Refunds and Cancellations:**
     - Implement refund policies and allow users to cancel tickets based on event-specific rules.

6. **Event Logistics**
   - **Logistics Management:**
     - Allow event planners to manage logistics such as equipment rentals, catering services, venue bookings, and transportation.
     - Track expenses related to event logistics and allocate budgets accordingly.
   - **Inventory Tracking:**
     - Track inventory such as sound equipment, stage setups, or decorative items required for events.

7. **Customer Reviews and Feedback**
   - **Event Reviews:**
     - Allow attendees to leave reviews for events they attended, rating factors such as venue, logistics, and overall experience.
     - Implement a review moderation system where reviews are approved by admins before they are made public.
   - **Feedback for Vendors:**
     - Enable attendees to provide feedback specifically for vendors they interacted with during the event.
     - Provide vendors with aggregated ratings to assess their performance.

8. **Reports and Analytics**
   - **Attendance Reports:**
     - Generate reports on event attendance, showing the number of tickets sold and attendees present.
     - Provide planners with insights into attendee demographics and preferences.
   - **Revenue Reports:**
     - Provide event planners and admins with detailed revenue reports based on ticket sales, vendor fees, and overall event costs.
   - **Dashboard Analytics:**
     - Provide role-based analytics dashboards for event planners and admins, showing upcoming events, revenue trends, and logistical needs.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/drishya-lol/EventMS.git
   ```
2. Navigate to the project directory:
  ```bash
  cd EventMS
  .venv\Scripts\Activate
```
3. Install the required dependencies:
  ```bash
  pip install -r requirements.txt
```
## Usage
  To run the project, use the following command:
    ```bash
    python manage.py runserver
    ```
## Contributing
  Contributions are welcome! Please follow these steps to contribute:
  
  Fork the repository.
  Create a new branch (```git checkout -b feature-branch```).
  Commit your changes (```git commit -m 'Add some feature'```).
  Push to the branch (```git push origin feature-branch```).
  Open a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Code
Feel free to modify any section as needed. Let me know if you need further assistance!
