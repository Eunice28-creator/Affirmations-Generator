from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_input = request.form['user_input']
    affirmation = f"Your affirmation is: {user_input}"  # Placeholder for actual affirmation generation logic
    return render_template('result.html', affirmation=affirmation)

if __name__ == '__main__':
    app.run(debug=True)