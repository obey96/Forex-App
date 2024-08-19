from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# API details : URL of the conversion API and the access key for authetication

API_URL = 'https://api.exchangerate.host/convert'
ACCESS_KEY = '6bbdccc40399d4e5646e01cebefa16f8'

#Define the route for the root URL, handling both GET and POST request 
@app.route('/', methods=['GET', 'POST'])
def index():
    # Check if the request method is POST(form submitted)
    if request.method == 'POST':
        # Get the currency and amount inputs from the form
        converting_from = request.form.get('converting_from').upper() # convert to uppercase for consistency
        converting_to = request.form.get('converting_to').upper() #convert to uppercase for consistency 
        amount = float(request.form.get('amount')) #Convert the amount to a float
        
        # API request with access key / Construct the API request with the necessary parameters
        try:
            # Make GET request to the API with the provided access key, currencies, and 
            response = requests.get(f'{API_URL}?access_key={ACCESS_KEY}&from={converting_from}&to={converting_to}&amount={amount}')
            data = response.json()

            # Debugging: Print the response data  to the console for inspection
            print("API Response:", data)

            # Check if the request was successful (STATUS CODE 200) and process the data
            if response.status_code == 200:
                converted_amount = data.get('result')
                if converted_amount is not None:
                    # Render the template with the converted amount and input data
                    return render_template('index.html', converted_amount=converted_amount,
                                           converting_from=converting_from, converting_to=converting_to, amount=amount)
                else:
                    # If the conversation result is NONE, display an error msg
                    error = f"Conversion failed. Please check the currency codes and try again."
                    return render_template('index.html', error=error)
            else:
                # If the API request was unsuccessful, display an error message
                error = f"Error: {data.get('error', 'Unknown error occurred')}"
                return render_template('index.html', error=error)
        except requests.exceptions.RequestException as e:
            # Handle any exceptions that occur during the API request (e.g., network issues)
            error = f"Request failed: {e}"
            return render_template('index.html', error=error)
    # If the request method is GET (page initially loaded), render the form without any data
    return render_template('index.html')
# Run the flask app in debug mode to allow easy debugging during development 
if __name__ == '__main__':
    app.run(debug=True)
