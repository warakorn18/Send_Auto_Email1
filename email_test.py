from flask import Flask
from flask import render_template # to render our html page
from flask import request # to get user input from form
import hashlib # included in Python library, no need to install
import psycopg2 # for database connection
# NEW for this part 4 of our series on adding user registration to an application:
from flask_mail import Mail
from flask_mail import Message

app = Flask(__name__)

# New for this part 4:
def smtp_config(config_name, smtp=1):
    with open(config_name) as f:
            config_data = json.load(f)
    if smtp not in {1,2}:
        raise ValueError("smtp can only be 1 or 2")
    if smtp==2:
        MAIL_USERNAME = config_data['MAIL_USERNAME'][1]
        MAIL_PASSWORD = config_data['MAIL_PASSWORD'][1]
    else:
        MAIL_USERNAME = config_data['MAIL_USERNAME'][0]
        MAIL_PASSWORD = config_data['MAIL_PASSWORD'][0]
    MAIL_SERVER = config_data['MAIL_SERVER']
    MAIL_PORT = config_data['MAIL_PORT']
    MAIL_USE_TLS = bool(config_data['MAIL_USE_TLS'])
    return [MAIL_USERNAME, MAIL_PASSWORD, MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS]
# Set up the mail object we will use later.
mail = Mail()

@app.route("/")

def showForm():
    # Show our html form to the user.
    t_message = "Python and Postgres Registration Application"
    return render_template("register.html", message = t_message)

@app.route("/register", methods=["POST","GET"])
def register():
    # Get user input from the html form.
    t_email = request.form.get("t_email", "")
    t_password = request.form.get("t_password", "")

    # Check for blanks
    if t_email == "":
        t_message = "Please fill in your email address"
        return render_template("register.html", message = t_message)

    if t_password == "":
        t_message = "Please fill in your password"
        return render_template("register.html", message = t_message)

    # Hash the password they entered
    t_hashed = hashlib.sha256(t_password.encode())
    t_password = t_hashed.hexdigest()

    # Database insert
    t_host = "191.191.2.179"
    t_port = "5432"
    t_dbname = "Totle-2nd-Mask"
    t_user = "admin"
    t_pw = "Ab123456"
    db_conn = psycopg2.connect(host=t_host, port=t_port, dbname=t_dbname, user=t_user, password=t_pw)
    db_cursor = db_conn.cursor()

    # We take the time to build our SQL query string so that
    #   (a) we can easily and quickly read it; and
    #   (b) we can easily and quickly edit or add/remote lines.
    #   The more complex the query, the greater the benefits of this approach.
    s = ""
    s += "INSERT INTO users "
    s += "("
    s += " t_email"
    s += ",t_password"
    s += ",b_enabled"
    s += ") VALUES ("
    s += " '" + t_email + "'"
    s += ",'" + t_password + "'"
    s += ", false"
    s += ")"
    # IMPORTANT WARNING: this format allows for a user to try to insert
    #   potentially damaging code, commonly known as "SQL injection".
    #   In a later article we will show some methods for
    #   preventing this.

    # Here we are catching and displaying any errors that occur
    #   while TRYing to commit the execute our SQL script.
    db_cursor.execute(s)
    try:
        db_conn.commit()
    except psycopg2.Error as e:
        t_message = "Database error: " + e + "/n SQL: " + s
        return render_template("register.html", message = t_message)

    db_cursor.close()

    # NOTE WE CHANGED THIS AND MOVED IT TO THE BOTTOM
    # t_message = "Your user account has been added."

    # ------------------------------------#
    # NEW for this part 4 of our series on adding user registration to an application:
    # ------------------------------------#

    # Get user ID from PostgreSQL users table
    s = ""
    s += "SELECT ID FROM users"
    s += "WHERE"
    s += "("
    s += " t_email ='" + t_email + "'"
    s += " AND"
    s += " b_enabled = false"
    s += ")"
    # Warning: this format allows for a user to try to insert
    #   potentially damaging code, commonly known as "SQL injection".
    #   In a later article we will show some methods for
    #   preventing this.
    # Another item we'll save for another article:
    #   using another field, along with t_email and b_enabled,
    #   to be sure to get the new user ID

    db_cursor.execute(s)

    # Here we are catching and displaying any errors that occur
    #   while TRYing to commit the execute our SQL script.
    try:
        array_row = cur.fetchone()
    except psycopg2.Error as e:
        t_message = "Database error: " + e + "/n SQL: " + s
        return render_template("register.html", message = t_message)

    ID_user = array_row(0)

    # Cleanup our database connections
    db_cursor.close()
    db_conn.close()

    # Send confirmation email to the user
    smtp_data = smtp_config('config.json', smtp=1)
    app.config.update(dict(
    MAIL_SERVER = smtp_data[2],
    MAIL_PORT = smtp_data[3],
    MAIL_USE_TLS = smtp_data[4],
    MAIL_USERNAME = smtp_data[0],
    MAIL_PASSWORD = smtp_data[1],
    ))
    mail.init_app(app)
    # Set up smtp (send mail) configuration
    t_subject = "IMPORTANT: Confirmation link"
    t_recipients = t_email
    t_sender = "server@ourapplication.com"

    # Build message body here
    s = ""
    s += "Dear " + s_email + "<br>"
    s += "<br>"
    s += "Thank you for beginning the registration process." + "<br>"
    s += "<br>"
    s += "STEP ONE - To COMPLETE the process,  you MUST please click on the following link:" + "<br>"
    s += "<br>"
    s += "<a href='https://YOUR APP DOMAIN NAME HERE/register.py?confirm=" + ID_user
    s += "'>https://YOUR APP DOMAIN NAME HERE/register.py?confirm=" + ID_user
    s += "</a>" + "<br>"
    s += "<br>"
    s += "This action will COMPLETE the process and verify your email address and password." + "<br>"
    s += "<b>IMPORTANT: YOUR USERNAME IS YOUR EMAIL ADDRESS.</b><br>"
    s += "<br>"
    s += "NOTE: If you clicked on the link above and for some reason it did not take you to a web page "
    s += "confirming your account has been enabled, please use your mouse to highlight the link "
    s += "above and copy the link and then paste it into the address bar of your web browser and "
    s += "press the ENTER key to be taken to the page on our site that will enable your account."
    s += "<br>"
    s += "STEP TWO - Please save the user name (email address) you see below." + "<br>"
    s += "<br>"
    s += "User Name: " + t_email + "<br>"
    s += "<br>"
    s += "If you have any questions, feel free to reply to this message." + "<br>"
    s += "<br>"
    # Set up our mail message
    msg = Message(
        body = s,
        subject = t_subject,
        recipients = [t_recipients],
        sender = t_sender,
        reply_to = t_sender
        )

    # Send the email
    mail.send(msg)

    # Show user they are done and remind them to check their email.
    t_message = "Your user account has been added. Check your email for confirmation link."
    return render_template("register.html", message = t_message)

# This is for command line testing
if __name__ == "__main__":
    app.run(debug=True)