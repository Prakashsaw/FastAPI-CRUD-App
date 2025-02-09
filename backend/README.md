# **Books Store** 📚  
A FastAPI CRUD app where users can create an account and manage their favorite books.  

## 📌 GitHub Repository  
```bash
https://github.com/Prakashsaw/FastAPI-CRUD-App
```

## 🌍 Live Demo  
```bash
https://fastapi-crud-app.netlify.app
```

---

## **📚 Description**  
Books Store is a **full-stack CRUD application** built with FastAPI, React.js, and MongoDB. Users can register, log in, and manage their favorite books securely. The app features **JWT-based authentication, email verification, session management, and password recovery**.  

---

## **🛠 Tech Stack**  

### **Frontend**  
- JavaScript, React.js, Bootstrap, CSS  

### **Backend**  
- Python, FastAPI, FastAPI-Mail  

### **Database**  
- MongoDB  

---

## **🚀 Getting Started**  

### **Step 1: Clone the Repository**  
```bash
git clone https://github.com/Prakashsaw/FastAPI-CRUD-App.git
```

### **Step 2: Navigate to the Project Directory**  
```bash
cd FastAPI-CRUD-App
```

### **Step 3: Install Dependencies for Frontend & Backend**  

#### **Frontend Setup**  
```bash
cd frontend
npm install
```

#### **Backend Setup**  
1️⃣ Create a virtual environment:  
```bash
python -m venv your_virtual_env_name
```
2️⃣ Activate the virtual environment:  
```bash
# Windows
your_virtual_env_name\Scripts\activate

# macOS/Linux
source your_virtual_env_name/bin/activate
```
3️⃣ Install dependencies:  
```bash
pip install -r requirements.txt
```

---

### **Step 4: Configure Environment Variables**  
Create a `.env` file in the `backend` directory and add the following environment variables:  

```bash
MONGO_URI = 
DB_NAME = 

JWT_SECRET_KEY = 
JWT_ALGORITHM = 
JWT_ACCESS_SECRET_KEY = 
JWT_ACCESS_EXPIRY_MINUTES = 
JWT_REFRESH_SECRET_KEY = 
JWT_REFRESH_EXPIRY_DAYS = 

USER_SESSION_EXPIRY_MINUTES = 

MAIL_USERNAME = 
MAIL_PASSWORD = 
MAIL_FROM = 
MAIL_FROM_NAME = 
MAIL_PORT = 
MAIL_SERVER = 
MAIL_STARTTLS = 
MAIL_SSL_TLS = 
USE_CREDENTIALS = 
VALIDATE_CERTS = 

FRONTEND_HOST = http://localhost:3000 or https://your-deployed-domain.com
APP_NAME = 
```

---

### **Step 5: Run the Application**  

#### **Start the Backend Server**  
- **If the virtual environment is not activated, activate it first:**
```bash
# Windows
your_virtual_env_name\Scripts\activate

# macOS/Linux
source your_virtual_env_name/bin/activate
```
- **Run the FastAPI server:**
```bash
uvicorn main:app --reload
```

#### **Start the Frontend React App**  
```bash
cd frontend
npm run start
```

📌 **Now, the Books Store app should be running locally!**

---

## **✨ Features**  

- **User Registration & Login** with complete validation.  
- **Email Verification:** Users receive a confirmation link via email to verify their account.  
- **Secure Authentication & Authorization:**  
  - Middleware ensures protected routes using JWT tokens.  
  - Refresh tokens allow users to renew access tokens without re-logging in.  
- **Forgot Password:** Users can reset their password if forgotten.  
- **Session Expiry Handling:**  
  - If an access token expires, users can refresh it without logging in again.  
- **CRUD Operations:**  
  - Users can add, edit, delete, and manage their favorite books.  
- **User Profile Management:**  
  - Users can update their profile details and change their password.  

---

## **📸 Screenshots**  

| Feature | Screenshot |
|---------|-----------|
| **User Sign Up** | ![Sign Up](/frontend/images/1-SignUp.png) |
| **Email Verification Link Sent** | ![Verification Email](/frontend/images/2-SignUp-Success-Email-Verification-link-sent.png) |
| **Email Verification Confirmation** | ![Verify Email](/frontend/images/3-Verify-email.png) |
| **User Login** | ![Login](/frontend/images/4-Login.png) |
| **Forgot Password** | ![Forgot Password](/frontend/images/5-Forgot-Password.png) |
| **Reset Password Link Sent** | ![Reset Password Link](/frontend/images/6-Reset-Password-Lint-Sent-Success.png) |
| **Reset Password** | ![Reset Password](/frontend/images/7-Reset-Password.png) |
| **User Dashboard** | ![Home Page](/frontend/images/8-Home-Page-User-Details.png) |
| **Session Expiry & Token Refresh** | ![Session Expiry](/frontend/images/9-Session-Expired-Refresh-Token.png) |

---

## **👨‍💻 Made By**  
- [@Prakashsaw](https://github.com/Prakashsaw)  

---

## **🐜 License**  
This project is licensed under the **MIT License**.  

---

### **🌟 If you like this project, don't forget to star the repo!** ⭐  

