from flask import Flask, render_template, request
import openai
import os

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = "your-api-key-here"

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

    return render_template('result.html', affirmations=affirmations, name=name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)