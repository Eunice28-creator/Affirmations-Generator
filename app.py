from flask import Flask, render_template, request
import openai
import os
from twilio.rest import Client  # Added Twilio import

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "your-api-key-here"

def send_affirmation_sms(phone_number, affirmation):
    account_sid = "AC62f4bdf0da08c9c3788204ea945ed2d3"  # Replace with your Twilio Account SID
    auth_token = "dc1563f841a5e52e4806dfbe4111e5ef"  # Replace with your Twilio Auth Token
    twilio_number = "your_twilio_phone_number"  # Replace with your Twilio phone number

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=affirmation,
        from_=twilio_number,
        to=phone_number
    )

    return message.sid

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    name = request.form['name']
    mood = request.form['mood']
    focus = request.form['focus']
    illness = request.form['illness']
    tone = request.form['tone']
    identity = request.form['identity']
    phone_number = request.form.get('phone_number')  # Optional phone number field

    # Create prompt for GPT
    prompt = f"""
    Generate 5 affirmations for a person named {name}.
    Emotional state: {mood}.
    Life area of focus: {focus}.
    Tone: {tone}.
    Identity/self-description: {identity}.
    {name} {'has a chronic illness and often feels defeated.' if illness == 'yes' else ''}
    Keep the affirmations warm, tailored, and uplifting.
    """

    # Get response from OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in mental health and affirmation writing."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )

    affirmations = response['choices'][0]['message']['content'].strip()

    # Send affirmations via SMS if phone number is provided
    if phone_number:
        send_affirmation_sms(phone_number, affirmations)

    return render_template('result.html', affirmations=affirmations, name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)