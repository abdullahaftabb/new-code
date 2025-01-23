from flask import Flask, request, jsonify, render_template, url_for, make_response, session
import requests
import uuid
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24) 
app.config['SESSION_COOKIE_SECURE'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30) 
@app.route('/')
def index():
    return render_template('index.html', locations = None)

@app.route('/location', methods=['GET', 'POST'])
def get_location():
    print('coming from the front end')
    search_query = request.args.get('search') or request.form.get('search') or request.json.get('search')
    print(search_query)
    if not search_query:
        return jsonify({'error': 'Search parameter is required'}), 400
    
    print('#'*50)
    
    url = "https://locations.api.hlag.cloud/api/locations"
    headers = {
        "x-token": 'eyJhbGciOiJSUzI1NiIsImtpZCI6InpaX3V5cWNMZEwtZFZSaTdkclRPbEZIMEctazJ2M2MtYnJ1bVJERVdwSVUiLCJ0eXAiOiJKV1QifQ.eyJleHAiOjE3Mzc2NDM4NTYsIm5iZiI6MTczNzYzMzA1NiwidmVyIjoiMS4wIiwiaXNzIjoiaHR0cHM6Ly9obGFnd2VicHJvZC5iMmNsb2dpbi5jb20vNjNkZjhlNzEtMDYxMi00OTMyLWE2ZGUtMmEwZjVhYTNjNzhjL3YyLjAvIiwic3ViIjoiVTQwNzk2NSIsImF1ZCI6IjY0ZDdhNDRiLTFjNWItNGI1Mi05ZmY5LTI1NGY3YWNkOGZjMCIsImFjciI6ImIyY18xYV9zaWdudXBfc2lnbmluIiwibm9uY2UiOiIwMTk0OTJmZS00N2FiLTc2ZjYtYjUxNy01ODY0NzFkZjI1NGEiLCJpYXQiOjE3Mzc2MzMwNTYsImF1dGhfdGltZSI6MTczNzYzMzA1MywianRpIjoiZDgyZjcyNmEtMWJjZC00NzQ4LWFhNzctOGZkNjJjNmVkZGU2IiwibmV3VXNlciI6dHJ1ZSwiam9iVGl0bGUiOiJib29rZXIiLCJleHRlbnNpb25fVUlEIjoiVTQwNzk2NSIsInRpZCI6IjYzZGY4ZTcxLTA2MTItNDkzMi1hNmRlLTJhMGY1YWEzYzc4YyIsInBhc3N3b3JkRXhwaXJlZCI6ZmFsc2V9.Mvmvht_Tvo0h2tkna0l_UHKkaYHvN7ltbWKtE8FsGVu9DTdZL-4gnYxWW-3TnZA6IXnwrab1V0eIUv1MNGsFC8kCbKMKo-hzcN6txB9xTARohrjYMvwqDmhRF-AkeMHZ03Mpss84FxqCHefJ0qkYfysFFpc6riPcbUE0TDt2wlRL1TAsURDXEtf9uMoIIea1RumF-pQW3h-X86BChzHCkCk6Y69qqNOZKtYwS-NyTCFYP93sM8ut69GnsdnV_cmc3-W8Gbe-7Tl9vUSL3etFAgkx0oF2hemK5ZyyqKiRLVN7OUZ3eUEwA3ptrl8k7SXoA1Og1vcksjJe4gkZ1_TMCw',
    }
    params = {
        "search": search_query,
        "limit": 20,
        "orderType": "seaportsfirst"
    }

    try:
        print('sending request to the backend')
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        location_data = response.json()
        print(location_data)
        if request.method == 'GET':
            response = make_response(jsonify(location_data))
            response.headers.add('Access-Control-Allow-Origin', '*')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
            response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
            return response
        return render_template('index.html', locations=location_data)

    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": f"HTTP error occurred: {http_err}"}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

@app.route('/api/send_offer', methods=['GET', 'POST'])
def send_offer():
    print('*' * 50)
    random_uuid = str(uuid.uuid4())
    print(random_uuid)
    try:
        print(' i am inside the try block')
        response = make_response(random_uuid)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    except requests.exceptions.HTTPError as http_err:
        return jsonify({"error": f"HTTP error occurred: {http_err}"}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"An error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(port=8007)