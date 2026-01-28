from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret")

# ======================
# DATABASE CONNECTION
# ======================
def get_conn():
    return psycopg2.connect(os.environ["DATABASE_URL"])


# ======================
# HOME (PROTECTED)
# ======================
@app.route("/")
def home():
    if not session.get("admin"):
        return redirect(url_for("login"))

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, nama_produk, harga, image_url
        FROM products
        ORDER BY id
    """)
    products = cur.fetchall()

    cur.close()
    conn.close()

    return render_template("index.html", products=products)


# ======================
# LOGIN
# ======================
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["admin"] = True
            return redirect(url_for("home"))
        else:
            return render_template("login.html", error="Login gagal")

    return render_template("login.html")


# ======================
# LOGOUT
# ======================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ======================
# TAMBAH PRODUK
# ======================
@app.route("/tambah")
def tambah():
    if not session.get("admin"):
        return redirect(url_for("login"))
    return render_template("tambah.html")


@app.route("/simpan", methods=["POST"])
def simpan():
    if not session.get("admin"):
        return redirect(url_for("login"))

    nama = request.form["nama"]
    harga = request.form["harga"]
    image_url = request.form["image_url"]

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO products (nama_produk, harga, image_url)
        VALUES (%s, %s, %s)
    """, (nama, harga, image_url))

    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("home"))


# ======================
# DELETE PRODUK
# ======================
@app.route("/delete/<int:id>")
def delete(id):
    if not session.get("admin"):
        return redirect(url_for("login"))

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=%s", (id,))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for("home"))
