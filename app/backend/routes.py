from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('../frontend/home/pages/index.html')

@app.route('/films')
def about():
    return render_template('../frontend/home/pages/films.html')

@app.route('/series')
def services():
    return render_template('../frontend/home/pages/series.html')

@app.route('/recomendations')
def contact():
    return render_template('../frontend/home/pages/recomendations.html')

if __name__ == '__main__':
    app.run(debug=True)