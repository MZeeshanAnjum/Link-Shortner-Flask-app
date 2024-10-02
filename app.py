from flask import Flask, render_template, request, jsonify, redirect, url_for, flash,session
import json
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = "djhd778qhsoq8qhd"


@app.route("/")
def index():
    codes = session.keys() if session else None
    return render_template("index.html",codes=codes)

@app.route("/clear_cache")
def clear_session():
    session.clear()  # Clear all session data
    flash("Session has been cleared!", "success")
    return redirect(url_for("index"))
@app.route("/clear_database")
def clear_data():
    os.remove("D:\Study\Flask\Link_Shortner\static\links.json")
    flash("Database has been cleared!", "success")
    return redirect(url_for("index"))
@app.route("/shortner", methods=['POST', "GET"])
def shortner():
    if request.method == 'POST':
        urls = {}
        if os.path.exists("D:\Study\Flask\Link_Shortner\static\links.json"):
            with open("D:\Study\Flask\Link_Shortner\static\links.json", "r") as f:
                urls = json.load(f)

        if request.form['action'] == 'url':
            if request.form['code'] in urls.keys():
                flash("Code Already Exists! Please choose another one ;)")
                return redirect(url_for("index"))
            code = request.form['code']
            urls[request.form['code']] = {'url': request.form['url']}
            # urls["status"]="success"
        if request.form['action'] == 'file':
            code = request.form['code_file']
            if request.form['code_file'] in urls.keys():
                flash("Code Already Exists! Please choose another one ;)")
                return redirect(url_for("index"))
            code = request.form['code_file']
            ff = request.files['file']
            full_name = request.form['code_file']+secure_filename(ff.filename)
            ff.save("D:/Study/Flask/Link_Shortner/static/user_files/"+full_name)
            urls[request.form['code_file']] = {'file': full_name}
        with open("D:\Study\Flask\Link_Shortner\static\links.json", "w") as f:
            json.dump(urls, f)
            session[code]=True
        # return jsonify(urls)
        # return render_template("shortner.html", code=code)
        flash('Your form has been successfully submitted!', 'success')
        return redirect(url_for("index")) 

    if request.method == 'GET':
        flash("You can't access this page")
        return redirect(url_for("index"))


@app.route("/<code>")
def handle_redirect(code):
    code = str(code)
    if os.path.exists("D:\Study\Flask\Link_Shortner\static\links.json"):
        with open("D:\Study\Flask\Link_Shortner\static\links.json", "r") as foile:
            shorts = json.load(foile)
            if code in shorts:
                if "url" in shorts[code]:
                    return redirect(shorts[code]["url"])
                elif "file" in shorts[code]:
                    return redirect(url_for("static", filename="user_files/"+shorts[code]["file"]))
            else:
                # If the code does not exist in the dictionary
                flash("Invalid code! Please check the link and try again.", "error")
                return redirect(url_for("index"))
    else:
        flash("No links file found.", "error")
        return redirect(url_for("index"))

@app.route("/api")
def session_api():
    with open("D:\Study\Flask\Link_Shortner\static\links.json", "r") as f:
        dick=json.load(f)
    return jsonify(dick)
if __name__ == '__main__':
    app.run(debug=True)
