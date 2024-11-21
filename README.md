# **Token-Relay-Messenger-API**

**Token-Relay-Messenger-API** is a microservice-based system that handles JWT authentication and allows users to receive personalized messages based on their authentication status. The system is composed of multiple services working together to provide the complete functionality.

### **Key Services**
- **Auth Service**: Handles user management, user authentication, JWT generation, and validation.
- **Message Service**: Responds with personalized messages based on the token's validation and user role.
- **User Service**: Manages user registration, login, and handles the user's authentication using auth microservice and message retrieval using message service.
- **Database**: Stores user credentials and other necessary data for the system.

---

## **Features**

- **JWT Authentication**: Secure login and access management using JSON Web Tokens.
- **User Registration (Signup)**: Allow users to create accounts with their details and store hashed passwords.
- **Login and Token Generation**: Users can log in to generate a JWT token.
- **Modular Microservices**: Services operate independently and communicate via HTTP requests.
- **Error Handling**: Returns clear messages for missing or invalid tokens, authentication errors, etc.
- **Simple and Clean API**: RESTful API endpoints that are intuitive to use.
- **Scalability**: The system can scale easily as each service is independently deployable.

---

## **Technologies Used**

- **FastAPI**: A modern Python web framework for building APIs, with asynchronous support.
- **Uvicorn**: ASGI server to run FastAPI applications.
- **PyJWT**: Python library to encode, decode, and validate JWT tokens.
- **Bcrypt**: Password hashing library used to securely store passwords.
- **SQLite (or other databases)**: Database for storing user credentials and session data.
- **SQLAlchemy**: ORM used to interact with the database.
- **python-dotenv**: Loads environment variables from `.env` files.

---

## **Installation Guide**

Follow the steps below to get the project up and running.

### **Step 1: Clone the Repository**

```bash
git clone https://github.com/jeetendra29gupta/Token-Relay-Messenger-API.git
cd Token-Relay-Messenger-API
```

### **Step 2: Create a Virtual Environment (Recommended)**

This ensures that dependencies are isolated and won't affect your global Python setup.

```bash
# For Python 3
python3 -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### **Step 3: Install Dependencies**

Install the required libraries specified in `requirements.txt`.

```bash
pip install -r requirements.txt
```

### **Step 4: Set Up Environment Variables**

Create a `.env` file in the project root directory with the following content:

```env
SECRET_KEY=Secret_Key-2024

ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

USER_SERVICE_URL=http://localhost:8181/
AUTH_SERVICE_URL=http://localhost:8282/
MESSAGE_SERVICE_URL=http://localhost:8383/

SQLALCHEMY_DATABASE_URL=sqlite:///./database.db
```

Make sure to adjust the URLs and any other configurations (like the database URL) for your environment.

### **Step 5: Run the Services**

Use the `main_app_runner.py` script to run and check the services.

#### **Run the Script**

```bash
python main_app_runner.py
```

---

## **User Authentication: Signup & Login**

### **Signup (User Registration)**

Users can sign up by providing a username, email, and password. The password is hashed using **bcrypt**, and the user details are stored securely in the database.

#### **POST** `/user/signup`

**Admin User**

Request Body:
```json
{
  "username": "admin_user", 
  "password": "admin_user_password", 
  "email": "admin_user@email.com", 
  "is_admin": "true"
}
```

Response:
```json
{
  "status_code": 201, 
  "detail": "User created successfully, user ID 1!", 
  "date_time": "2024-11-21 14:31:34"
}
```

**Normal User**

Request Body:
```json
{
  "username": "normal_user", 
  "password": "normal_user_password", 
  "email": "normal_user@email.com", 
  "is_admin": "false"
}
```

Response:
```json
{
  "status_code": 201, 
  "detail": "User created successfully, user ID 2!", 
  "date_time": "2024-11-21 14:32:34"
}
```

### **Login**

Once registered, users can log in with their username and password. Upon successful login, a **JWT token** is generated and returned.

#### **POST** `/user/login`

**Admin User**

Request Body:
```json
{
  "username": "admin_user", 
  "password": "admin_user_password"
}
```

Response:
```json
{
  "status_code": 200, 
  "detail": {
      "token_type": "bearer", 
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbl91c2VyIiwiZXhwIjoxNzMyMTgxNTAxfQ.Bo4e6DWLXv5PhGsKsOTKGNz3fdtwe0vv-j28_2qRLsY", 
      "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbl91c2VyIiwiZXhwIjoxNzMyNzg0NTAxfQ.iLSJn66j_f2XbVEqzoG1PojFHOm5bTjUN419759pMnA"
  }, 
  "date_time": "2024-11-21 14:31:41"
}
```

**Normal User**

Request Body:
```json
{
  "username": "normal_user", 
  "password": "normal_user_password"
}
```

Response:
```json
{
  "status_code": 200, 
  "detail": {
      "token_type": "bearer", 
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJub3JtYWxfdXNlciIsImV4cCI6MTczMjE4MTUwOX0.vFs390HRTCO8MCcQymWgk7-zLJ8RLT6IqB20Ak0_VPc", 
      "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJub3JtYWxfdXNlciIsImV4cCI6MTczMjc4NDUwOX0.zrfcRpv2wXyMZkbLgZETqn79G5HVsUZnMVpk8ehtnXc"
  }, 
  "date_time": "2024-11-21 14:32:41"
}
```
---

## **JWT Authentication**

The JWT token received during login is required for authenticating all subsequent requests to protected endpoints.

### **Usage of JWT Token**

To access the message service or any other protected resources, include the token in the `Authorization` header:

Example with `curl`:

```bash
curl -X 'GET' 'http://localhost:8181/user/message' -H 'Authorization: Bearer JWT_token_here'
```

---

## **Accessing the Services and Testing the System**

Use the `checking_micro_services.py` script to test the interaction between services.

#### **Run the Script**

```bash
python checking_micro_services.py
```

Example Output:

```txt
INFO:root:Making request to http://localhost:8181/user/signup with user details: {'username': 'admin_user', 'password': 'admin_user_password', 'email': 'admin_user@email.com', 'is_admin': 'true'}
INFO:root:Response: {'status_code': 201, 'detail': 'User created successfully, user ID 1!', 'date_time': '2024-11-21 14:31:34'}
INFO:root:Making request to http://localhost:8181/user/signup with user details: {'username': 'normal_user', 'password': 'normal_user_password', 'email': 'normal_user@email.com', 'is_admin': 'false'}
INFO:root:Response: {'status_code': 201, 'detail': 'User created successfully, user ID 2!', 'date_time': '2024-11-21 14:31:36'}
INFO:root:Making request to http://localhost:8181/user/login with user details: {'username': 'admin_user', 'password': 'admin_user_password'}
INFO:root:Response: {'status_code': 200, 'detail': {'token_type': 'bearer', 'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbl91c2VyIiwiZXhwIjoxNzMyMTgxNTAxfQ.Bo4e6DWLXv5PhGsKsOTKGNz3fdtwe0vv-j28_2qRLsY', 'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbl91c2VyIiwiZXhwIjoxNzMyNzg0NTAxfQ.iLSJn66j_f2XbVEqzoG1PojFHOm5bTjUN419759pMnA'}, 'date_time': '2024-11-21 14:31:41'}
INFO:root:Making request to http://localhost:8181/user/message with token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbl91c2VyIiwiZXhwIjoxNzMyMTgxNTAxfQ.Bo4e6DWLXv5PhGsKsOTKGNz3fdtwe0vv-j28_2qRLsY
INFO:root:Response: {'status_code': 200, 'detail': 'Welcome, Admin! You have full access.', 'date_time': '2024-11-21 14:31:47'}
INFO:root:Making request to http://localhost:8181/user/login with user details: {'username': 'normal_user', 'password': 'normal_user_password'}
INFO:root:Response: {'status_code': 200, 'detail': {'token_type': 'bearer', 'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJub3JtYWxfdXNlciIsImV4cCI6MTczMjE4MTUwOX0.vFs390HRTCO8MCcQymWgk7-zLJ8RLT6IqB20Ak0_VPc', 'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJub3JtYWxfdXNlciIsImV4cCI6MTczMjc4NDUwOX0.zrfcRpv2wXyMZkbLgZETqn79G5HVsUZnMVpk8ehtnXc'}, 'date_time': '2024-11-21 14:31:49'}
INFO:root:Making request to http://localhost:8181/user/message with token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJub3JtYWxfdXNlciIsImV4cCI6MTczMjE4MTUwOX0.vFs390HRTCO8MCcQymWgk7-zLJ8RLT6IqB20Ak0_VPc
INFO:root:Response: {'status_code': 200, 'detail': 'Welcome, Authenticated user! Limited access.', 'date_time': '2024-11-21 14:31:53'}
```

---

## **Database Integration**

The system stores user information (including credentials) in a database. By default, **SQLite** is used, but you can switch to a more robust database like PostgreSQL or MySQL by updating the `DATABASE_URL` in the `.env` file.

| Step | Description                                   |
|------|-----------------------------------------------|
| **User Registration** | Store user credentials securely in the database, with password hashing. |
| **Login** | Validate user credentials and generate a JWT token upon successful login. |
| **Database Operations** | Use **SQLAlchemy** to perform operations such as querying, adding users, and authenticating. |

---

## **Error Handling**

The system includes robust error handling for various scenarios, such as:

| Error Scenario                          | HTTP Status | Error Message                                              |
|-----------------------------------------|-------------|------------------------------------------------------------|
| Missing Authorization Token             | `400`       | `"Authorization token is missing"`                         |
| Invalid Token                           | `401`       | `"Invalid token, access denied"`                           |
| Incorrect Username or Password         | `401`       | `"Incorrect username or password"`                         |
| General Internal Server Error           | `500`       | `"Internal server error. Please try again later."`         |

---