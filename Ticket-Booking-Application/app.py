from flask import Flask,render_template,redirect,request,url_for
import data,re,validationFunctions


app=Flask(__name__)

# Function to Direct Index Page
@app.route('/')
def index():
    return render_template('index.html')


#Function to Direct Login Page
@app.route('/login',methods=['post','get'])
def login():
    return render_template('login.html')


#Function to Direct Signup Page
@app.route('/signup',methods=['post','get'])
def signup():
    return render_template('signup.html')


#Function to Direct Notification Page
@app.route('/notification',methods=['post','get'])
def notification():
    image="/static/images/tick1.gif"
    msg1="Congratulation!"
    msg2="Your Account has been Successfully Created!!"
    return render_template("notification.html",image=image,msg1=msg1,msg2=msg2)

# Function to insert Values to the Database get from the HTML 
@app.route('/insertUser',methods=['post','get'])
def insertUser():
    fullname=request.form['fullname']
    username=request.form['username']
    email=request.form['email']
    phone=request.form['phone']
    password=request.form['password']
    cpassword=request.form['cpassword']
    gender = request.form.get('gender')

    
    if not validationFunctions.checkValidation.emailCheck(email):
        return render_template('notification.html',image="/static/images/image2.gif",msg1="Ooops!",msg2='Provide Valid Mail Id....',msg3='/signup')

    if not validationFunctions.checkValidation.phoneNoCheck(phone):
        return render_template('notification.html',image="/static/images/image2.gif",msg1="Ooops!",msg2='Provide Valid Phone Number....',msg3='/signup')

    if not validationFunctions.checkValidation.passwordCheck(password):
        return render_template('notification.html',image="/static/images/image2.gif",msg1="Password Does not Match Constraints..",msg2='Requirements:At least 8 characters long.Contains at least one uppercase letter.Contains at least one lowercase letter.Contains at least one digit.Contains at least one special character (e.g., !@#$%^&*()).',msg3='/signup')

    if(cpassword!=password):
        return render_template('notification.html',image="/static/images/image2.gif",msg1="Ooops!",msg2='Passwords are Not Same....',msg3='/signup')
    

    result=data.dbConnection.insertUsers(fullname=fullname,username=username,email=email,mobile=phone,password=password,gender=gender)
    if result=='Success':
        return render_template('notification.html',image="/static/images/tick1.gif",msg1="Congratulation!",msg2="Your Account has been Successfully Created!!",msg3='/login')
    elif result=='UNIQUE constraint failed: users.username':
        return render_template('notification.html',image="/static/images/image2.gif",msg1="Ooops!",msg2='Username Already Exists....',msg3='/login')
    else:
        return render_template('notification.html',image="/static/images/image2.gif",msg1="Ooops!",msg2=result,msg3='/signup')
    

# Function Use dto Check the user existence and allow for Login
@app.route('/checkUser',methods=['post','get'])
def checkUser():
    username = request.form['username']
    password = request.form['password']
    if(username=='admin' and password=='admin'):
        return redirect(url_for('adminhome'))
    result=data.dbConnection.checkUser(username=username,password=password)
    if result=='True':
        #  return  redirect(url_for('.userhome',username=username))
         return render_template('notification.html',image="/static/images/tick1.gif",msg1="Congratulation!",msg2="Your Login Sucess!!",msg3='/userhome',msg4=username)
    elif result=='False':
        return render_template('notification.html',image="/static/images/image2.gif",msg1="Ooops!",msg2='Your Password is Wrong!!!',msg3='/login')
    elif result=='Username Does Not Exists...':
        return render_template('notification.html',image="/static/images/image2.gif",msg1="Ooops!",msg2=result,msg3='/login')
    else:
        return render_template('notification.html',image="/static/images/image2.gif",msg1="Ooops!",msg2=result,msg3='/')


# Function to Check the Existence of Username
@app.route('/checkUserName',methods=['post','get'])
def checkUserName():
    username = request.form['username']
    result=data.dbConnection.checkUser(username=username,password='')
    if result=='Username Does Not Exists...':
        return render_template('signup.html',uName=username)
    elif result=='True' or result=='False':
        return render_template('notification.html',image="/static/images/image2.gif",msg1="Ooops!",msg2='UserName Allready Exists!!!',msg3='/login')
    else:
        return render_template('notification.html',image="/static/images/image2.gif",msg1="Ooops!",msg2=result,msg3='/')

# Function to Direct to UserHome page
@app.route('/userhome',methods=['post','get'])
def userhome():
    username=request.form['username']
    details=data.dbConnection.getUserData(userName=username)
    buses=data.dbConnection.getBusData()
    mybookings=data.dbConnection.getUserBookingData(userName=username)
    return render_template('userhome.html',details=details,buses=buses,mybookings=mybookings)

# Function to register Tickets
@app.route('/registertickets',methods=['post','get'])
def registertickets():
    no_of_passengers = request.form['no_of_passengers']
    username=request.form['username']
    id=request.form['id']
    idcheck=data.dbConnection.checkBusId(id=id)
    if not idcheck:
        return render_template('notification.html',image="/static/images/image2.gif",msg1="Ooops!",msg2="Enter Proper Bus Id...",msg3='/userhome',msg4=username)
    result=data.dbConnection.updateBookingData(username=username,id=id,no=no_of_passengers)
    if result=="Your Tickets are Confirmed. Have a Nice Day!!!":
        print("Your Tickets are Confirmed. Have a Nice Day!!!")
        return render_template('notification.html',image="/static/images/tick1.gif",msg1="Congratulation!",msg2="Your Tickets are Confirmed. Have a Nice Day!!!",msg3='/userhome',msg4=username)
    print(result,'\n')
    if result=="Seats are less than the availability..":
        return render_template('notification.html',image="/static/images/image2.gif",msg1="Ooops!",msg2="Seats are less than the availability..",msg3='/userhome',msg4=username)
    return render_template('notification.html',image="/static/images/image2.gif",msg1="Ooops!",msg2="Error",msg3='/userhome',msg4=username)

# Function for Admin Home Page
@app.route('/adminhome')
def adminhome():
    buses=data.dbConnection.printBus()
    bookings=data.dbConnection.printBooking()
    users=data.dbConnection.printUsers()
    return render_template('adminhome.html',buses=buses,bookings=bookings,users=users)

# Function For Adding Bus Details
@app.route('/addBus',methods=['post','get'])
def addBus():
    no=request.form['BusNo']
    type=request.form['BusType']
    route=request.form['route']
    seats=request.form['seat']
    price=request.form['price']
    res=data.dbConnection.addBusData(no=no,type=type,route=route,seats=seats,price=price)
    return redirect(url_for('adminhome'))

# Function For Deleting Bus 
@app.route('/deleteBus',methods=['post','get'])
def deleteBus():
    id=request.form['busId']
    res=data.dbConnection.removeBusData(id)
    return redirect(url_for('adminhome'))


if __name__=="__main__":
    app.run(host="0.0.0.0",port="8080",debug=True)
