from flask import Flask,render_template,request,url_for
from datetime import datetime as date
import datetime
from joblib import load
import re
import nltk
from nltk.corpus import stopwords
#nltk.download('stopwords')
from nltk.stem.porter import PorterStemmer
import sqlite3
app = Flask(__name__)
app.secret_key="__privatekey__"
app = Flask(__name__)
model = load('static/nlp_gnb_pcl_model.joblib')
cv = load('static/cv.joblib')
print("model loaded successfully")


import string

#establishing connection with mongodb cloud for uploading the data into the cloud
from pymongo import MongoClient
client = MongoClient('mongodb+srv://subhi:subhi123@cluster0.wbhszdj.mongodb.net/?retryWrites=true&w=majority')

db = client.get_database('student')
print("connected with mongodb cloud")
records = db.register
date_element = datetime.date.today()
print(date_element)





@app.route('/hello')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/add/')
def add():  # put application's code here
    return render_template('student_add.html')




@app.route('/register',methods =["GET", "POST"])
def register_m():# put application's code here
    if request.method == "POST":
        name = request.form.get("name")
        branch = request.form.get('branch')
        usn = request.form.get('usn')
        email = request.form.get('email')
        password = request.form.get('password')
        dob = request.form.get('dob')
        adar = request.form.get('adar')
        father = request.form.get('father')
        sem = request.form.get('sem')

        new_student = {
            "name": name,
            "branch": branch,
            "usn": usn,
            "email": email,
            "password": password,
            "dob": dob,
            "adar": adar,
            "father": father,
            "sem": sem
        }
        records.insert_one(new_student)
        print("record inserted")
        msg = "We have added the student to the list"
        return render_template("admin.html", msg=msg)







@app.route('/')
def login():  # put application's code here
    return render_template('login.html')

def check(usn,password):
    Usn = usn
    print(Usn)
    Password = password
    print(Password)
    #query = {"usn": Usn,"password":Password}
    db.register.find({"usn":Usn,"password":Password})
    resu = records.find({"usn": Usn,"password":Password})
    print(resu)
    #for i in records.find(query,{"name":1,"usn":1,"password":1}):
     #   print(i)

    if Usn==Usn and Password==Password:
        msg="true"
        return msg
    else:
        msg = "false"
        return msg


@app.route('/loginact',methods =["GET", "POST"])
def login_act(): # put application's code here
    if request.method == "POST":
        usn = request.form.get('name')
        password = request.form.get('pass')

        if usn=="admin" and password=="admin123":
            return render_template("admin.html")

        else:

            query = {"usn":usn}
            print("printing the values for query")
            li = []
            for x in records.find(query):
                print(x)
                li.append(x['usn'])#0
                li.append(x['password'])#1
                li.append(x['name'])#2
                li.append(x['branch'])#3
                li.append(x['email'])#4
                li.append(x['dob'])#5
                li.append(x['adar'])#6
                li.append(x['father'])#7
                li.append(x['sem'])#8

                #li.append(x['name'])
            print(li)

            #
            Usn = str(li[0])
            Password = str(li[1])
            name = str(li[2])
            branch = str(li[3])
            email = str(li[4])
            dob = str(li[5])
            adar = str(li[6])
            father = str(li[7])
            sem = str(li[8])

            print("printing both usn and password")
            print(usn)
            print(password)
            print(Usn)
            print(Password)
            data = {
                "usn":Usn,
                "password":Password,
                "name":name,
                "branch":branch,
                "email":email,
                "dob":dob,
                "adar":adar,
                "father":father,
                "sem":sem
            }

            #-------------------------------
            #for retrieveing data for results
    #----------------------------------------------------------------
            results = db.results
            query = {"usn":usn}
            print("printing the values for results query")
            li1 = []
            for x in results.find(query):
                print(x)
                li1.append(x['usn'])#0
                li1.append(x['name'])#1
                li1.append(x['sem'])#2
                li1.append(x['ann'])#3
                li1.append(x['nosql'])#4
                li1.append(x['ai_platforms'])#5
                li1.append(x['oe_1'])#6
                li1.append(x['total'])#7
                li1.append(x['sgpa'])#8
                li1.append(x['satus'])#9


                #li.append(x['name'])
            print(li1)

            #
            uSn = str(li1[0])
            name = str(li1[1])
            sem = str(li1[2])
            ann = str(li1[3])
            nosql = str(li1[4])
            ai_platforms = str(li1[5])
            oe_1 = str(li1[6])
            total = str(li1[7])
            sgpa = str(li1[8])
            status = str(li1[9])

            result_data = {
                "usn":uSn,
                "name":name,
                "sem":sem,
                "ann":ann,
                "nosql":nosql,
                "ai_platforms":ai_platforms,
                "oe_1":oe_1,
                "total":total,
                "sgpa":sgpa,
                "status":status
            }
            #--------------------
            timetable = db.timetable
            day = date.today().strftime("%A")
            print(day)
            day = day.lower()
            print(day)

            q = {"course":branch,"sem":sem,"day":day}
            y = timetable.find(q)
            print(y)

            #------------------------------------------------------------
            #for retriving the data for attendance

            da = datetime.datetime.now()
            print(da)
            d = da.strftime('%m%d%Y')
            q = {
                "usn":usn,
                "date":d
            }
            attend = db.attendance
            x = attend.find(q)





            #for y in timetable.find(q):
             #   print(y)



            if usn == Usn and password == Password:
                msg="true"
                return render_template('dashboard.html',dat=data,res =result_data,y=y,attend=x)
            else:
                msg="false"
                return render_template('login.html')

            print(msg)
            return "logged in"

@app.route('/add_result_page')
def add_result_page():
    return render_template("result_add.html")

@app.route('/add_result',methods =["GET", "POST"])
def add_result():  # put application's code here
    if request.method == "POST":
        usn = request.form.get('usn')
        name= request.form.get('name')
        sem = request.form.get('sem')
        ann = request.form.get('ann')
        nosql = request.form.get('nosql')
        ai_platforms = request.form.get('ai_platforms')
        oe_1 = request.form.get('oe_1')
        total = request.form.get('total')
        sgpa = request.form.get('sgpa')
        status = request.form.get('status')

        data = {
            "usn":usn,
            "name":name,
            "sem":sem,
            "ann":ann,
            "nosql":nosql,
            "ai_platforms":ai_platforms,
            "oe_1":oe_1,
            "total":total,
            "sgpa":sgpa,
            "satus":status
        }

        results = db.results
        results.insert_one(data)
        print("result inserted")
        msg = "We have added the student result to the database"
        return render_template("admin.html", msg=msg)


#adding admin dashboard
@app.route('/admin')
def admin():
    return render_template("admin.html")

@app.route('/search_page')
def search_page():
    return render_template("student_search.html")


@app.route('/search',methods =["GET", "POST"])
def search():
    if request.method == "POST":
        usn = request.form.get('usn')
        query = {"usn": usn}
        print("printing the values for query")
        li = []
        for x in records.find(query):
            print(x)
            li.append(x['usn'])  # 0
            li.append(x['password'])  # 1
            li.append(x['name'])  # 2
            li.append(x['branch'])  # 3
            li.append(x['email'])  # 4
            li.append(x['dob'])  # 5
            li.append(x['adar'])  # 6
            li.append(x['father'])  # 7
            li.append(x['sem'])  # 8

            # li.append(x['name'])
        print(li)

        #
        Usn = str(li[0])
        Password = str(li[1])
        name = str(li[2])
        branch = str(li[3])
        email = str(li[4])
        dob = str(li[5])
        adar = str(li[6])
        father = str(li[7])
        sem = str(li[8])

        print("printing both usn and password")
        print(usn)

        print(Usn)

        data = {
            "usn": Usn,
            "password": Password,
            "name": name,
            "branch": branch,
            "email": email,
            "dob": dob,
            "adar": adar,
            "father": father,
            "sem": sem
        }

    return render_template("search_result.html",dat=data)

@app.route('/add_timetable_page')
def add_timetable_page():  # put application's code here
    return render_template('add_timetable_page.html')

@app.route('/add_timetable',methods =["GET", "POST"])
def add_timetable():
    if request.method == "POST":
        course = request.form.get('course')
        sem = request.form.get('sem')
        day = request.form.get('day')
        c1 = request.form.get('c1')
        c2 = request.form.get('c2')
        c3 = request.form.get('c3')
        c4 = request.form.get('c4')
        c5 = request.form.get('c5')
        c6 = request.form.get('c6')
        c7 = request.form.get('c7')

        new_timetable = {
            "course": course,
            "sem": sem,
            "day": day,
            "class1": c1,
            "class2": c2,
            "class3": c3,
            "class4": c4,
            "class5": c5,
            "class6": c6,
            "class7": c7
        }
        timetable = db.timetable
        q = {
            "course": course,
            "sem": sem,
            "day": day,
            "class1":c1,
            "class2": c2,
            "class3": c3,
            "class4": c4,
            "class5": c5,
            "class6": c6,
            "class7": c7,

             }

        timetable.insert_one(new_timetable)
        print("record inserted")
        msg = "We have added the student to the list"
        return render_template('admin.html')

#add student attendance
@app.route('/add_attendance_page')
def add_attendance_page():  # put application's code here
    return render_template('add_attendance_page.html')

@app.route('/add_attendance',methods =["GET", "POST"])
def add_attendance():

    data = datetime.datetime.now()
    print(data)
    d = data.strftime('%m%d%Y')
    if request.method == "POST":
        usn = request.form.get('course')
        dd = d#date in mmddyyyy formant
        c1 = request.form.get('c1')
        c2 = request.form.get('c2')
        c3 = request.form.get('c3')
        c4 = request.form.get('c4')
        c5 = request.form.get('c5')
        c6 = request.form.get('c6')
        c7 = request.form.get('c7')
        attend = db.attendance
        new_attendance = {
            "usn": usn,
            "date": dd,
            "class1":c1,
            "class2": c2,
            "class3": c3,
            "class4": c4,
            "class5": c5,
            "class6": c6,
            "class7": c7,

             }
        attend.insert_one(new_attendance)
        print("record inserted")
        print("student attendance added")
        msg = "We have added the student to the list"
        return render_template('admin.html')



@app.route('/search_attendance_page')
def search_attendance_page():
    return render_template("search_attendance_page.html")



@app.route('/search_attendance',methods =["GET", "POST"])
def search_attendance():
    if request.method == "POST":
        dd = request.form.get('date')
        attend = db.attendance

        query = {"date": dd}
        res = attend.find(query)
        # table in html to be done
        return render_template('search_attendance_result.html',res=res)

#student feedback page
@app.route('/feedback_page')
def feedback_page():
    return render_template("feedback_page.html")


@app.route('/feedback',methods =["GET", "POST"])
def feedback():
    if request.method == "POST":
        usn = request.form.get('usn')
        text = request.form.get('feed')
        print(text)
        corpus = []
        review = re.sub('[^a-zA-Z]', ' ', text)
        review = review.lower()
        review = review.split()
        ps = PorterStemmer()
        review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
        review = ' '.join(review)
        corpus.append(review)

        z = cv.transform(corpus).toarray()
        v = model.predict(z)
        if v[0] == 1:
            status="positive"
            st = "positive"
        if v[0] ==0:
            status="negative"
            st="valuable"
        print(status)
        feed = db.feedback
        new = {
            "usn":usn,
            "feedback":text,
            "sentiment":status
        }
        feed.insert_one(new)
        print("record inserted")
        return render_template('feedback_page.html',stat=st)


@app.route('/admin_feedback_page')
def admin_feedback_page():
    feed = db.feedback
    dat = feed.find()
    return render_template("admin_feedback.html",data=dat)




if __name__ == '__main__':
    app.run()
