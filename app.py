from flask import Flask, request
from flask import Response
import json
import mysql.connector

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'

def get_db_connection():
    try:
        conn = mysql.connector.connect(user='root',password='test',host='127.0.0.1',database='search_db')
        return conn
    except Exception as e:
        print("ERROR:: Problem in getting connection {}".format(e))
        return None

def insert_or_update_search_qurey_rank(req_data):
    try:
        conn = get_db_connection()
        #query = 'INSERT INTO search_rank (userid, search_key, count) VALUES("{}", "{}", 1) \
        #        ON DUPLICATE KEY UPDATE count = count + 1'.format(req_data['user'], req_data['search_query'])
        query = "INSERT INTO search_rank(userid, search_key, count, record_id, record_rank) VALUES(%(userid)s, %(search_key)s, \
                %(count)s, %(record)s, %()S) ON DUPLICATE KEY UPDATE count = count + 1 , rank = rank + 1"
        values = {
                'userid':req_data['user'],
                'search_key':req_data['search_query'],
                'count':1,
                'record_id':req_data['record_id'],
                'record_rank':1
                }
        #cursor_obj = conn.cursor()
        cursor_obj = conn.cursor(buffered=True)
        result = cursor_obj.execute(query, values)
        conn.commit()
        cursor_obj.close()
        conn.close()
        return 'Success'
    except Exception as e:
        print("Error:: Problem in updating ranking table {}".format(e))
        return None

def get_search_records(request_data):
    try:
        import pdb;pdb.set_trace()
        query = "select * from students where (first_name like '%{}%' or last_name like '%{}%')".format(request_data['search_query'],\
                request_data['search_query'])
        conn = get_db_connection()
        cursor_obj = conn.cursor(buffered=True)
        cursor_obj.execute(query)
        result = cursor_obj.fetchall()
        #row_headers=[x[0] for x in cursor_obj.description]
        cursor_obj.close()
        conn.close()
        return result
    except Exception as e:
        print("ERROR::Problem in getting search records {}".format(e))
        return None

@app.route('/search_record', methods=['POST'])
def get_record_details(request_data):
    try:
        student_id = request_data["record_id"]
        search_key = request_data['serch_query']
        user_id = request_data['user']
        query = "select * from students where id={}".format(student_id) 
        conn = get_db_connection()
        cursor_obj = conn.cursor(buffered=True)
        cursor_obj.execute(query)
        student_details = cursor_obj.fetchall()

        rank_query = "update search_rank set student_id={}, record_rank=record_rank+1 where userid={} and"
    except Exception as e:
        print("ERROR:: Problem in getting record details {}".format(e))


@app.route('/search', methods=['POST', 'GET'])
def search():
    """
    This API returns a list of records matching the keyword
    """
    return 'test'
    msg = ''
    import pdb;pdb.set_trace()
    request_data = json.loads(request.data)
    #status = insert_or_update_search_qurey(request_data)

    search_records = get_search_records(request_data)
    if search_records:
        msg = json.dumps(search_records)
        #msg = 'Successfully updated/inserted search query'
    else:
        msg = 'Problem in updating the search rank table'
    resp = Response(msg, status=200, mimetype='application/json')
    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
