from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import base64

con = sqlite3.connect("data.db")
cur = con.cursor()

con.execute("CREATE TABLE IF NOT EXISTS brand_details(image BLOB,id INTEGER PRIMARY KEY, bike_name VARCHAR(50), kms_driven INTEGER, owners_details VARCHAR(100),register_details VARCHAR(100), emi_details VARCHAR(100), price REAL, location_details VARCHAR(100))")

app = Flask(__name__)

def get_db_connection():
    return sqlite3.connect("data.db")

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/register-bike", methods=["POST", "GET"])
def register_bike():
        
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    if request.method == "POST":
        id = request.form["id"]
        image = request.files["image"].read()
        bike_name = request.form["bike_name"]
        kms_driven = request.form["kms_driven"]
        owner_details = request.form["owner_details"]
        register_details = request.form["register_details"]
        emi_details = request.form["emi_details"]
        price = request.form["price"]
        location_details = request.form["location_details"]
        cur.execute("INSERT INTO brand_details(id,image, bike_name, kms_driven, owners_details,register_details, emi_details, price, location_details) VALUES (?, ?, ?, ?, ?, ?,?, ?, ?)",
                    (id,image, bike_name, kms_driven, owner_details,register_details, emi_details, price, location_details))
        con.commit()
        return render_template("register_success.html")
    
    if request.method == "GET":
        return render_template("register_bike.html")

@app.route("/update-bike/<int:id>", methods=["POST", "GET"])
def update_bike(id):
    if request.method == "POST":
        con = get_db_connection()
        cur = con.cursor()
        image = request.files["image"].read()
        bike_name = request.form["bike_name"]
        kms_driven = request.form["kms_driven"]
        owner_details = request.form["owner_details"]
        register_details = request.form["register_details"]
        emi_details = request.form["emi_details"]
        price = request.form["price"]
        location_details = request.form["location_details"]
        cur.execute("UPDATE brand_details SET image=?, bike_name=?, kms_driven=?, owners_details=?,register_details=?, emi_details=?, price=?, location_details=? WHERE id=?",
                    (image,bike_name, kms_driven, owner_details,register_details, emi_details, price, location_details, id))
        con.commit()
        con.close()
        return redirect(url_for("register_success"))
    elif request.method == "GET":
        con = get_db_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM brand_details WHERE id=?", (id,))
        bike = cur.fetchone()
        con.close()
        return render_template("update_bike.html", bike=bike)

@app.route("/delete-bike/<int:id>", methods=["POST","GET"])
def delete_bike(id):
    con = get_db_connection()
    cur = con.cursor()
    cur.execute("DELETE FROM brand_details WHERE id=?", (id,))
    con.commit()
    con.close()
    return redirect(url_for("register_success"))

@app.route("/register-success")
def register_success():
    return render_template("register_success.html")



@app.route("/view-bikes")
def viewbikes():
    con = sqlite3.connect("data.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM brand_details")
    data = cur.fetchall()
    return render_template("view-bikes.html", data=data)





if __name__ == "__main__":
    app.run(debug=True)
