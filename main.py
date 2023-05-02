from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "many random bytes"


app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "adam"
app.config["MYSQL_PASSWORD"] = "user12345"
app.config["MYSQL_DB"] = "crud"

mysql = MySQL(app)


@app.route("/")
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM std")
    data = cur.fetchall()
    cur.close()
    return render_template("index.html", student=data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO std (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        mysql.connection.commit()
        return redirect(url_for('Index'))


@app.route("/delete/<string:id_data>", methods=["GET"])
def delete(id_data):
    flash("Data deleted successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM std WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for("Index"))


@app.route("/update", methods=["GET", "POST"])
def update():
    if request.method == "POST":
        id_data = request.form["id"]
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE std SET name=%s, email=%s, phone=%s
        WHERE id=%s
        """, (name, email, phone, id_data))
        flash("Data updated successfully")
        return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)
