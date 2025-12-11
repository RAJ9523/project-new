**Stock Price Prediction Web Application**

## **Project Overview**
The Stock Price Prediction Web App is a full-stack application that leverages machine learning to predict future stock prices based on historical data. The app utilizes a Flask backend, React frontend, and MongoDB for storing user-related data. The machine learning model is built using LSTM (Long Short-Term Memory) neural networks to predict future stock prices. It allows users to input stock data, predict prices, and store/manage their investments securely using JWT-based authentication.

---

## **Technologies Used**
- **Frontend:**
  - React.js
  - Material UI
  - Axios
  - React Router for navigation

- **Backend:**
  - Flask
  - Flask-JWT-Extended for user authentication
  - Flask-PyMongo for MongoDB integration
  - TensorFlow & Keras for building and using machine learning models
  - Scikit-learn for data preprocessing
  - Joblib for saving and loading models

- **Database:**
  - MongoDB for storing user data and investments

- **Deployment:**
  - Flask app can be deployed on any cloud service (Heroku, AWS, etc.)

---

## **Features**

### **Frontend Features:**
- **User Registration and Authentication:** Users can register, login, and securely access the app with JWT authentication.
- **Stock Price Prediction:** Users can input stock prices and receive predictions based on historical data.
- **Investment Management:** Users can manage and store their stock investments, including viewing, adding, and deleting investments.
- **Interactive User Interface:** The app uses Material UI for responsive design and user-friendly interactions.
  
### **Backend Features:**
- **Machine Learning Model:** The backend integrates a pre-trained LSTM model for stock price prediction based on open price data.
- **Investment API:** The backend provides RESTful APIs for creating, fetching, and deleting investment records for users.
- **JWT Authentication:** Ensures secure access and allows for user-specific data management.
- **Flask-PyMongo:** For seamless interaction with MongoDB to store user and investment data.

---

## **Project Structure**
```bash
/stock-prediction-web-app
│
├── /backend # Flask backend
│ ├── /models # Folder to store machine learning models
│ ├── app.py # Main Flask app
│ ├── requirements.txt # Required Python dependencies
│ └── /templates # HTML templates (if any)
│
├── /frontend # React frontend
│ ├── /src
│ │ ├── /components # React components for UI
│ │ ├── /pages # Different pages in React (Home, Login, Register, Predict, etc.)
│ │ ├── App.js # Main React app file
│ │ └── index.js # Entry point for React app
│ └── package.json # NPM package file
│
└── README.md # This file
