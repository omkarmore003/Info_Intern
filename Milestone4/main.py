from flask import Flask, render_template, request
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Flask app
app = Flask(__name__)

# Database connection
def connect_to_db():
    return mysql.connector.connect(
        host="127.0.0.1", 
        user="root",
        password="Omkar@003", 
        database="inventory_management"
    )

# Email configuration
SMTP_SERVER = "smtp.gmail.com"  # Gmail SMTP server
SMTP_PORT = 587
SENDER_EMAIL = "003omkarmore@gmail.com"
SENDER_PASSWORD = "wuna hwyv tvwa rlja"  # Use an app-specific password if needed
RECIPIENT_EMAIL = "33omkarmore@gmail.com"  # Update to the desired recipient email

# Function to send email notifications
def send_email(subject, body):
    try:
        # Create email message
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECIPIENT_EMAIL
        msg["Subject"] = subject

        # Add email body
        msg.attach(MIMEText(body, "plain"))

        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        print(f"Email sent: {subject}")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Route: Dashboard
@app.route("/dashboard")
def dashboard():
    conn = connect_to_db()
    cursor = conn.cursor()

    try:
        # Fetch adjusted inventory data
        cursor.execute("SELECT * FROM adjusted_inventory")
        adjusted_inventory = pd.DataFrame(cursor.fetchall(), columns=["Country", "Stock Level", "Stock Adjusted", "Adjustment", "Published At"])

        # Fetch risk data
        cursor.execute("SELECT * FROM risk_data")
        risk_data = pd.DataFrame(cursor.fetchall(), columns=["ID", "Title", "Risk Level", "Stock Adjustment", "Published At"])

        # Create visualizations
        # 1. Risk Levels Distribution
        risk_level_counts = risk_data["Risk Level"].value_counts()
        plt.figure(figsize=(8, 6))
        risk_level_counts.plot(kind="bar", color=["red", "orange", "green"])
        plt.title("Risk Levels Distribution")
        plt.xlabel("Risk Level")
        plt.ylabel("Count")
        plt.savefig("static/risk_levels.png")
        plt.close()

        # 2. Inventory Adjustments
        plt.figure(figsize=(10, 6))
        adjusted_inventory.set_index("Country")["Adjustment"].plot(kind="bar", color="blue")
        plt.title("Inventory Adjustments by Country")
        plt.xlabel("Country")
        plt.ylabel("Adjustment")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig("static/inventory_adjustments.png")
        plt.close()

        # Trigger email notifications for critical conditions
        # High-risk and Low-risk levels
        critical_risks = risk_data[risk_data["Risk Level"].isin(["High", "Low"])]
        for _, row in critical_risks.iterrows():
            subject = f"Risk Alert: {row['Title']}"
            body = f"Risk Level: {row['Risk Level']}\nTitle: {row['Title']}\nStock Adjustment: {row['Stock Adjustment']}\nPublished At: {row['Published At']}"
            send_email(subject, body)

        # All stock adjustments
        for _, row in adjusted_inventory.iterrows():
            subject = f"Stock Adjustment Alert: {row['Country']}"
            body = f"Country: {row['Country']}\nStock Level: {row['Stock Level']}\nStock Adjusted: {row['Stock Adjusted']}\nAdjustment: {row['Adjustment']}\nPublished At: {row['Published At']}"
            send_email(subject, body)

        return render_template("dashboard.html", risk_image="risk_levels.png", inventory_image="inventory_adjustments.png")

    except Exception as e:
        return f"Error: {e}"

    finally:
        cursor.close()
        conn.close()

# Run the Flask app
if __name__ == "__main__":
    if not os.path.exists("static"):
        os.mkdir("static")  # Create a static directory if it doesn't exist
    app.run(debug=True)
