from flask import Flask, render_template, request
import re

app = Flask(__name__)

def calculate_strength(password):
    score = 0
    if len(password) >= 8:
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"[0-9]", password):
        score += 1
    if re.search(r"[!@#$%^&*()_+=\[\]{};':\\|,.<>/?`~\-]", password):
        score += 1
    if len(password) >= 12:
        score += 1
    return score

def is_blacklisted(password):
    try:
        with open("common_passwords.txt", "r") as f:
            common = f.read().splitlines()
            return password in common
    except:
        return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():
    password = request.form["password"]
    score = calculate_strength(password)
    blacklist_flag = is_blacklisted(password)

    if blacklist_flag:
        message = "This password is too common. Avoid using it."
    elif score < 2:
        message = "Weak password. Try adding symbols, numbers, and uppercase letters."
    elif score < 4:
        message = "Moderate password. Could be stronger."
    else:
        message = "Strong password!"

    return render_template("result.html", password=password, score=score, message=message, is_blacklisted=blacklist_flag)

if __name__ == "__main__":
    app.run(debug=True)