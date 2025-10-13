from flask import Flask
import math, random
app = Flask(__name__)

@app.route('/')
def home():
    # simulate CPU work
    for i in range(10**6):
        math.sqrt(random.randint(1, 100))
    return "Hello from AutoScaleX! (Dynamic Scaling Demo)"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
