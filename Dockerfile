FROM python:3.9-slim
WORKDIR /app

# Step 1: Copy the updated requirements.txt (which now includes pandas, numpy, scikit-learn)
COPY requirements.txt .

# Step 2: Install all dependencies for the Flask app AND the AI Anomaly Detector
RUN pip install --no-cache-dir -r requirements.txt

# Step 3: Copy the rest of the application files (app.py, scripts/, etc.)
COPY . .

# Step 4: Run the main Flask application
CMD [ "python", "app.py" ]
