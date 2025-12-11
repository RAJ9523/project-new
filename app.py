from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from bson import ObjectId
import datetime

import numpy as np
import pandas as pd



from flask_cors import CORS
# Initialize Flask app and setup MongoDB connection
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this in production
jwt = JWTManager(app)
CORS(app)
# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/investment_db"
mongo = PyMongo(app)

@app.route("/",methods=["get"])
def main():
    return "Working"

# User Registration Route
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid input, email and password are required'}), 400

    email = data['email'].strip().lower()
    password = data['password']

    users_collection = mongo.db.users
    existing_user = users_collection.find_one({"email": email})
    if existing_user:
        return jsonify({'error': 'Email already exists'}), 400

    users_collection.insert_one({'email': email, 'password': password})
    return jsonify({'message': 'User registered successfully!'}), 201


# User Login Route - Generates JWT token
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid input, email and password are required'}), 400

    email = data['email'].strip().lower()
    password = data['password']
    
    users_collection = mongo.db.users
    existing_user = users_collection.find_one({"email": email})

    if existing_user and existing_user['password'] == password:
        access_token = create_access_token(identity=email, expires_delta=datetime.timedelta(hours=1))
        return jsonify({'message': 'Login successful!', 'access_token': access_token, 'userid': str(existing_user['_id'])}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


# Investment Route
@app.route("/investment", methods=["POST"])
@jwt_required()
def add_investment():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    if not data.get('type') or not data.get('name') or not data.get('amount') or not data.get('returnRate'):
        return jsonify({"error": "Missing required fields"}), 400

    investment = {
        "userId": current_user_id,
        "type": data['type'],
        "name": data['name'],
        "amount": data['amount'],
        "returnRate": data['returnRate'],
        "prediction": data['amount'] * (data['returnRate'] / 100),
        "date": datetime.datetime.utcnow()
    }

    investments_collection = mongo.db.investments
    investments_collection.insert_one(investment)

    return jsonify({"message": "Investment added successfully!", "investment": investment}), 201


# Get all investments for the logged-in user
@app.route("/investments", methods=["GET"])
@jwt_required()
def get_investments():
    current_user_id = get_jwt_identity()
    investments_collection = mongo.db.investments
    investments = investments_collection.find({"userId": current_user_id})

    investment_list = []
    for investment in investments:
        investment_list.append({
            "type": investment['type'],
            "name": investment['name'],
            "amount": investment['amount'],
            "returnRate": investment['returnRate'],
            "prediction": investment['prediction'],
            "date": investment['date']
        })

    return jsonify({"investments": investment_list}), 200


# Delete an investment
@app.route('/investment/<investment_id>', methods=['DELETE'])
@jwt_required()
def delete_investment(investment_id):
    current_user_id = get_jwt_identity()

    investment = mongo.db.investments.find_one({"_id": ObjectId(investment_id)})

    if not investment:
        return jsonify({"error": "Investment not found"}), 404

    if investment["userId"] != current_user_id:
        return jsonify({"error": "You can only delete your own investments"}), 403

    mongo.db.investments.delete_one({"_id": ObjectId(investment_id)})

    return jsonify({"message": "Investment deleted successfully"}), 200


import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler


# Example: Ensure correct feature structure when predicting

@app.route("/predict-stock", methods=["POST"])
@jwt_required()
def predict_stock():
    # Fetch the input value (Open price) from the request
    data = request.get_json()
    open_price = data.get("open_price")

    if not open_price:
        return jsonify({"error": "Open price is required"}), 400
    df = pd.read_csv('GOOGL.csv')  # Your dataset file

# Feature selection: let's assume we're using "Open", "High", "Low", etc.
    features = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    X = df[features]
    y = df['Close']  # Target variable

# Scaling the features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

# Train a model
    model = LinearRegression()
    model.fit(X_scaled, y)


    # Ensure your input matches the features used during training (e.g., "Open", "High", etc.)
    input_data = pd.DataFrame({
        'Open': [open_price],
        'High': [0],   # Replace with valid data if you have it
        'Low': [0],    # Replace with valid data if you have it
        'Close': [0],  # Replace with valid data if you have it
        'Adj Close': [0], 
        'Volume': [0]   # Replace with valid data if you have it
    })

    # Scale the input data using the same scaler used for training
    input_data_scaled = scaler.transform(input_data)

    # Use the loaded model to make a prediction
    predicted_price = model.predict(input_data_scaled)[0]

    return jsonify({"predicted_price": predicted_price}), 200

if __name__ == "__main__":
    app.run(debug=True)
