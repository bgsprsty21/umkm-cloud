from flask import Flask, render_template, request, redirect, url_for
from flask import request
from flask import request, session
from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2, os
import os


app = Flask(__name__)

app.secret_key = "umkm-kebumen-secret-123"

@app.route("/")
def home():
    if not session.get("admin"):
        return redirect(url_for("login"))

    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = conn.cursor()

    cur.execute("""
        SELECT nama_produk, harga, image_url, id
        FROM products
    """)
    products = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("index.html", products=products)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # LOGIN SEDERHANA (bisa dikembangkan ke DB nanti)
        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect(url_for("home"))
        else:
            return "Login gagal"

    return render_template("login.html")


@app.route("/simpan", methods=["POST"])
def simpan():
    nama = request.form["nama"]
    harga = request.form["harga"]
    image_url = request.form["image_url"]

    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO products (nama_produk, harga, image_url)
        VALUES (%s, %s, %s)
    """, (nama, harga, image_url))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("home"))

@app.route("/delete/<int:id>")
def delete(id):
    if not session.get("admin"):
        return redirect(url_for("login"))
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    return redirect(url_for("home"))


@app.route("/edit/<int:id>")
def edit(id):
    if not session.get("admin"):
        return redirect(url_for("login"))
    ...


@app.route("/tambah")
def tambah():
    if not session.get("admin"):
        return redirect(url_for("login"))
    return render_template("tambah.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
