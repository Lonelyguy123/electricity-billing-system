import mysql.connector
from mysql.connector import Error

def create_database():
    try:
        # First connect without selecting a database
        conn = mysql.connector.connect(
            host='localhost',
            user="Shastha",
            password="idkbro"
        )
        
        if conn.is_connected():
            cursor = conn.cursor()
            
            # Create database if it doesn't exist
            cursor.execute("CREATE DATABASE IF NOT EXISTS electricbill")
            print("Database 'electricbill' created successfully")
            
            # Switch to the electricbill database
            cursor.execute("USE electricbill")
            
            # Create table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS electricbill (
                    name varchar(30), 
                    monyear varchar(30),
                    pu integer,
                    tamount integer
                );
            """)
            print("Table 'electricbill' created successfully")
            
            return conn
            
    except Error as e:
        print(f"Error: {e}")
        return None

# Initial database connection
try:
    # Try to connect to existing database first
    conn = mysql.connector.connect(
        host='localhost',
        user="Shastha",
        password="idkbro",
        database="electricbill"
    )
except Error:
    # If database doesn't exist, create it
    print("Database not found. Creating new database...")
    conn = create_database()

if conn is not None and conn.is_connected():
    print("""--------------------------------Electricity Billing System----------------------------------
    
    """)
    print("""--------------------------------Version 1.1.1-------------------------------------------------
    
    """)
    cursor = conn.cursor()

def setup():
    question = input("""do you want to setup the application? Respond with 'y' to setup, 'n' to skip (only for first time): 
    """)
    
    if question.lower() == 'y':
        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS electricbill (
                name varchar(30), 
                monyear varchar(30),
                pu integer,
                tamount integer
                );""")
            print("Finished setting up the application")
        except Error as e:
            print(f"Error during setup: {e}")
    else:
        print("Setup skipped")

def calc():
    try:
        pu = 0.0
        time = 0
        name = input("""Enter your name:  
        
        """)
        n = int(input("""Enter no of appliances: 
        
        """))
        
        for i in range(n):
            pr = float(input("Power rating of the appliance: " + " " + str(i+1) + ":"))
            t = int(input("""Enter the usage time(in hours)

                """))
            pu += (pr*t/1000)
        
        if pu <= 100:
            amount = pu * 4.22
        elif pu > 100 and pu <= 200:
            amount = (100*4.22)+(pu-100)*5.02
        else:
            amount = (100 * 4.22) + (100 * 5.02) + (pu-200) * 5.87
            
        print("""Fixed charge of rupees 40 and energy duty of 0.15 rupees per unit is applicable

            """)
        tamount = amount + 40 + (pu*0.15)
        print("Your total bill is ", tamount)
        monyear = input("""Enter the month and year of the bill in the form mm-yyyy: 

            """)
        
        sql = "INSERT INTO electricbill(name,monyear,pu,tamount) VALUES('{}','{}',{},{});".format(name,monyear,pu,tamount)
        cursor.execute(sql)
        conn.commit()
        print("Bill saved successfully!")
        
    except Error as e:
        print(f"Error saving bill: {e}")
        conn.rollback()

def find():
    try:
        monthfinder = input("""Enter the month and year in the form mm-yyyy
        """)
        namefinder = input("""Enter your name:
        """)
        
        sql = "SELECT * FROM electricbill WHERE name = '{}' AND monyear = '{}' ".format(namefinder,monthfinder)
        cursor.execute(sql)
        results = cursor.fetchall()
        
        if results:
            print("""Here is the data from the date in the form (name,month,average power consumption(KWh), bill(in rupees):""")
            print(results)
        else:
            print("No bills found for the specified month and name.")
            
    except Error as e:
        print(f"Error finding bill: {e}")

def findall():
    try:
        namefinder = input("Enter your name(first letter caps): ")
        sql = "SELECT * FROM electricbill Where name = '{}'".format(namefinder)
        cursor.execute(sql)
        results = cursor.fetchall()
        
        if results:
            print("Here are all the bills listed with the name " + namefinder)
            print(results)
        else:
            print("No bills found for the specified name.")
            
    except Error as e:
        print(f"Error finding bills: {e}")

def comm_appliance():
    print("----------------------------Wattage of Common Appliances---------------------------")
    print("""No. Appliance                      Min    Max    Standby
     1.  32 InchLEDTV                    20W    60W    1W
     2.  Refrigerator                    100W   200W   N/A
     3.  Washing Machine                 500W   500W   1W
     4.  100W light bulb (Incandescent)  100W   100W   0W
     5.  Electric Pressure Cooker        1000W  1000W  N/A
     6.  Inverter Air conditioner        1300W  1800W  N/A
     7.  Iron                            1000W  1000W  N/A
     8.  Laptop Computer                 50W    100W   N/A
     9.  LED Light Bulb                  7W     10W    0W
     10. Pedestal Fan                    50W    60W    N/A""")

def softinfo():
    print("-----------------------------Software Information----------------------")
    print("Version: 1.1.1")
    print("Latest Patch: 17/2/2022")
    print("Python version: 3.9")
    print("MySQL Version: 8.0.28")
    print("""------------------------v1.1.1 Patch Notes--------------------------------
             - Minor changes in the menu
             - Added monthly billing instead of billing by date
             - Added automatic database creation
    """)

def menu(menyoo):
    if menyoo == 1:
        calc()
    elif menyoo == 2:
        find()
    elif menyoo == 3:
        findall()
    elif menyoo == 4:
        comm_appliance()
    elif menyoo == 5:
        setup()
    elif menyoo == 6:
        softinfo()
    elif menyoo == 7:
        try:
            cursor.close()
            conn.close()
            print("Application closed successfully.")
        except Error as e:
            print(f"Error closing connection: {e}")

def main():
    menyoo = 1
    while menyoo in range(1, 8):  # Changed to include 7
        print("------------------------------Main Menu-----------------------------")
        print("1. Calculate a electricity bill")
        print("2. View previous bills")
        print("3. View all previous bills of a user")
        print("4. View wattage of common appliances")
        print("5. Installation Setup for firsttimers")
        print("6. View Software Information")
        print("7. Exit the application")

        try:
            menyoo = int(input("Enter your choice(1-7): "))
            if menyoo not in range(1, 8):
                print("Please enter a valid choice between 1 and 7")
                continue
            menu(menyoo)
            if menyoo == 7:
                break
        except ValueError:
            print("Please enter a valid number between 1 and 7")

if __name__ == "__main__":
    if conn is not None and conn.is_connected():
        try:
            main()
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
                print("MySQL connection closed.")
    else:
        print("Failed to establish database connection. Please check your MySQL server and credentials.")