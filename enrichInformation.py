import json
from datetime import datetime
import requests
import sqlite3
from datetime import datetime

api_url_base = 'http://127.0.0.1:5000'
newHeaders = {'Content-type': 'application/json'}

DATABASE = 'dnstracker.db'
def create_connection(db_file=DATABASE):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)

    return conn

def updateQuery(query):
    json_data = json.dumps(query)
    response = requests.post(api_url_base+'/dns_query',
                             json_data, headers=newHeaders)

    print(response.status_code)
    if response.status_code != 201:
        print(json_data)
        print(response.text)


if __name__ == '__main__':
    conn = create_connection()
    cur = conn.cursor()
    query = cur.execute("select * from dns_query") # This line performs query and returns json result
    rows = query.fetchall()
    addressList = open("addresses.txt", "w")
    for row in rows:
        if row[5] != "None":
            addressList.write(str(row[5]+"\n"))
        if row[6] != "None":
            addressList.write(str(row[6]+"\n"))
            

