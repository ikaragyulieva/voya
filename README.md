# Voya Travel Project

This project is a **travel management application** designed to streamline trip planning, proposal creation, and service management for travel companies.

## Features

- **Client Management:**  
  Store and manage client information.
  
- **Trip Requests and Proposals:**  
  Handle incoming trip requests with detailed group, date, and destination information.  
  Generate customized proposals for each trip request.

- **Service Management:**  
  Define and manage services like accommodations, transport, activities, and guides.  
  Dynamically filter services by city and other parameters.

- **User Roles and Permissions:**  
  Support for different user roles such as employees and clients.  
  Secure authentication and role-based access control.

- **Multi-Language and Currency Support:**  
  Easily define supported languages and currencies for trips.

- **Extensible Architecture:**  
  Modular design with reusable components and services.

---

## Project Structure

- **`voya` Directory**:
  - Core application logic.
  - **Sub-apps**:
    - `clients`: Manage client profiles and related data.
    - `employees`: Employee management and role definitions.
    - `proposals`: Handle trip proposals.
    - `services`: Define and manage available services.
    - `users`: User authentication and management.
    - `common`: Shared utilities and base classes.
  - **Configuration**:
    - `settings.py`: Central Django configuration, including integration with `.env`.
    - `urls.py`: URL routing definitions.
    - `wsgi.py` and `asgi.py`: Deployment interfaces for WSGI and ASGI servers.

- **Templates and Static Files**:
  - `templates`: Contains HTML files for UI rendering.
  - `static` and `staticfiles`: Include CSS, JavaScript, and image assets.

- **`requirements.txt`**:
  - List of dependencies for the project.

- **`.env`**:
  - Environment variables for sensitive information like `SECRET_KEY` and database credentials.

---

## Installation

### Prerequisites

- Python 3.8 or higher
- PostgreSQL (or your preferred database backend)
- Virtual environment tool (`venv`, `virtualenv`, etc.)

### Setup

1. **Clone the Repository**:  
   ```bash
   git clone <repository-url>
   cd voya
   
2. **Create a Virtual Environment:**:  
   ```bash
   python -m venv .venv
   source .venv/bin/activate    # Linux/Mac
   .venv\Scripts\activate       # Windows

3. **Install Dependencies:**:  
   ```bash
   pip install -r requirements.txt
   
4. **Set Up Environment Variables:**:  
- Create a `.env` file in the `voya` directory:
   ```bash
   SECRET_KEY=your-secret-key
   DB_NAME=your-database-name
   DB_USER=your-database-user
   DB_PASSWORD=your-database-password
   DB_HOST=localhost
   DB_PORT=5432
  
5. **Run Migrations:**:  
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   
6. **Collect Static Files:**:  
   ```bash
   python manage.py collectstatic
   
7. **Run the Server:**:  
   ```bash
   python manage.py runserver
   
8. **Access the Application:**:
   Open `http://127.0.0.1:8000/` in your browser.

---

## Usage

Once the application is set up and running, here’s how you can interact with its various features:

### 1. **Homepage**
   - Visit the homepage at `http://127.0.0.1:8000/`.
   - The homepage serves as the entry point for accessing different features based on user roles (e.g., client, employee, admin).
   - **Account creation options** are available here:
     - **Company Creation:** Clients must first create a **Company Profile** using the **Create Company** section on the unauthenticated homepage. 
       - During company creation, clients are required to provide:
         - **Company Name**
         - **Tax ID**
         - **Address**
         - **Contact Information**
       - Once created, this company profile is added to the database and can be used during client account creation.
     - **Clients:** New client accounts can be created directly from the **New Client** section on the unauthenticated homepage. Note:
       - Clients must provide a **Tax ID** of an existing company in the database during account creation.
       - This Tax ID links the client to their company profile.
     - **Employees:** Employee accounts must be created via an unpublished URL, which is provided to employees by the admin. Note:
       - Once an employee creates an account, it must be manually activated by an admin before it can be used.

### 2. **Company Module**
   - The **company profile** must be created **before** a client can create an account. This ensures that clients can associate their accounts with an existing company.
   - **Creating a Company Profile:**
     - Clients can create a company profile using the **Create Company** section on the unauthenticated homepage.
     - Provide company details, including:
       - Name
       - Address
       - Contact Information
       - **Tax ID** (used to link clients to their respective companies).
   - **Client-Company Association:**
     - When a client creates an account, they must provide the Tax ID of their company.
     - The system validates the Tax ID and assigns the client to the corresponding company profile.
   - **Managing Companies:**
     - Employees and admins can view, edit, or delete company profiles as needed from the admin panel or other management interfaces.

### 3. **Authentication**
   - Log in using your credentials. The system supports different user roles:
     - **Clients:** Limited access to their proposals and trip details.
     - **Employees:** Full access to manage clients, trips, services, and proposals.
   - If you do not have an account, refer to the **Account Creation** section above.

### 4. **Trip Requests**
   - Employees can create new trip requests for clients, capturing details such as:
     - Group information (e.g., nationality, age range, group type).
     - Trip dates and duration.
     - Destinations and transportation preferences.
   - Clients can view their trip requests and submit additional observations if required.

### 5. **Trip Proposals**
   - Employees can generate trip proposals based on trip requests.
   - Customize each proposal by selecting services such as accommodations, transport, activities, and guides.
   - Use the **Add Row** feature to add more service items for a trip, selecting services by city and dynamically populating their price.

### 6. **Service Management**
   - Admins and employees can define and manage services such as:
     - **Accommodations**: Hotels, resorts, etc., with price variations for high and low seasons.
     - **Transport**: Public and private transport options.
     - **Activities**: Guided tours, tickets, and other local experiences.
     - **Guides**: Assign local guides with their price details.
   - Filter services by city to ensure only relevant options are displayed during proposal customization.

### 7. **Dynamic Fields**
   - Dropdowns for services and cities are dynamically populated based on the selected section and user inputs.
   - Prices are automatically displayed based on the selected service, ensuring accurate billing details.

### 8. **Admin Panel**
   - Access the admin panel at `/admin/` for advanced management features.
   - Manage:
     - **Users:** Add or remove employees and clients, assign roles.
     - **Companies:** Add or update company profiles for client association.
     - **Services:** Add, update, or remove service entries.
     - **Trips and Proposals:** View and modify all client-related data.
   - **Employee Account Activation:** Activate new employee accounts from this panel after they are created via the unpublished URL.

### 9. **Data Export and Analysis**
   - Export client, trip, or service data for offline analysis.
   - Use the admin panel or implement custom scripts to generate reports.

---

### Example Workflow for Employees:
1. **Log In:** Use employee credentials.
2. **Create a Trip Request:** Capture client requirements.
3. **Generate a Proposal:** Select services and customize details.
4. **Submit Proposal:** Save and send the proposal to the client.
5. **Modify Services:** Adjust services based on client feedback.

### Example Workflow for Clients:
1. **Create Company Profile:** Use the **Create Company** section on the homepage.
2. **Create Account:** After creating the company, use the **New Client** section to create an account. Provide the Tax ID of the company you work for.
3. **Log In:** Use client credentials to access the system.
4. **View Proposals:** Access the trip proposals prepared by the agency.
5. **Submit Feedback:** Provide additional observations or changes to the trip.

---

## Security Measures

- **Environment Variables**:
  Use `.env` for sensitive data and ensure `.env` is added to `.gitignore`.
- **Database Credentials:**
  Store credentials securely in `.env`.
- **Secret Key:**
  Rotate the secret key if it is compromised.

---

## Contributing

- Fork the repository and submit pull requests for improvements.
- Ensure code quality with PEP 8 compliance.

---

## License

This project is licensed under the MIT License.