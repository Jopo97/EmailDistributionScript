# Email distribution program created by Jonah McElfatrick for CMP311 Professional Project Development and Delivery
# Finished on 24/02/2020
import csv
from email.utils import formatdate
from socket import gaierror
import email_to
import os

contacts = []
names = []

def read_contacts():
    # Read in the contacts csv file to store the emails and names into arrays
    print ("To distribute the emails, this system requires a CSV (Comma Separated Values) file that includes the email and first name of the recipients")
    print ("Please include the CSV file in the same directory as this file")
    file_name = input("Please enter the name of the contacts CSV file (format: contacts.csv): ")
    print ("\n")
    # Validate that the entered file is a .csv file
    file_name = validate_file_csv(file_name)

    # Attempt to open the file and read the contents
    try:
        with open(file_name) as csv_file:
            contents = csv.reader(csv_file, delimiter=',')
            contact_count = 0
            # Add the contents of the file to the contacts and name arrays
            for (email, name) in contents:
                contacts.append(email)
                names.append(name)
                contact_count += 1
    # Error if unable to open the file, this could be due to non existent file or a error in logic
    except:
        print ("Error opening file " + file_name + "\n")

def input_validation(value_min,value_max,value):
    # integer input validation for within a specific range
    while (value < value_min or value > value_max):
        print ("Value entered is out of range!\n")
        value = input("Please enter a value between " + value_min + " and " + value_max + ": ")
        print ("\n")
    return value

def validate_file_csv(data):
    # Check to see if the selected file is a .csv file
    # Splits the string before and after the '.' to get the filename and extension
    name, end = os.path.splitext(data)
    while (end != '.csv'):
        # Will repeatedly ask the user for a file name until the user enters a .csv file
        print ("File type entered does not match that required \n")
        data = input("Please enter a filename with filetype csv: ")
        name, end = os.path.splitext(data)
    return data

def validate_file_txt(data):
    # Check to see if the selected file is a .txt file
    # Splits the string before and after the '.' to get the filename and extension
    name, end = os.path.splitext(data)
    while (end != '.txt'):
        # Will repeatedly ask the user for a file name until the user enters a .txt file
        print ("File type entered does not match that required \n")
        data = input("Please enter a filename with filetype txt: ")
        name, end = os.path.splitext(data)
    return data

def pick_choices():
    # Allows for the user to pick which type of email they are wanting to distribute, from a specialised email or a generalised email
    choice = 0
    print ("This system is designed to allow the distribution of phishing emails that to a list of contacts that is inputted through a csv file \n")
    print ("There are three implementations in this program. The three implementations are : \n")
    print ("1: Specialised Email")
    print ("2: Generalised Email")
    print ("3: Custom Email")
    print ("\n")
    choice = input ("Which option would you like to select?: ")
    # Validate that the user input is within the range specified
    choice = input_validation('1','3',choice)
    print ("\n")
    return choice

def read_email(choice):
    # Attempt to login to the server
    try:
        server = email_to.EmailServer('smtp.gmail.com', 587, 'GMAIL EMAIL ADDRESS', 'GMAIL PASSWORD')
    except:
        print("Cannot connect to the server")

    try:
        # Check to see if the user is wanting a specified email or a general one
        if (choice == '1'):
            # If choice is equal to 1, then the level of sophistication for the specialised email is requested
            soph_level = input("Please enter the level of sophistication that the email should represent from 1 to 3 (1 - Lowest Sophistication, 3 - Highest Sophistication): ")
            # Validate that the user input is within the range specified
            soph_level = input_validation('1','3',soph_level)
            print ("\n")

            if (soph_level == '1'):
                # Lowest level of sophistication
                filename = "low.txt"
                
            elif (soph_level == '2'):
                # Middle level of sophistication
                filename = "middle.txt"

            elif (soph_level == '3'):
                # Highest level of sophistication
                filename = "high.txt"

            email_sender = 'REPLACE WITH SPOOF EMAIL'
            email_subject = 'Password is about to expire'
            
        elif (choice == '2'):
            # If choice is equal to 2, then the general instance of a phishing scam will be loaded and sent out to the contacts list
            filename = "GeneralScam/GeneralEmail.txt"
            email_sender = 'microsoftitservice@outlook.com'
            email_subject = 'Two Factor Authentication Code'

        elif (choice == '3'):
            # If choice is equal to 3, then the user is asked for the custom email sender, subject and file name
            email_sender = input("Please enter the email sender you wish to appear on the email: ")
            email_subject = input("Please enter the email subject you wish to appear on the email: ")
            print ("For a custom email to be distributed, a .txt file with the email contents must be loaded. Please include this file in the same directory as this python file.")
            filename = input("Please enter the name of the custom email file you wish to distribute:")
            filename = validate_file_txt(filename)
            print ("\n")
              
        # Read in the email file and add the contents to the email message variable
        file = open(filename,mode='r')
        file_contents = file.read()
        file.close()
        message = email_to.Message(file_contents)

        # Contacts counter to keep track of which position in the array the program is at
        contact_count = 0
        
        for x in contacts:
            # Set the email receiver and the name of the receiver at the same position in the array
            email_receiver = [x]
            name = names[contact_count]
            contact_count += 1
            
            try:
                # Send out the emails to the contacts list entered
                server.send_message(message, x, email_subject)
                print ("Email sent to " + x)
                
            except:
                # Error with the try statement above sending the email, this could be due to bad parameters or mislabelled variables
                print ("Email cannot be sent!")
                
    except Exception as e:
        # Print out an error message if there is an error in the above code
        print("Cannot connect to the server. Possible bad password or for Gmail, 'Less secure app access may be turned off'.")

def main():
    # 3 functions are called from the main function. The first is the choice for a specialised email or a generalised email.
    # Second is the reading of the contacts file. Third is the reading of the chosen email and the sending of the email.
    try:
        choice = pick_choices()
        read_contacts()
        read_email(choice)
        
    except Exception as e:
        # Print out an error message if there is an error in connecting to the server, this could be due to a error in logic
        print("Cannot connect to the server. \n Possible bad password or for Gmail, 'Less secure app access' may be turned off.")
    #finally:
     #   server.close()

# Call main function to start program
main()
