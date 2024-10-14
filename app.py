import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Hardcoded conversion rates for the sake of this example
conversion_rates = {
    'USD': {
        'EUR': 0.85,
        'USD': 1.0,
    },
    'EUR': {
        'USD': 1.18,
        'EUR': 1.0,
    }
}

@app.route('/')
def index():
    return render_template('index.html')  # Render the HTML form

@app.route('/convert', methods=['POST'])
def convert():
    # Get the amount and the currencies from the form
    amount = float(request.form.get('amount'))
    from_currency = request.form.get('from_currency')
    to_currency = request.form.get('to_currency')

    # Perform the conversion
    if from_currency in conversion_rates and to_currency in conversion_rates[from_currency]:
        converted_amount = amount * conversion_rates[from_currency][to_currency]
        return jsonify({
            'success': True,
            'converted_amount': round(converted_amount, 2),
            'from_currency': from_currency,
            'to_currency': to_currency
        })
    else:
        return jsonify({'success': False, 'error': 'Invalid currency conversion'}), 400

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))  # Use the PORT environment variable or default to 5000
    app.run(host='0.0.0.0', port=port)
