# Library Management System

A Library Management System (LMS) developed in two approaches:  

1. Using **Python** for both frontend and backend.  
2. Using **Jaseci Language (Jac)** for both frontend and backend.  

The system handles library management tasks like book inventory, member records, issue/return workflows, and intelligent automation with Jac.
![image](https://github.com/user-attachments/assets/6998b14e-c510-4fd6-9246-39d7a7134e39)

---

## Features

- Add, update, delete, and search books.
- Manage members and staff details.
- Book issue, return, and reservation functionalities.
- Notifications for overdue books.
- Intelligent automation of workflows (Jac approach).

---

## Tech Stack

### Approach 1: Python-based System  
- **Frontend**: Python (Flask/Django templates with HTML, CSS, and JavaScript).  
- **Backend**: Python (Flask/Django RESTful APIs).  
- **Database**: MySQL/PostgreSQL.

### Approach 2: Jac-based System  
- **Frontend**: Jac (UI definitions and workflows).  
- **Backend**: Jac walkers, sentinels, and actions.  
- **Database**: Jaseci built-in or integrated external DB (optional).  

---

## Installation and Setup

### Prerequisites:
- Install [Python](https://www.python.org/).  
- Install [Jaseci](https://github.com/Jaseci-Labs/jaseci).  
- Install [MySQL](https://www.mysql.com/) or [PostgreSQL](https://www.postgresql.org/) if using a relational database.  
- Install Git for version control.  

---

### Approach 1: Python-based System

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/library-management-system.git
   cd library-management-system
2.Run the backebnd
 ```bash
    cd backend
    uvicorn backend:app --reload
 ```
3.Run the frontend
  ```bash
    cd frontend
    streamlit run main.py 
