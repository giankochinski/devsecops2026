from flask import Flask, request, render_template, session, url_for, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = b'1234'

# Simulação de um banco de dados inseguro
def get_db_connection():
    conn = sqlite3.connect('database.db')
    return conn

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/welcome", methods=['GET'])
def welcome():

    if 'username' in session:
        username = session.pop('username')
        return render_template('welcome.html', username=username)

    return render_template('error.html')
    

@app.route("/login", methods=['GET'])
def login_page():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('passwd') 
    
    conn = get_db_connection()
    query = f"SELECT * FROM users WHERE username = '{username}' AND passwd = '{password}'"
    user = conn.execute(query).fetchone()
    
    if user:
        session['username'] = username
        return redirect(url_for('welcome'))
    return "Usuário ou senha incorretos", 401

if __name__ == '__main__':
    app.run(debug=True)