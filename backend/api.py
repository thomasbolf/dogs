from flask import Flask, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

@app.route('/data')
def serve_csv():
    return send_file('animals.csv', mimetype='text/csv', as_attachment=True)

@app.route("/counties")
def serve_counties():
    return send_file('county_counts.csv', mimetype='text/csv', as_attachment=True)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)