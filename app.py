from flask import *
import os
from flask_mail import *
from flask_session import Session
from random import *
from flask_mysqldb import MySQL
import hashlib
from werkzeug.utils import secure_filename
import zipfile
import shutil
import socket

app=Flask(__name__)
app.secret_key = "supers secret key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['MYSQL_HOST']= "localhost"
app.config['MYSQL_USER']= "root"
app.config['MYSQL_PASSWORD']= "praval@123"
app.config['MYSQL_DB']= "steelplant" 
app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_USERNAME"] = 'mp936@snu.edu.in'  
app.config['MAIL_PASSWORD'] = 'Xevfuj-befnex-cewme9'      
app.config["MAIL_PORT"] = 465     
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True 
UPLOAD_FOLDER = '/Users/pravalmaddala/Documents/GitHub/SteelPlant/Files'  # Specify the folder where you want to save the uploaded files
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Session(app)
mail=Mail(app)
mysql=MySQL(app)
socket.gethostbyname("")
otp = randint(0000,9999)  

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password=request.form['password']
        cur=mysql.connection.cursor()
        cur.execute('SELECT * FROM user WHERE email = %s', [email])
        account = cur.fetchone()
        if account:
            a=hashlib.md5(password.encode())
            aa=a.hexdigest()
            if(aa==account[3]):
            # cur=mysql.connection.cursor()
            # cur.execute('SELECT * FROM user WHERE email = %s AND password=MD5(%s)', ([email],[password]))
            # accounts= cur.fetchone()
                session['loggedin']= True
                session['name']=account[1]
                session['email']=account[2]
                session['id']=account[0]
                return render_template('team_confirm.html',data=account)
            else:
                return render_template('login.html',msg="Password is entered incorrectly!")
        else:
            return render_template('login.html',msg="Email-ID is entered incorrectly!")
    return render_template('login.html')


@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        pas = request.form['password']
        cpass = request.form['cpassword']
        if(pas!=cpass):
            return render_template('signup.html',msg="Passwords Dont Match!")
        else:
            cur=mysql.connection.cursor()
            cur.execute('SELECT * FROM user WHERE email = %s', (email,  ))
            account = cur.fetchone()
            if account:
                return render_template('signup.html',msg="Account Exists!")
            else:
                msg = Message('OTP',sender = 'mp936@snu.edu.in', recipients = [email]) 
                msg.body = str(otp)  
                mail.send(msg)   
                return render_template('verify.html',name=name,email=email,pas=pas,cpass=cpass,otp=otp)
    return render_template('signup.html')

@app.route('/verify',methods=["POST"])  
def verify():  
    user_otp = request.form['otp']  
    if otp == int(user_otp):  
        name = request.form['name']
        email = request.form['email']
        pas = request.form['pass']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO user (name,email,password) VALUES (%s,%s,MD5(%s))",(name,email,pas))
        mysql.connection.commit()
        cur.close()
        cur=mysql.connection.cursor()
        cur.execute('SELECT * FROM user WHERE email = %s', (email,))
        account = cur.fetchone()
        # Create session data, we can access this data in othr routes
        session['loggedin']= True
        session['name']=account[1]
        session['email']=account[2]
        session['id']=account[0]

        return render_template('team_confirm.html',data=account)
    else:
        render_template('signup.html',msg="Verification Failed!") 
    return render_template('home.html')
@app.route('/upload', methods=['POST'])
def upload():
    if session['loggedin']== True:
        uploaded_file = request.files['file']
        if uploaded_file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)
            return render_template('home.html',msg='File uploaded and saved successfully')
        return render_template('home.html',msg='No file uploaded')
@app.route('/reviews',methods=['GET','POST'])
def reviews():
    return "hi"
@app.route('/new_team',methods=['GET','POST'])
def new_team():
    if request.method == 'POST':
        title = request.form['title']
        name = request.form['name']
        desc = request.form['desc']
        id1=session['id']
        mail=session['email']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO team (title,name,desci,id1,mail) VALUES (%s,%s,%s,%s,%s)",(title,name,desc,id1,mail))
        mysql.connection.commit()
        cur=mysql.connection.cursor()
        cur.execute('SELECT * FROM team WHERE title = %s AND name=%s AND id1=%s', (title,name,id1))
        account= cur.fetchone()
        session['teamid']=account[0]
        return render_template('add_team.html')
    return render_template('new_team.html')
@app.route('/old_team',methods=['GET','POST'])
def old_team():
    return render_template('old_team.html')
@app.route('/team',methods=['GET','POST'])
def team():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM team WHERE teamlead = %s OR member2= %s OR member2= %s OR member2= %s OR member2= %s', (session['id'],session['id'],session['id'],session['id'],session['id'],))
    account = cur.fetchone()
    if account:
        return render_template('team.html',data=account)
    
    else:
        return render_template('team.html',msg="You Havent formed a team",data=[])
    
    
if __name__ == "__main__":
        app.run(debug=True,port=5000)

