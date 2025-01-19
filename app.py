from flask import Flask
from routes import register_blueprints

app = Flask(__name__)
register_blueprints(app)

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