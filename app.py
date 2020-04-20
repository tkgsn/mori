from flask import Flask, render_template

app = Flask(__name__)

@app.route("/home/takamo012345/mori/")
def bbs():
    message = "Hello"
    return render_template("index.html", message = message)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
