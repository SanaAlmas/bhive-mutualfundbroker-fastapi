# 📖 Bhive Mutual Fund Broker FastAPI

This is a **FastAPI-based Mutual Fund Broker Application** that allows users to **manage investments, fetch NAV updates, and interact with RapidAPI** for mutual fund data.

---

## **🔗 GitHub Repository**
[Bhive Mutual Fund Broker](https://github.com/SanaAlmas/bhive-mutualfundbroker-fastapi)

---

## **🚀 Features**
- ✅ **User Authentication** (Signup, Login, Logout)
- ✅ **Investment Portfolio Management** (Add, View, Update, Delete Investments)
- ✅ **NAV Updates** (Fetch & Store NAV details from RapidAPI)
- ✅ **Celery + Redis for Background Tasks** (NAV Updates Every Hour)
- ✅ **Database with MySQL** (SQLAlchemy & Alembic Migrations)

---

## **🛠️ Setup & Installation**

### **1️⃣ Clone the Repository**
```sh
git clone https://github.com/SanaAlmas/bhive-mutualfundbroker-fastapi
cd bhive-mutualfundbroker-fastapi
```

### **2️⃣ Set Up a Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate      # Windows
```

### **3️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
```

### **4️⃣ Create & Configure `.env` File**
Create a `.env` file in the root directory and **add the following**:
```ini
RAPID_API_URL=https://latest-mutual-fund-nav.p.rapidapi.com/latest
RAPID_API_KEY=your_rapidapi_key
RAPID_API_HOST=latest-mutual-fund-nav.p.rapidapi.com
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=your_jwt_secret
JWT_ALGORITHM=HS256
DOMAIN=localhost:8000
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_db_password
MYSQL_DB=mutualfundbroker_db
DATABASE_URL=mysql+pymysql://root:your_db_password@localhost/mutualfundbroker_db
```

---

## **🛠️ Database Setup**

### **1️⃣ Create the Database**
**MySQL**, run:
```sh
mysql -u root -p
CREATE DATABASE mutualfundbroker_db;
```

### **2️⃣ Run Database Migrations**
```sh
alembic revision --autogenerate -m "Initial database migration"
alembic upgrade head
```

---

## **🚀 Running the Application**

### ** Start the FastAPI Server**
```sh
Run main.py from IDE
```
🚀 Server runs at **`http://localhost:8000`**.

### ** Run Celery Worker for NAV Updates**
```sh
celery -A src.scheduler.nav_updator worker --loglevel=info
```

### ** Start Celery Beat (Scheduled Tasks)**
```sh
celery -A src.scheduler.nav_updator beat --loglevel=info
```

---

## **📝 API Documentation**
📚 Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)  
📚 ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)  

---

## **👥 Contributing**
1. **Fork the repository**  
2. **Create a feature branch:**  
   ```sh
   git checkout -b feature-new
   ```
3. **Commit changes:**  
   ```sh
   git commit -m "Added new feature"
   ```
4. **Push to GitHub:**  
   ```sh
   git push origin feature-new
   ```
5. **Open a pull request!**
