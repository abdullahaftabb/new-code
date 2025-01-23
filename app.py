from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate
from flask_mail import Mail, Message
from langchain_groq import ChatGroq
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import time
import uuid
import jwt
import os
from groq import Groq
import groq
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.llm import LLMChain
import pandas as pd
from typing import Optional
from pydantic import BaseModel, Field
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

load_dotenv()

app=Flask(__name__)
app.secret_key = os.urandom(24) 
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/rankvizdatabase'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ethicalgan@gmail.com'
app.config['MAIL_PASSWORD'] = 'rehg hjfx tauh zrof'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.secret_key = "supersecretkey"
mongo = PyMongo(app)
mail = Mail(app)



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

def generate_token(user):
    payload = {
        'email': user['email'],
        'time': time.time()
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    session.clear()
    if 'messages' in app.config:
        app.config['messages'] = []
    email = request.form['email'].strip()
    password = request.form['password']
    print(email)
    print(password)
    user = mongo.db.users.find_one({'email': email})
    if user and check_password_hash(user['password'], password):
        session['email'] = email
        session['token'] = generate_token(user)
        print('current_token is ',session['token'])
        return jsonify(status="success", redirect_url=url_for('index'))
    else:
        return jsonify(status="error", message="Invalid credentials")

@app.route('/logout')
def logout():
    session['token'] = None
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('home'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email'].strip()  
        user = mongo.db.users.find_one({'email': email})  
        
        if user:
            token = str(uuid.uuid4())
            mongo.db.password_reset_tokens.insert_one({
                'email': email,  
                'token': token,
            })

            reset_url = url_for('reset_password', token=token, _external=True)

            msg = Message('Password Reset Request',
                          sender='ethicalgan@gmail.com',
                          recipients=[email])
            msg.body = f'Click the following link to reset your password: {reset_url}'

            try:
                mail.send(msg)
                flash('A password reset link has been sent to your email.', 'info')
            except Exception as e:
                flash(f'Error sending email: {str(e)}', 'danger')
        else:
            flash('Email not found. Please check the email address.', 'danger')

        return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    print(token)
    if request.method == 'POST':
        new_password = request.form['password']
        reset_token = mongo.db.password_reset_tokens.find_one({'token': token})

        email = reset_token['email']
        hashed_password = generate_password_hash(
            new_password, method='pbkdf2:sha256')
        mongo.db.users.update_one({'email': email}, {'$set': {'password': hashed_password}})
        mongo.db.password_reset_tokens.delete_one({'token': token})
        flash('Password has been reset successfully! You can now log in.')
        return redirect(url_for('home'))
    return render_template('reset_password.html', token=token)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email'].strip()
        password = request.form['password']
        print(email)
        print(password)
        existing_user = mongo.db.users.find_one({'email': email})

        if existing_user:
            flash('Username already exists. Please choose a different username.')
            return redirect(url_for('signup'))
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        mongo.db.users.insert_one({'email': email, 'password': hashed_password})
        flash('Signup successful! Please log in.')
        return redirect(url_for('home'))
    return render_template('signup.html')


GROQ_API_KEY = "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"
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

llm = ChatGroq(model="llama3-8b-8192")
client = Groq()

source_selection_prompt = ChatPromptTemplate.from_template(
    """Given the following question, determine the most appropriate data source based on the content of each source:
        1. not a general greeting: For questions about those which are not only general greeting like sending stuff , about rates, mainly from one place to another, etc.

       2. general greeting:
       For questions that don't require specific document data or can be answered with general Greeting.
       - Normal Greeting like Hi, Hello, How are you, etc.

    3. Print:
    for questions like print the data, print the invoice , show the invoice, generate a quotation, make a quotation etc.

    Respond with exactly one of these options:
    - "not a general greeting" for questions about those which are not only general greeting like sending stuff , about rates, mainly from one place to another, etc.
    - "print" for questions like print the data, print the invoice , show the invoice, generate a quotation, make a quotation etc.
    - "general greeting" For questions that don't require specific document data or can be answered with general greeting or general inquires. 

    Question: {input}

    Your response (not_only_a_general_greeting/general_greeting/print) only:"""
)

def select_source(question):
    selection_chain = source_selection_prompt | llm
    response = selection_chain.invoke({'input': question})
    return response.content.strip().lower()

class Person(BaseModel):
    origin: Optional[str] = Field(description="source for the first place (starting location)")
    destination: Optional[str] = Field(description="destination for the second place (ending location)")

prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert extraction algorithm. "
            "Only extract relevant information from the text which is origin and destination."
            "If you do not know the value of an attribute asked to extract, "
            "return null for the attribute's value."
            "return null if the origin or descrition of which is not provided",
        ),
        ("human", "{text}"),
    ]
)
structured_llm = llm.with_structured_output(schema=Person)

def process_general_chat(user_prompt: str):

    
    messages = [
        {
            "role": "system",
            "content": f"""You are a friendly conversational partner. Focus on natural dialogue and social interactions.

Key behaviors:
- Engage in casual conversation (how are you, what's new, etc.)
- Express empathy and interest in the user's responses
- Keep responses conversational and friendly
- Avoid providing encyclopedic knowledge or technical explanations
- Maintain a warm, personal tone
- your name is Alexa

Example exchanges:
User: "Hi, how are you?"
Assistant: "I'm doing great, thanks for asking! How has your day been?"

User: "I'm feeling tired today"
Assistant: "Oh, I'm sorry to hear that. Have you been getting enough rest lately?"
"""
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages
        )
        assistant_response = response.choices[0].message.content
    except groq.InternalServerError as e:
        print("Internal server error:", e)

    return assistant_response

@app.route('/chatbot', methods=['GET', 'POST'])
def index():
    token = session['token']
    print('current_token in chatbot is: ',token)
    if token is None:
        flash('You are not authorized to access this page.')
        return redirect(url_for('home'))

    if 'messages' not in app.config:
        app.config['messages'] = []

    if request.method == 'POST':
        question = request.form.get('question') or request.json.get('question')
        print("Question:", question)
        print('\n')   
        print("-"*50)              
        source = select_source(question)
        print(source)
        print('-'*50)
        source = source.strip()
        print(session.get('origin'))
        print(session.get('destination'))
        
        if source == 'general_question' or source == '"general_question"' or source == 'general questions' or source == '"general questions"' or source == 'general_greeting' or source == '"general greeting"' or source == 'general greeting' or source == '"general greeting"':
            print("General questions ..................")
            response = process_general_chat(question)
            print("Response:", response)
            app.config['messages'].append((question, response))
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'question': question, 'response': response})
            return render_template('index.html', messages=app.config.get('messages', []))

        elif source == 'not a general greeting' or source == '"not a general greeting"' or source == 'not_only_a_general_greeting' or source == '"not only a general greeting"':
            prompt = prompt_template.invoke({"text": question})
            response_data = structured_llm.invoke(prompt)
            origin = response_data.origin
            destination = response_data.destination
            
            session['origin'] = origin
            session['destination'] = destination
            
            print(f"Source: {origin}")
            print(f"Destination: {destination}")
            
            df = pd.read_csv('FFDataset2.csv', header=0)
            filtered_rows = df[(df['Origin Port Name'] == origin) & (df['Destination Port Name'] == destination)]
            print("Filtered rows:", filtered_rows)
            print("type of filtered_rows is: ",type(filtered_rows))

            # extracted_record = None
            if not filtered_rows.empty:
                stringified_data = filtered_rows.to_json(orient="records", lines=True)
                data_list = [json.loads(item) for item in stringified_data.split('\n') if item]
                full_data = []
                extracted_data = []
                for data in data_list:
                    extracted_record = {
                        "origin": data.get('Origin Port Name'),
                        "destination": data.get('Destination Port Name'),
                        "direction": data.get('Direction'),
                        "service_type": data.get('Service Type'),
                        "rate_type": data.get('Rate Type'),
                        "rate_value": data.get('Rate Value'),
                        "currency": data.get('Currency'),
                    }
                    extracted_data.append(extracted_record)
                    full_data.append(data)
                    session['full_data'] = full_data
                    print("Extracted record:", extracted_record)

                if extracted_record:
                    data_str = json.dumps(extracted_record, indent=2)
                    message = [
                        {"role": "system", "content": f"""You are an intelligent assistant. Here is some structured data:
                        Please process this data and provide a summary or respond to the following query:
                        1. Just summarize the origin, destination, direction, service type, rate type, rate value, and currency. Make it readable and just summarize the data; do not add any extra information."""},
                        {"role": "user", "content": data_str}
                    ]
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=message
                    )
                    response = response.choices[0].message.content
                    print('\n')
                    print("-----------------------------------------------------------------------------")
                    print('the response from the llm is : ')
                    print("Response:", response)
                    app.config['messages'].append((question, response))
                    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return jsonify({'question': question, 'response': response})
                    return render_template('index.html', messages=app.config.get('messages', []))
            else:
                response = '''We couldn't locate any matching data for this shipping query.'''
                # print("No matching rows found.")
                app.config['messages'].append((question, response))
                if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({'question': question, 'response': response})
                return render_template('index.html', messages=app.config.get('messages', []))

        elif source == 'print' or source == '"print"':
            print("Printing the data ..................")
            origin = session.get('origin')
            destination = session.get('destination')
            print(f"Retrieved from session - Origin: {origin}, Destination: {destination}")
            full_data = session.get('full_data')
            print("Full data:", full_data)
            print("type of full_data is: ",type(full_data))
            if origin is None or destination is None:
                response = '''The origin and destination details are required to generate the invoice.'''
                app.config['messages'].append((question, response))
                if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({'question': question, 'response': response})
                return render_template('index.html', messages=app.config.get('messages', []))
            else:
                try:
                    invoice_data = full_data[0] if full_data else {}
                    
                    print('*'*50)
                    print('invoice_data is : ')
                    print(invoice_data)
                    session['invoice_data'] = invoice_data
                    print('*'*50)
                    
                    invoice_response = requests.post(
                        url_for('invoice', _external=True),
                        json=invoice_data,
                        headers={'Content-Type': 'application/json'}
                    )
                    
                    if invoice_response.status_code == 200:
                        invoice_url = url_for('invoice')
                        response = (
                            f"Click this link to generate the invoice.\n\n"
                            f"You can view the invoice details here: <a href='{invoice_url}' target='_blank'>Invoice Details</a>\n\n"
                        )
                    else:
                        response = "Failed to retrieve the invoice details."
                except Exception as e:
                    response = f"An error occurred while fetching the invoice: {str(e)}"
                app.config['messages'].append((question, response))
                if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({'question': question, 'response': response})
                return render_template('index.html', messages=app.config.get('messages', []))
        if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'question': question, 'response': response})
    return render_template('index.html', messages=app.config.get('messages', []))

@app.route('/invoice', methods=['POST', 'GET'])
def invoice():
    if request.method == 'POST':
        print(' i am in the invoice post method')
        freight_data = request.get_json()
        print('Received JSON data in POST:')
        print(freight_data)
        session['freight_data'] = freight_data
        print('Stored in session:')
        print(session['freight_data'])
        if request.headers.get('Accept') == 'application/json':
            return jsonify(freight_data)
        return jsonify(freight_data)
    else:  
        print(' i am in the invoice get method')
        freight_data = session.get('invoice_data')
        print('Data retrieved from session in GET:')
        print(freight_data)
        if request.headers.get('Accept') == 'application/json':
            return jsonify(freight_data)
        return render_template('invoice.html', freightData=freight_data)



def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

@app.route('/scrape', methods=['POST'])
def scrape_website():
    driver = setup_driver()
    
    try:
        url = request.json.get('url', "https://www.jctrans.com/en/inquiry/freightinquiry?targetCountryId=94&targetCityId=1790&cargoType=Dangerous+Goods,Projects,General,Reefer+Container,Personal+Cargo,Special+Cargo,Others,eCommerce&transportType=LCL&lineId=20000000")
        
        driver.get(url)
        time.sleep(5)

        items = []
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "wrapper-content"))
            )
            
            item_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'wrapper-content')]//div[contains(@class, 'item')]")
            
            for item in item_elements:
                text = item.text.strip()
                class_name = item.get_attribute("class")
                if text:
                    items.append({
                        "text": text,
                        "class": class_name
                    })

        except TimeoutException:
            return jsonify({"error": "Timed out waiting for page content."}), 408
        except NoSuchElementException:
            return jsonify({"error": "Could not find the elements."}), 404

        return jsonify({"items": items})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(port=8006, debug=True)