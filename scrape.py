import csv
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from dotenv import load_dotenv
from os import getenv

from .utils import (
    extract_data,
    current_timestamp
)

load_dotenv()

app = Flask(__name__)
CORS(app)
CORS(app, origins=["*"])

# PostgreSQL connection
try:
    conn = psycopg2.connect(database=getenv("database"), user=getenv("user"), password=getenv("password"), host=getenv("host"), port=getenv("port"))
    cur = conn.cursor()
except Exception as e:
    print("DATABASE CONNECTION ERROR!")

#------------------------------------------------------APIS START--------------------------------------------------------#
@app.route('/parse_url', methods=['POST'])
def parse_url():
    url = request.json.get('url', '')
    if url:
        raw_data, error = extract_data(url)
        if error == "":
            # Store data in CSV file
            csv_filename = datetime.now().strftime("%d%m%Y") + "_verge.csv"
            with open(csv_filename, mode='a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(['', raw_data['link'], raw_data['title'], raw_data['author'], raw_data['pub_date']])

            # Store in PostgreSQL
            try:
                cur.execute("INSERT INTO articles (url, title, author, pub_date, timestamp) VALUES (%s, %s, %s, %s, %s) "
                            "ON CONFLICT (url) DO UPDATE SET title=EXCLUDED.title, author=EXCLUDED.author, pub_date=EXCLUDED.pub_date, timestamp=EXCLUDED.date",
                            (raw_data['link'], raw_data['title'], raw_data['author'], raw_data['pub_date'], current_timestamp()))
            except Exception as e:
                conn.rollback()
                error = "Database entry failure!"
            
            conn.commit()
            result = {
                "message": "Data parsed and stored successfully!",
                "error": error,
                "output": {
                    "title": raw_data["title"],
                    "url": raw_data["link"],
                    "author": raw_data["author"],
                    "published_date": raw_data["pub_date"],
                },
            }
            return jsonify(result), 200
        else:
            return jsonify({"success": False, "error": error}), 400
    else:
        return jsonify({"success": False, "error": "URL not provided"}), 400



@app.route('/get_data/<int:id>', methods=['GET'])
def get_data(id):
    cur.execute("SELECT * FROM articles WHERE id = %s", (id,))
    data = cur.fetchone()
    if data:
        result = {
            "id": data[0],
            "url": data[1],
            "title": data[2],
            "author": data[3],
            "published_date": data[4].strftime("%Y-%m-%d %H:%M:%S")  # format date as string
        }
        return jsonify(result), 200
    else:
        return jsonify({"success": False, "error": "Data not found"}), 404

#------------------------------------------------------APIS END--------------------------------------------------------#


if __name__ == '__main__':
    app.run(debug=True)
