from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/selection')
def selection():
    return render_template('selection.html')

@app.route('/matches')
def matches():
    return render_template('matches.html')

@app.route('/contact')
def contact():
    return render_template('contact.html') 

@app.route('/signin')
def signin():
    return render_template('Signin.html')         


if __name__ == '__main__':
    app.run(debug=True)