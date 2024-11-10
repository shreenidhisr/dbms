from flask import Flask, render_template, request, redirect, url_for, session,flash
import pymysql
import regex
import sys
mydb = pymysql.connect(
    host="localhost",
    user="shreenidhi",
    password="Sd@something",
    database="pythonlogin",
)
cursor = mydb.cursor()

app = Flask(__name__)
app.secret_key = "your secret key"
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route("/login", methods=["GET", "POST"])
@app.route("/", methods=["GET", "POST"])
def farmer():
    # Output message if something goes wrong...
    msg = ""
    # Check if "username" and "password" POST requests exist (user submitted form)
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        # Create variables for easy access
        username = request.form["username"]
        password = request.form["password"]
        cursor.execute(
            "SELECT * FROM accounts WHERE username = %s AND password = %s",
            (
                username,
                password,
            ),
        )
        # Fetch one record and return result
        account = cursor.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            session["loggedin"] = True
            session["id"] = account[0]
            session["username"] = account[1]
            session["farmer"] = True
            # Redirect to home page
            return redirect(url_for("home"))
        else:
            msg = "incorrect username or password"
    return render_template("index.html", msg=msg)


@app.route("/Cheif", methods=["GET", "POST"])
def SocietyChief():
    msg = ""
    # Check if "username" and "password" POST requests exist (user submitted form)
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        # Create variables for easy access
        username = request.form["username"]
        password = request.form["password"]
        cursor.execute(
            "SELECT * FROM accounts_cheif WHERE username = %s AND password = %s",
            (
                username,
                password,
            ),
        )
        # Fetch one record and return result
        account = cursor.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            session["loggedin"] = True
            session["id"] = account[0]
            session["username"] = account[1]
            session["Society_cheif"] = True
            # Redirect to home page
            return redirect(url_for("home"))
        else:
            msg = "incorrect username or password"
    return render_template("societyChief.html",msg=msg)


@app.route("/govtAuth", methods=["GET", "POST"])
def govtAuth():
    msg = ""
    # Check if "username" and "password" POST requests exist (user submitted form)
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        # Create variables for easy access
        username = request.form["username"]
        password = request.form["password"]
        cursor.execute(
            "SELECT * FROM accounts_govt WHERE username = %s AND password = %s",
            (
                username,
                password,
            ),
        )
        # Fetch one record and return result
        account = cursor.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            session["loggedin"] = True
            session["id"] = account[0]
            session["username"] = account[1]
            session["govt_auth"] = True
            # Redirect to home page
            return redirect(url_for("home"))
        else:
            msg = "incorrect username or password"
    return render_template("GovtAuth.html", msg=msg)


# http://localhost:5000/python/logout - this will be the logout page
@app.route("/logout")
def logout():
    # Remove session data, this will log the user out
    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("username", None)
    if "govt_auth" in session:
        session.pop("govt_auth",None)
    if "Society_cheif" in session:
        session.pop("Society_cheif",None)
    if "farmer" in session:
        session.pop("farmer",None)
    # Redirect to login page
    return redirect(url_for("farmer"))


# http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route("/register", methods=["GET", "POST"])
def register():
    # Output message if something goes wrong...
    msg = ""
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
        and "email" in request.form
    ):
        # Create variables for easy access
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]

        # Check if account exists using MySQL

        cursor.execute("SELECT * FROM accounts WHERE username = %s", (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = "Account already exists!"
        elif not regex.match(r"[^@]+@[^@]+\.[^@]+", email):
            msg = "Invalid email address!"
        elif not regex.match(r"[A-Za-z0-9]+", username):
            msg = "Username must contain only characters and numbers!"
        elif not username or not password or not email:
            msg = "Please fill out the form!"
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute(
                "INSERT INTO accounts VALUES (NULL, %s, %s, %s)",
                (
                    username,
                    password,
                    email,
                ),
            )
            mydb.commit()
            msg = "You have successfully registered!"
    elif request.method == "POST":
        # Form is empty... (no POST data)
        msg = "Please fill out the form!"
    # Show registration form with message (if any)
    return render_template("register.html", msg=msg)


# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route("/home")
def home():
    # Check if user is loggedin
    if "loggedin" in session:
        # User is loggedin show them the home page
        if "govt_auth" in session:
            return render_template("g.html", username=session["username"])
        if "Society_cheif" in session:
            return render_template("c.html", username=session["username"])
        if "farmer" in session:
            
               
            return render_template("f.html", username=session["username"])
        #return render_template("home.html", username=session["username"])
    # User is not loggedin redirect to login page
    return redirect(url_for("farmer"))

@app.route("/cart")
def cart():
    return "this is ur cart"
# http://localhost:5000/pythinlogin/profile - this will be the profile page, only accessible for loggedin users
@app.route("/pythonlogin/profile")
def profile():
    # Check if user is loggedin
    if "loggedin" in session:
        if "farmer" in session:
            cursor.execute("SELECT * FROM accounts WHERE id = %s", (session["id"],))
            account = cursor.fetchone()
            # Show the profile page with account info
            return render_template("profile.html", account=account)
        # We need all the account info for the user so we can display it on the profile page
        if "govt_auth" in session:
            cursor.execute(
                "SELECT * FROM accounts_govt WHERE id = %s", (session["id"],)
            )
            account = cursor.fetchone()
            # Show the profile page with account info
            return render_template("profile.html", account=account)
        if "Society_cheif" in session:
            cursor.execute(
                "SELECT * FROM accounts_cheif WHERE id = %s", (session["id"],)
            )
            account = cursor.fetchone()
            # Show the profile page with account info
            return render_template("profile.html", account=account)

    # User is not loggedin redirect to login page
    return redirect(url_for("farmer"))

@app.route("/addproduct",methods=['GET','POST'])
def addproduct():
    #add product in database
    if request.method == 'POST':
        flash("product added successfully")
        return "added product"
    return render_template("addproduct.html")
    
@app.route("/getfarmerdetails",methods=['GET','POST'])
def getfarmerdetails():
    if request.method == 'POST':
        #add here searching logic afterwards
        flash("ok ")
        return "farmer1"
    return render_template("getfarmer.html")



if __name__ == "__main__":
    app.run(debug=True)
