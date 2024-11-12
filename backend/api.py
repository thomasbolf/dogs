from flask import Flask, send_file
from flask_cors import CORS
import pandas as pd
app = Flask(__name__)
CORS(app)  

@app.route('/data')
def serve_csv():
    return send_file('animals.csv', mimetype='text/csv', as_attachment=True)

@app.route("/counties")
def serve_counties():
    return send_file('county_counts.csv', mimetype='text/csv', as_attachment=True)

@app.route("/number_of_dogs")
def serve_num():
    #count number of dogs in animals.csv and return it
    df = pd.read_csv('animals.csv')
    num_dogs = df[df['type'] == 'Dog'].shape[0]
    return str(num_dogs)
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)