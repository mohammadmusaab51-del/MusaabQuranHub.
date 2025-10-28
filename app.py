from flask import Flask, render_template, request, flash, redirect
import sqlite3
import yagmail

# ------------------ Configuration ------------------ #
app = Flask(__name__)
app.secret_key = "97b834d7823974e2e7913928ba537ada7bf954f803927dc06b6cadeda1d7feae"

DB_NAME = "bookings.db"
SENDER_EMAIL = "moahmmadmusaab51@gmail.com"
SENDER_APP_PASSWORD = "pfkxdbxlpdbqqapf"  # <-- your new App Password
RECEIVER_EMAIL = "moahmmadmusaab51@gmail.com"

# ------------------ Initialize Database ------------------ #
def init_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            course TEXT NOT NULL,
            message TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.close()
    print("Database initialized.")

init_db()

# ------------------ Routes ------------------ #
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        course = request.form.get("course")
        message = request.form.get("message")

        if not all([name, email, phone, course]):
            flash("Please fill in all required fields!")
            return redirect("/")

        # Save to SQLite
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO bookings (name,email,phone,course,message) VALUES (?,?,?,?,?)',
                (name,email,phone,course,message)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            flash(f"Database error: {e}")
            return redirect("/")

        # Send email
        try:
            yag = yagmail.SMTP(SENDER_EMAIL, SENDER_APP_PASSWORD)
            contents = [
                f"Name: {name}",
                f"Email: {email}",
                f"WhatsApp: {phone}",
                f"Course: {course}",
                f"Message: {message}"
            ]
            yag.send(RECEIVER_EMAIL, f"New Booking from {name}", contents)
            print("Email sent successfully!")
            flash("Booking submitted successfully! Check your Gmail.")
        except Exception as e:
            print("Email could not be sent:", e)
            flash(f"Could not send email. Check console. {e}")

        return redirect("/")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
