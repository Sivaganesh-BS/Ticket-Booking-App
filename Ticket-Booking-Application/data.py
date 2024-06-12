import sqlite3


class dbConnection:
    # __Init__ Function to Start the DB connection and Create the Required Tables
    def __init__(self) -> None:
        
        try:
            con = sqlite3.connect('records.db')
            cur = con.cursor()
            # User data Table
            cur.execute("""CREATE TABLE users(
                        fullname text,
                        username text,
                        email text,
                        mobile integer,
                        password text,
                        gender text,
                        Primary Key(username) )
                            """)
            con.commit()
            print('Table User Created')

            #Bus Table
            cur.execute('''CREATE TABLE bus (
                                             id integer primary key AUTOINCREMENT,
                                             busno integer, 
                                             type text,
                                             route text, 
                                             price integer, 
                                             seat integer)
                                             ''')
            con.commit()
            print("Table Bus Created")

            # Booking Table
            cur.execute("""CREATE TABLE booking(
                                    bookingid integer Primary Key AUTOINCREMENT,
                                    id integer,
                                    username text,
                                    totalfair integer,
                                    no_of_passengers integer,
                                    Foreign Key (id) REFERENCES bus(id),
                                    Foreign Key (username) REFERENCES bus(username) )
                                        """)
            con.commit()
            print("Table Booking Created")

        except Exception as e:
            print(str(e).upper())
        finally:
            cur.close()
            con.close()
            print('DataBase Closed...')

    # Function to Check the user Existence and Login
    def checkUser(username,password=''):
        try:
            con = sqlite3.connect('records.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE username=?", (username,))
            uName = cur.fetchone()
            con.commit()
            if uName:
                if uName[4]==password:
                    return 'True'
                else:
                    return 'False'
            else:
                return 'Username Does Not Exists...'
            
        except Exception as e:
            return e
        finally:
            cur.close()
            con.close()
            print('DataBase Closed...')

    # Function to  Insert User Details into the Database
    def insertUsers(fullname,username,email,mobile,password,gender):
        try:
            con = sqlite3.connect('records.db')
            cur = con.cursor()
            cur.execute("INSERT INTO users(fullname,username,email,mobile,password,gender) VALUES (?,?,?,?,?,?)", 
                        (fullname,username,email,mobile,password,gender))
            con.commit()
            print("User details Inserted...")
            return "Success"
        except Exception as e:
            return e 
        finally:
            cur.close()
            con.close()
            print('DataBase Closed...')


    # Function to print All users details
    def printUsers():
        try:
            print("Printing All User Table Details")
            con = sqlite3.connect('records.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM users")
            con.commit()
            result=cur.fetchall()
            for i in result:
                print(i)
            return result
        except Exception as e:
            return e 
        finally:
            cur.close()
            con.close()
            print('DataBase Closed...','\n')

    # Function to print All Bus details
    def printBus():
        try:
            print("Printing All Bus Table Details")
            con = sqlite3.connect('records.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM bus")
            con.commit()
            result=cur.fetchall()
            for i in result:
                print(i)
            return result
        except Exception as e:
            return e 
        finally:
            cur.close()
            con.close()
            print('DataBase Closed...','\n')
    
    # Function to print All Booking details
    def printBooking():
        try:
            print("Printing All Booking Table Details")
            con = sqlite3.connect('records.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM booking")
            con.commit()
            result=cur.fetchall()
            for i in result:
                print(i)
            return result
        except Exception as e:
            return e 
        finally:
            cur.close()
            con.close()
            print('DataBase Closed...','\n')

    # Function to Get the User Details
    def getUserData(userName):
        try:
            con = sqlite3.connect('records.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE username=?",(userName,))
            con.commit()
            result=cur.fetchall()
            return result[0]
        except Exception as e:
            return e 
        finally:
            cur.close()
            con.close()
            print('DataBase Closed... By Siva')

    # Function to get the Bus Details
    def getBusData():
        try:
            con = sqlite3.connect('records.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM bus")
            con.commit()
            result=cur.fetchall()
            print("Data retrived Successfully....")
            return result

        except Exception as e:
            print(e,'\n')
        finally:
            cur.close()
            con.close()
            print("Database Closed Successfully...",'\n')

    
    # Function to get the User Booking Details
    def getUserBookingData(userName):
        try:
            con = sqlite3.connect('records.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM booking WHERE username=?",(userName,))
            con.commit()
            result=cur.fetchall()
            print("Data retrived Successfully....")
            return result

        except Exception as e:
            print(e,'\n')
        finally:
            cur.close()
            con.close()
            print("Database Closed Successfully...",'\n')


    # Function to Update the Booking Table Data
    def updateBookingData(username,id,no):
        try:
            id=int(id)
            no=int(no)
            con = sqlite3.connect('records.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM bus WHERE id=?",(id,))
            con.commit()
            res=cur.fetchall()
            result=res[0]
            if(result[5]<no):
                print("Seats are less than the availability..")
                return "Seats are less than the availability.."
            newSeat=result[5]-no 
            totalfair=result[4]*no
            cur.execute("UPDATE bus SET seat=? WHERE id=?",(newSeat,id))
            con.commit()
            cur.execute('INSERT INTO booking(id,username,totalfair,no_of_passengers) VALUES(?,?,?,?)',(id,username,totalfair,no))
            con.commit()
            print("Data Updated Successfully....")
            return "Your Tickets are Confirmed. Have a Nice Day!!!"

        except Exception as e:
            print(e,'\n')
            return e
        finally:
            cur.close()
            con.close()
            print("Database Closed Successfully...",'\n')
    

    #Function to Check the valid Bus Id
    def checkBusId(id):
        try:
            con = sqlite3.connect('records.db')
            cur = con.cursor()
            cur.execute("SELECT * FROM bus WHERE id=?",(id,))
            con.commit()
            result=cur.fetchall()
            print("Data retrived Successfully....")
            return result

        except Exception as e:
            print(e,'\n')
        finally:
            cur.close()
            con.close()
            print("Database Closed Successfully...",'\n')


    #Function to Add Bus Data Details
    def addBusData(no,type,route,seats,price):
        try:
            con = sqlite3.connect('records.db')
            cur = con.cursor()
            cur.execute('INSERT INTO bus(busno,type,route,price,seat) VALUES(?,?,?,?,?)',(no,type,route,price,seats))
            con.commit()
            result=cur.fetchall()
            print("Data retrived Successfully....")
            return result

        except Exception as e:
            print(e,'\n')
            return e
        finally:
            cur.close()
            con.close()
            print("Database Closed Successfully...",'\n')

    # Function to Delete Bus Data
    def removeBusData(id):
        try:
            con = sqlite3.connect('records.db')
            cur = con.cursor()
            cur.execute('DELETE FROM bus WHERE id = ?',(id,))
            con.commit()
            print("Bus Data Removed Successfully....")
            return "Success"

        except Exception as e:
            print(e,'\n')
            return e
        finally:
            cur.close()
            con.close()
            print("Database Closed Successfully...",'\n')

    # Function to test the functionality
    def sampleFunction():
        try:
            con = sqlite3.connect('records.db')
            cur = con.cursor()
            cur.execute('INSERT INTO bus(busno,type,route,price,seat) VALUES(5186,"Sleeper","Chennai-Covai",999,45)')
            con.commit()
            print("Data entered Successfully....")

        except Exception as e:
            print(e)
        finally:
            cur.close()
            con.close()
            print("Database Closed Successfully...",'\n')


if __name__ == '__main__':
    # obj = dbConnection()
    # res=dbConnection.updateBookingData('siva',1,45)
    # res=dbConnection.addBusData(no=1234,type='Semi-Sleeper',route='Delhi-Chennai',seats=45,price=550)
    dbConnection.removeBusData(3)
    dbConnection.sampleFunction()
    dbConnection.printUsers()
    dbConnection.printBus()
    dbConnection.printBooking()
    # print(res)
