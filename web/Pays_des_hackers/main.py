from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models.users import User
from models.roles import Role
from flask import send_from_directory

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

from flask import session

app = Flask(__name__)
app.secret_key = 'DFKJDfkjs3984dsfh932U@@dsfj!:dsfo988\-'

engine = create_engine('mysql://chall:dsfFKJDSkjdsf!83274fjdsh@localhost/challenge')
# Define the function to call the stored procedure
def persist_user(username, password, role):
    Session = sessionmaker(engine)
    with engine.connect() as conn:
        # Call the stored function using a SELECT statement
        result = conn.execute(
            text("""SELECT challenge.newuser(:username, :password, :role) AS result"""),
            {"username":username, "password":password, "role":role}
        )
        # Fetch the result
        row = result.fetchone()
        if row:
            conn.commit()
            return row
        else: 
            conn.rollback()
            return False

def get_user(username):
     Session = sessionmaker(engine)
     with engine.connect() as conn:
        # Call the stored function using a SELECT statement
        result = conn.execute(
            text("""SELECT username, password, name as role FROM users INNER JOIN roles ON users.role = roles.id WHERE users.username = :username;"""),
            {"username":username}
        )
        # Fetch the result
        row = result.fetchone()
        if row:
            return row
        else: 
            return False

roles = [role.value for role in Role]

def check_session():
    return session.get('login', False) == True 

@app.route('/')
def home():
    if (not check_session()):
        return redirect("/login", code=302)
    return render_template("index.html", role=session.get('role', 'unique'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login", code=302)

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        if (not ("username" in request.form 
                 and "password" in request.form)):
            flash('Paramètres manquants.', 'danger')
            return render_template('login.html'), 400

        username = request.form['username']
        password = request.form['password']

        row = get_user(username)
        if (row == False):  
            flash('Mauvais mot de passe ou Nom d\'utilisateur', 'danger')
            return render_template('login.html')
        
        row = row._tuple()
        # Access individual elements of the tuple
        if row[0] == username and row[1] == password:
            session['login'] = True
            session['username'] = row[0]
            session['role'] = row[2]
            flash('Login successful', 'success')
            return redirect(url_for('home'))
        else:   
            flash('Mauvais mot de passe ou Nom d\'utilisateur', 'danger')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    global users
    session.clear()
    if request.method == 'POST':
        if (not ("username" in request.form 
                 and "password" in request.form
                 and "role" in request.form)):
            flash('Paramètres manquants.', 'danger')
            return render_template('register.html'), 400
        
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        if (len(username) > 30) :
            flash('Le nom d\'utilisateur ne doit pas dépasser 30 caractères.', 'danger')
            return render_template('register.html'), 400
        if (len(password) > 100) : 
            flash('Le mot de passe ne doit pas dépasser 100 caractères.', 'danger')
            return render_template('register.html'), 400
        if (len(role) > 20) :
            flash('Le rôle ne doit pas dépasser 20 caractères.', 'danger')
            return render_template('register.html'), 400
        if (not role in roles) :
            flash('Erreur : Rôle inconnu.', 'danger')
            return render_template('register.html'), 400

        result = persist_user(username, password, role)._tuple()[0]
        print(result)
        if ('Erreur' in result):
            flash(result, 'danger')
            return render_template('register.html'), 400
        
        return redirect('/login', 302)

    return render_template('register.html')

@app.route('/me', methods=['GET'])
def me():
    if not "login" in session:
        return "Not logged in.", 400
    return jsonify({"username":session["username"], "role":session["role"]})

@app.route('/role', methods=['GET', 'POST'])
def role():
    if request.method == 'GET':
        return jsonify({"roles":["Administratorz_du_76", "Hunter", "Pentester", "Analyste SOC", "Mauvais Hacker..."]})
    if request.method == 'POST':
        if not request.is_json:
            return "Bad data format", 400
        data = request.json
        count = 0
        match data.get("posture"):
            case "attack":
                count += 5
            case "defense":
                count += 3
            case "victim":
                count += 1
                
        match data.get("master"):
            case "high":
                count += 5
            case "medium":
                count += 3
            case "low":
                count += 1

        match data.get("report"):
            case "advanced":
                count += 5
            case "learner":
                count += 3
            case "beginner":
                count += 1

        role = Role.BADHACKER
        if (count > 4) :
            role = Role.SOCANALYST
        if (count > 8) :
            role = Role.PENTESTER
        if (count > 12) : 
            role = Role.HUNTER

        return jsonify({'role':role})
    

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/assets/<path:path>')
def send_assets(path):
    return send_from_directory('assets', path)

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)

if __name__ == '__main__':
    app.run(debug=False)
