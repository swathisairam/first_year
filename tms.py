import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="travel"
)

mycursor = mydb.cursor()

start = ["Chennai", "Bengaluru", "Hyderabad", "Mumbai"]
end = ["Manali", "Kodaikanal", "Alleppey", "Leh"]
package_name = ["3days_2nights", "4days_3nights", "5days_4nights"]

def main():
    print("Welcome to Travel Management System")
    register_prompt = int(input("Login or Register:\n1. Login\n2. Register\n"))
    
    if register_prompt == 1:
        current_id = int(input("Enter your user id: "))
        pass_prompt = input("Enter your Password: ")
        mycursor.execute("SELECT password FROM user_details WHERE user_id = %s", (current_id,))
        myresult = mycursor.fetchall()
        
        if myresult and myresult[0][0] == pass_prompt:
            view_details(current_id)
            selection(current_id)
        else:
            print("Enter the correct password")
            main()
    
    elif register_prompt == 2:
        print("Welcome to TMS\nEnter the following details to register your account")
        
        while True:
            lower, upper, special, digit = 0, 0, 0, 0
            password = input("Enter your password: ")
            
            if len(password) >= 8:
                for i in password:
                    if i.islower():
                        lower += 1
                    if i.isupper():
                        upper += 1
                    if i.isdigit():
                        digit += 1
                    if i in ['@', '$', '%']:
                        special += 1
                
                if lower >= 1 and upper >= 1 and special >= 1 and digit >= 1:
                    print("Valid Password")
                    break
                else:
                    print("Invalid Password. Please enter a password with at least one uppercase, lowercase, special character, and digit.")
        
        username = input("Enter your Name: ")
        dob = input("Enter DoB in the format (yyyy-mm-dd): ")
        phone_no = int(input("Enter Phone number: "))
        
        data_user = (password, username, dob, phone_no)
        add_user = "INSERT INTO user_details (password, name, dob, phone) VALUES (%s, %s, %s, %s);"
        mycursor.execute(add_user, data_user)
        mydb.commit()
        
        mycursor.execute("SELECT * FROM user_details WHERE name = %s", (username,))
        myresult = mycursor.fetchall()
        
        for x in myresult:
            print(x)
        
        current_id = myresult[0][0]
        print(current_id)
        selection(current_id)

def selection(current_id):
    function_select = int(input("Select one function:\n1. Create Trip\n2. Edit Trip\n3. Delete Trip\n4. View Trip\n5. Logout\n"))
    
    if function_select == 1:
        create_details(current_id)
    elif function_select == 2:
        update_details(current_id)
    elif function_select == 3:
        delete_details(current_id)
    elif function_select == 4:
        view_details(current_id)
    elif function_select == 5:
        main()

def view_details(current_id):
    print("User Details:")
    mycursor.execute("SELECT * FROM user_details WHERE user_id = %s", (current_id,))
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    
    print("Travel Details:")
    mycursor.execute("SELECT * FROM travel_details WHERE user_id = %s", (current_id,))
    myresult = mycursor.fetchall()
    for x in myresult:
        print(x)
    
    selection(current_id)

def create_details(current_id):
    print("Start cities available:")
    for i, x in enumerate(start, 1):
        print(f"{i}. {x}")
    
    i = int(input("Select Start city: "))
    source_city = start[i - 1]
    
    print("Destination cities available:")
    for j, x in enumerate(end, 1):
        print(f"{j}. {x}")
    
    j = int(input("Select Destination: "))
    destination_city = end[j - 1]
    
    if source_city != destination_city:
        s_date = input("Enter start date (yyyy-mm-dd): ")
        
        print("Packages available:")
        for k, x in enumerate(package_name, 1):
            print(f"{k}. {x}")
        
        k = int(input("Select Package: "))
        selected_package = package_name[k - 1]
        
        mycursor.execute("INSERT INTO travel_details (user_id, source, destination, start_date, package) VALUES (%s, %s, %s, %s, %s)",
                        (current_id, source_city, destination_city, s_date, selected_package))
        mydb.commit()
        
        selection(current_id)
    else:
        print("Enter Different Start and Destination Cities")
        create_details(current_id)

def delete_details(current_id):
    mycursor.execute("DELETE FROM user_details WHERE user_id = %s", (current_id,))
    mycursor.execute("DELETE FROM travel_details WHERE user_id = %s", (current_id,))
    mydb.commit()
    print(f"Successfully deleted details of user ID: {current_id}")
    selection(current_id)

def update_details(current_id):
    update_var = int(input("Do you want to update:\n1. User data\n2. Travel data\n"))
    
    if update_var == 1:
        select_var = int(input("Select attribute to update:\n1. Name\n2. Date of Birth\n3. Phone Number\n"))
        
        if select_var == 1:
            new_name = input("Enter name: ")
            mycursor.execute("UPDATE user_details SET name = %s WHERE user_id = %s", (new_name, current_id))
        elif select_var == 2:
            new_date = input("Enter Date of Birth: ")
            mycursor.execute("UPDATE user_details SET dob = %s WHERE user_id = %s", (new_date, current_id))
        elif select_var == 3:
            new_phone = input("Enter Phone Number: ")
            mycursor.execute("UPDATE user_details SET phone = %s WHERE user_id = %s", (new_phone, current_id))
        
    elif update_var == 2:
        select_var = int(input("Select attribute to update:\n1. Start City\n2. Destination\n3. Start Date\n4. Package\n"))
        
        # Similar update logic for travel details as user details
        
    mydb.commit()
    selection(current_id)

main()
