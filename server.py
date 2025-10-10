from flask import Flask, render_template, request, session, redirect, jsonify
import requests

app = Flask(__name__)



app.secret_key = "mi-secret-key-cohort60"

# http://127.0.0.1:5001/about
@app.get("/about")
def about():
    return render_template("about.html")


@app.get("/contact")
def contact():
    name = "Big John" #can send data as a variable
    return render_template("contact.html", name=name)


@app.get("/")
@app.get("/home")
@app.get("/index")
def home():
  if 'user_id' in session:
    user_id = session['user_id']
    response = requests.get(f"http://localhost:5000/api/expenses?user_id={user_id}")
    expenses = response.json()

    return render_template('home.html', username=session['username'], expenses=expenses)
  else:
    return render_template('login.html')


# http://127.0.0.1:5000/login
@app.route("/login", methods=["GET", "POST"]) # Should be the exact same url as the backend code
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    response = requests.post("http://127.0.0.1:5000/api/login", json={
        "username": username,
        "password": password
    })

    if response.status_code == 200:  
        data = response.json()
        session["user_id"] = data["user_id"] # stored as cookie
        session["username"] = data["username"] # stored as cookie
        return redirect("home")
    else:
        return jsonify({"error": "Login failed"}), 401
    

@app.route('/logout')
def logout():
  session.clear() # Deletes the session
  return redirect('home')

if __name__ == "__main__":
    app.run(debug=True, port=5001)




