from flask import Flask, render_template, request
app = Flask(__name__,static_folder=r"C:\Users\santm\Documents\proj\mysic\remote\templates")


@app.route('/')
def index():
    return render_template('remote.html')

#app.run(debug=True)
