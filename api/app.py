from flask import Flask, render_template

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/sandbox')
def sandbox():
    return render_template('sandbox.html')

@app.route('/current-members')
def current_members():
    return render_template('currentmem.html')

@app.route('/past-members')
def past_members():
    return render_template('pastmem.html')

if __name__ == '__main__':
    app.run(debug=True)
