from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Retrieve the API key from environment variables
API_KEY = os.getenv('API_KEY')

# Build the API URL using the API key
API_URL = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/'

@app.route('/', methods=['GET', 'POST'])
def index():
    conversion_result = None
    error_message = None
    if request.method == 'POST':
        amount = request.form.get('amount')
        from_currency = request.form.get('from_currency')
        to_currency = request.form.get('to_currency')
        
        if not amount or float(amount) <= 0:
            error_message = "Please enter a valid amount."
        else:
            try:
                response = requests.get(API_URL + from_currency)
                data = response.json()
                conversion_rate = data['conversion_rates'][to_currency]
                conversion_result = round(float(amount) * conversion_rate, 2)
            except Exception as e:
                error_message = f"An error occurred: {str(e)}"

    currencies = ['USD', 'EUR', 'GBP', 'INR', 'AUD', 'CAD', 'JPY']
    return render_template('index.html', currencies=currencies, conversion_result=conversion_result, error_message=error_message)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use the PORT environment variable or default to 5000
    app.run(host='0.0.0.0', port=port
