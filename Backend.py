import mysql.connector
import bcrypt
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'

# Database connection
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='company_dbms'
)
cursor = conn.cursor()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Token is missing"}), 403
        try:
            jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return jsonify({"error": "Invalid token"}), 403
        return f(*args, **kwargs)
    return decorated

# User authentication route
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    cursor.execute("SELECT id, password FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
        token = jwt.encode({'id': user[0], 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, 
                           app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    
    return jsonify({'error': 'Invalid credentials'}), 401

# CRUD for Employees
@app.route('/employees', methods=['GET'])
@token_required
def get_employees():
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    return jsonify(employees)

@app.route('/employees', methods=['POST'])
@token_required
def add_employee():
    data = request.json
    cursor.execute("INSERT INTO employees (name, position, salary) VALUES (%s, %s, %s)",
                   (data['name'], data['position'], data['salary']))
    conn.commit()
    return jsonify({"message": "Employee added successfully"})

@app.route('/employees/<int:id>', methods=['PUT'])
@token_required
def update_employee(id):
    data = request.json
    cursor.execute("UPDATE employees SET name=%s, position=%s, salary=%s WHERE id=%s",
                   (data['name'], data['position'], data['salary'], id))
    conn.commit()
    return jsonify({"message": "Employee updated successfully"})

@app.route('/employees/<int:id>', methods=['DELETE'])
@token_required
def delete_employee(id):
    cursor.execute("DELETE FROM employees WHERE id=%s", (id,))
    conn.commit()
    return jsonify({"message": "Employee deleted successfully"})

# CRUD for Machinery
@app.route('/machinery', methods=['GET'])
@token_required
def get_machinery():
    cursor.execute("SELECT * FROM machinery")
    machinery = cursor.fetchall()
    return jsonify(machinery)

@app.route('/machinery', methods=['POST'])
@token_required
def add_machinery():
    data = request.json
    cursor.execute("INSERT INTO machinery (name, type, status) VALUES (%s, %s, %s)",
                   (data['name'], data['type'], data['status']))
    conn.commit()
    return jsonify({"message": "Machinery added successfully"})

@app.route('/machinery/<int:id>', methods=['PUT'])
@token_required
def update_machinery(id):
    data = request.json
    cursor.execute("UPDATE machinery SET name=%s, type=%s, status=%s WHERE id=%s",
                   (data['name'], data['type'], data['status'], id))
    conn.commit()
    return jsonify({"message": "Machinery updated successfully"})

@app.route('/machinery/<int:id>', methods=['DELETE'])
@token_required
def delete_machinery(id):
    cursor.execute("DELETE FROM machinery WHERE id=%s", (id,))
    conn.commit()
    return jsonify({"message": "Machinery deleted successfully"})

# CRUD for Tenders
@app.route('/tenders', methods=['GET'])
@token_required
def get_tenders():
    cursor.execute("SELECT * FROM tenders")
    tenders = cursor.fetchall()
    return jsonify(tenders)

@app.route('/tenders', methods=['POST'])
@token_required
def add_tender():
    data = request.json
    cursor.execute("INSERT INTO tenders (title, client, amount) VALUES (%s, %s, %s)",
                   (data['title'], data['client'], data['amount']))
    conn.commit()
    return jsonify({"message": "Tender added successfully"})

@app.route('/tenders/<int:id>', methods=['PUT'])
@token_required
def update_tender(id):
    data = request.json
    cursor.execute("UPDATE tenders SET title=%s, client=%s, amount=%s WHERE id=%s",
                   (data['title'], data['client'], data['amount'], id))
    conn.commit()
    return jsonify({"message": "Tender updated successfully"})

@app.route('/tenders/<int:id>', methods=['DELETE'])
@token_required
def delete_tender(id):
    cursor.execute("DELETE FROM tenders WHERE id=%s", (id,))
    conn.commit()
    return jsonify({"message": "Tender deleted successfully"})

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
