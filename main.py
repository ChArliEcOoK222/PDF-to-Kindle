# how can I web scrape to find free pdf books?
# how can I download these PDF files?

# importing the required libraries for this program to run
import subprocess, email, smtplib, ssl, sys, os
from pathlib import Path
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# storing all of the files of the directory in a variable
files = os.listdir('PATH TO BOOK FILES')
finished_convert = False

# iterating over the files in order to find those that end in pdf
for file in files:
    if 'pdf' in file:
        # saving the path of all pdf files to a variable
        path =  os.path.abspath(f'PATH TO BOOK FILES{file}')
        # creating the new path of the epub files and saving them to a variable
        convert_format = str(path).replace('pdf', 'epub')
        # running the ebook-convert command of the calibre CLI using the two paths
        subprocess.call(["ebook-convert", path, convert_format])
        finished_convert = True
        if finished_convert == True:
            os.remove(path)
            
# creating the template of the email and using app password
body = "This is an email with attachment sent from Python"
sender_email = "PERSONAL EMAIL ADDRESS"
receiver_email = "KINDLE EMAIL ADDRESS"
password = "PASSWORD"

# creating a multipart message and setting headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email

# storing all of the files of the directory in a variable
files = os.listdir('PATH TO BOOK FILES')

# iterating over the files in order to find those that end in pdf
for file in files:
    if 'epub' in file:
        filename = file
        path =  os.path.abspath(f'PATH TO BOOK FILES{file}')
        # Open EPUB file in binary mode
        with open(path, "rb") as attachment:
            # adding file as application/octet-stream
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

            # encoding file in ASCII characters to send by email    
            encoders.encode_base64(part)

            # adding header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )

            # adding attachment to message and converting message to string
            message.attach(part)
            text = message.as_string()

# logging in to server using secure context and sending email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)