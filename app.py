from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def homepage():
    return render_template('base-template.html')


if __name__ == "__main__":
    app.run()
