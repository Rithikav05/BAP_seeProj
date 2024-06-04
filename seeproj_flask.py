from flask import Flask, redirect, url_for, request,render_template
from seeproj_sqlite3 import *

app=Flask(__name__)

users={"test1":"pass1"}

@app.route("/")
def view_form():
        return render_template("loginpageun.html")

#@app.route('/login')
#def loginpage():
#    return render_template("loginpageun.html")

@app.route("/loggingin",methods=["POST"])
def handlelogin():

    if request.method=="GET":
        return (render_template("loginpageun.html"))

    elif request.method=="POST":
        uname=request.form["username"]
        pwd=request.form["password"]

        if uname in users and users[uname]==pwd:
            return(render_template("unoteshome.html"))

        else:
            return (render_template("loginpageun.html",a="Invalid Credentials"))

@app.route("/contact",methods=["GET","POST"])
def getcontactinfo():

    if request.method=="GET":
        return (render_template("unoteshome.html"))

    fname=request.form["fname"]
    lname=request.form["lname"]
    phoneno=request.form["phoneno"]
    emailid=request.form["emailid"]

    ctiobj=CIS()
    ctiobj.ConnectDB()
    ctiobj.CreateTableContact()

    if(request.form["action_button"]=="Submit"):
         ctiobj.AddInfo(fname,lname,phoneno,emailid)
         print("Yay")

    return(render_template("unoteshome.html",fn=fname,ln=lname,pn=phoneno,em=emailid))

@app.route("/browse")
def browse():
    return(render_template("searching.html"))

@app.route("/retcontact")
def recontact():
    return redirect(url_for('getcontactinfo'))

@app.route("/addn",methods=["GET","POST"])
def addn():

    if request.method=="GET":
        return (render_template("add_notes.html"))

    author=request.form["author"]
    #date=request.form["date"]
    subject=request.form["subject"]
    topic=request.form["topic"]
    content=request.form["body"]

    #print(author,date,subject,topic,content)
    #print(author,subject,topic,content)

    ntsobj=CIS()
    ntsobj.ConnectDB()
    ntsobj.CreateTableNotes()

    if(request.form["action_button"]=="Add"):
         msg=ntsobj.AddN(author,subject,topic,content)
         print("Yay,",msg)

    return(render_template("add_notes.html",athr=author,subj=subject,topc=topic,cont=content,addmsg=msg))

@app.route("/searchn",methods=["GET","POST"])
def searchn():

    if request.method=="GET":
        return (render_template("searching.html"))
    
    skword=request.form["search"]

    ntsobj=CIS()
    ntsobj.ConnectDB()
    #ntsobj.CreateTableNotes()

    if(request.form["action_button"]=="Search"):
         retval=ntsobj.SearchN(skword)
         #ctiobj.Search(search)
         print("Yay")

    return(render_template("searching.html",rtv=retval))

if __name__=="__main__":
    app.run(port=9000) 