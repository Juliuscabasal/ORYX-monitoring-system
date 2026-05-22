ORYX is a full-stack, comprehensive web application designed to streamline and centralize internal department workflows. It replaces manual tracking methods by providing a secure, unified platform to monitor Purchase Orders (PO), Purchase Requests (PR), and User Acceptance Testing (UAT) lifecycles.

Designed with user experience and data integrity in mind, ORYX features a modern, responsive interface and robust backend reporting tools to help stakeholders keep track of critical operational data, timelines, and documentation.

🚀 Key Features
Comprehensive Workflow Tracking:

Purchase Requests (PR): Track requests by location (e.g., Desktop Support, R&D), itemized breakdowns, and urgency statuses.

Purchase Orders (PO): Monitor delivery statuses, Delivery Receipt (DR) and Sales Invoice (SI) numbers, and item-by-item status updates.

User Acceptance Testing (UAT): Log testing durations, personnel, billing status, and total costs.

Dynamic Itemized Data Entry: Intuitive, dynamically expanding forms allow users to add multiple items, quantities, and descriptions to a single PR or PO record without leaving the page.

Document Management System: Securely upload, view, and manage attached files and documents directly linked to specific PO, PR, or UAT records.

Automated Excel Reporting: Built-in analytics engine utilizing Pandas to instantly generate and download beautifully formatted, date-filtered Excel spreadsheets for auditing and reporting.

Modern, Interactive UI: Built with Tailwind CSS, featuring real-time search filtering, dynamic dashboard summaries, interactive popup modals, and a custom right-click context menu for rapid record editing and deletion.

Secure Authentication: Protected routes with hashed passwords and session management ensuring only authorized personnel can access or modify company data.

💻 Tech Stack
Backend: Python, Flask, Flask-Login

Database: MySQL, SQLAlchemy (ORM)

Data Processing & Export: Pandas, OpenPyXL

Frontend: HTML5, Tailwind CSS, Vanilla JavaScript, FontAwesome Icons

File Handling: Werkzeug (Secure File Uploads)
