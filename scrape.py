import csv
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from dotenv import load_dotenv
from os import getenv

from .utils import extract_data

load_dotenv()

app = Flask(__name__)
CORS(app)
CORS(app, origins=["*"])

# PostgreSQL connection
conn = psycopg2.connect(database=getenv("database"), user=getenv("user"), password=getenv("password"), host=getenv("host"), port=getenv("port"))
cur = conn.cursor()

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

            # # Store data in PostgreSQL
            cur.execute("INSERT INTO your_table_name (url, title, author, pub_date) VALUES (%s, %s, %s, %s)",
                        (raw_data['link'], raw_data['title'], raw_data['author'], raw_data['pub_date']))
            conn.commit()

            cur.execute("INSERT INTO articles (url, title, author, pub_date, date) VALUES (%s, %s, %s, %s, %s) "
                        "ON CONFLICT (url) DO UPDATE SET title=EXCLUDED.title, author=EXCLUDED.author, pub_date=EXCLUDED.pub_date, date=EXCLUDED.date",
                        (raw_data['link'], raw_data['title'], raw_data['author'], raw_data['pub_date'], today))
            conn.commit()
            result = {
                "message": "Data parsed and stored successfully!",
                "output": {
                    "title": raw_data["title"],
                    "url": raw_data["link"],
                    "author": raw_data["author"],
                    "published_date": raw_data["pub_date"]
                }
            }
            return jsonify(result), 200
        else:
            return jsonify({"success": False, "error": error}), 400
    else:
        return jsonify({"success": False, "error": "URL not provided"}), 400



@app.route('/get_data/<int:id>', methods=['GET'])
def get_data(id):
    cur.execute("SELECT * FROM your_table_name WHERE id = %s", (id,))
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
