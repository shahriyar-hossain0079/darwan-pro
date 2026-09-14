from flask import Flask, render_template_string, request, redirect, session
import json, os, random
app = Flask(__name__)
app.secret_key = "darwan-pro-final"
F = "students.json"
if not os.path.exists(F):
    open(F, "w").write("[]")

def load():
    try:
        return json.load(open(F))
    except:
        return []

def save(d):
    json.dump(d, open(F, "w"), indent=2)

HTML = """
<body style="background:#0f172a;color:white;font-family:sans-serif;padding:15px">
<h2>🔒 Darwan PRO</h2>
<div style="background:#1e293b;padding:15px;border-radius:15px">
<b>Teacher Class:</b> {{cls}}<br>
<form method=post action=/setcls style="margin-top:10px"><input name=c value="{{cls}}" style="width:100%;padding:10px"><button style="width:100%;padding:10px;margin-top:5px;background:#2563eb;color:white;border:none;border-radius:8px">Create Class With Gate</button></form>
<hr>
<b>Student Join</b><br>
<form method=post action=/join style="margin-top:10px"><input name=cn placeholder="Class Name" style="width:100%;padding:10px;margin:3px 0"><input name=n placeholder="Your Name" style="width:100%;padding:10px;margin:3px 0"><input name=i placeholder="ID Number" style="width:100%;padding:10px;margin:3px 0"><button style="width:100%;padding:10px;margin-top:5px;background:#16a34a;color:white;border:none;border-radius:8px">Join With ID</button></form>
<p style="color:#22c55e">{{msg}}</p>
</div>
<div style="border:2px solid #22c55e;padding:15px;border-radius:15px;margin-top:15px">
<h3>ID Generator - Meye Alada</h3>
<form method=post action=/gen><input name=name placeholder="Student Name" style="width:100%;padding:10px;margin:3px 0"><input name=roll placeholder="Roll" style="width:100%;padding:10px;margin:3px 0"><select name=g style="width:100%;padding:10px"><option>Female - Meye</option><option>Male - Chele</option></select><button style="width:100%;padding:10px;margin-top:5px;background:#16a34a;color:white;border:none">Generate ID</button></form>
<p style="color:yellow">New ID: {{gen}}</p>
{% for s in data %}<div style="background:#0f172a;padding:8px;margin:4px 0;border-radius:8px;font-size:13px">{{s.id}} | {{s.name}} | {{s.g}}</div>{% endfor %}
</div>
</body>
"""

@app.route("/")
def home():
    return render_template_string(HTML, cls=session.get("cls","Class-10 Girls"), msg=session.pop("msg",""), gen=session.pop("gen",""), data=load())

@app.route("/setcls", methods=["POST"])
def setcls():
    session["cls"] = request.form["c"]
    session["msg"] = "Class Created: " + request.form["c"]
    return redirect("/")

@app.route("/gen", methods=["POST"])
def gen():
    g = request.form["g"]
    nid = f"{'G' if 'Female' in g else 'B'}-{random.randint(1000,9999)}-{request.form['roll']}"
    d = load()
    d.append({"id": nid, "name": request.form["name"], "roll": request.form["roll"], "g": g})
    save(d)
    session["gen"] = nid
    return redirect("/")

@app.route("/join", methods=["POST"])
def join():
    sid = request.form["i"]
    d = load()
    ok = [x for x in d if x["id"] == sid]
    session["msg"] = f"Welcome {ok[0]['name']} Gate Opened!" if ok else "ID Not Found! Sir er theke ID nin"
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
