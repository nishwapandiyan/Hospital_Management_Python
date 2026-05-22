# Hospital Management System

A comprehensive desktop application for managing hospital operations including patient management, doctor management, appointments, and billing. Built with Python, Tkinter, and MySQL.

## Features

- **Patient Management** - Add, update, and manage patient records
- **Doctor Management** - Manage doctor profiles and information
- **Appointment Management** - Schedule and track patient appointments
- **Billing System** - Process and manage patient billing
- **Dashboard** - Central hub for navigating all modules
- **Secure Login** - User authentication system
- **Database Integration** - MySQL backend for data persistence

## Project Structure

```
HOSPITAL_MANAGEMENT/
├── main.py                          # Application entry point
├── README.md                         # Project documentation
├── requirements.txt                 # Python dependencies
├── assets/                          # Screenshots and media files
├── database/                        # Database configuration
│   └── hospital_db.sql             # Database schema
├── gui/                            # Tkinter GUI modules
│   ├── __init__.py
│   ├── login.py                    # Login window
│   ├── dashboard.py                # Main dashboard
│   ├── patient.py                  # Patient management module
│   ├── doctor.py                   # Doctor management module
│   ├── appointment.py              # Appointment management module
│   ├── billing.py                  # Billing module
│   └── reports.py                  # Reports module
└── hospital_management_system/     # Core system modules
    ├── __init__.py
    ├── database.py                 # Database connection handler
    └── .env                        # Environment variables
```

## Requirements

- Python 3.x
- MySQL Server
- tkinter (usually included with Python)
- tkcalendar
- mysql-connector-python
- python-dotenv

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd HOSPITAL_MANAGEMENT
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database**
   - Open `hospital_management_system/.env`
   - Update database credentials:
     ```
     DB_HOST = localhost
     DB_USER = root
     DB_PASSWORD = your_password
     DB_NAME = hospitaldb
     ```

5. **Create the database**
   - Import `database/hospital_db.sql` into MySQL:
     ```bash
     mysql -u root -p hospitaldb < database/hospital_db.sql
     ```

## Usage

Run the application:
```bash
python main.py
```

The login window will appear. Use your credentials to access the hospital management system.

## Modules

### Login Module (gui/login.py)
Handles user authentication and access control.

### Dashboard (gui/dashboard.py)
Central navigation hub providing access to all system modules.

### Patient Management (gui/patient.py)
- Add new patients
- Update patient information
- View patient records
- Search and filter patients

### Doctor Management (gui/doctor.py)
- Register doctors
- Manage doctor details
- Track doctor specializations

### Appointment Management (gui/appointment.py)
- Schedule appointments
- Manage appointment dates and times
- Link patients to doctors

### Billing (gui/billing.py)
- Generate billing records
- Calculate charges
- Print bills

### Database Module (hospital_management_system/database.py)
Handles all MySQL database connections and operations.

## Environment Variables

Create a `.env` file in `hospital_management_system/` folder:

```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=hospitaldb
```

## Technologies Used

- **Frontend:** Tkinter (Python GUI framework)
- **Backend:** Python
- **Database:** MySQL
- **Additional Libraries:** 
  - mysql-connector-python
  - tkcalendar
  - python-dotenv

## File Information

- **main.py** - Application entry point that initializes the database connection and launches the login window
- **requirements.txt** - Lists all Python package dependencies
- **database/hospital_db.sql** - SQL script with database schema and tables
- **assets/** - Contains application screenshots

## Contributing

Feel free to fork this project and submit pull requests for any improvements.

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please create an issue in the repository.