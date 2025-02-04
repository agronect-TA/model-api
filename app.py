from flask import Flask
from routes.model_routes import predict_blueprint
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
app.register_blueprint(predict_blueprint)

@app.route('/db_test')
def db_test():
    from db import get_db_connection
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT NOW()')
        result = cursor.fetchone()
    connection.close()
    return f'Time from DB: {result[0]}'

if __name__ == '__main__':
    app.run(debug=True)
