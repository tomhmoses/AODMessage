from flask import Flask, render_template, request, redirect, url_for, Response
import pickle
import datetime

app = Flask(__name__)
app.config["DEBUG"] = True

files = {
    "message":"message.pickle",
    "history":"history.pickle",
    "visits":"visits.pickle"
}

@app.route("/alwaysonmessage")
def alwaysOnMessage():
    history = loadPickle(files["history"])
    messageData = history[len(history)-1]
    return render_template("always_on_message.html", messageData=messageData)

@app.route("/setmessage")
def setMessageForward():
    return redirect(url_for('setMessage'))

@app.route("/set")
def setForward():
    return redirect(url_for('setMessage'))

@app.route("/setMessage", methods=["GET", "POST"])
def setMessage():
    if request.method == "GET":
        try:
            message = loadPickle(files["message"])
        except:
            message = "could not load message"
        try:
            history = loadPickle(files["history"])
        except:
            print("couldnt get history")
            history = [{"name":"tom","message":"couldnt get history","datetime":"never..."}]
        try:
            visits = loadPickle(files["visits"])
            visits += 1
            savePickle(files["visits"],visits)
        except:
            visits = 100
        return render_template("set_message.html", message=message, history=history, visits=visits)
    message = request.form["message"]
    if len(message) > 500:
        message = message[:500]
    name = request.form["name"]
    if len(message.replace(" ","")) == 0 or len(name.replace(" ","")) == 0:
        return "too short"
    savePickle(files["message"], message)
    history = loadPickle(files["history"])
    history.append({"name":name,"message":message,"datetime":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
    savePickle(files["history"],history)
    visits = loadPickle(files["visits"])
    return render_template("set_message.html", message=message, done=True, history=history, visits=visits)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


#extra stuff


def savePickle(file_name, obj, protocol=pickle.DEFAULT_PROTOCOL):
    with open(file_name, 'wb') as fobj:
        pickle.dump(obj, fobj, protocol)

def loadPickle(file_name):
    with open(file_name, 'rb') as fobj:
        return pickle.load(fobj)
