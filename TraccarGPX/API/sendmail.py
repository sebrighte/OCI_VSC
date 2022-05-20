def sendmail(subject, message):
    import smtplib, ssl

    smtp_server =  "smtp.office365.com"
    port = 587
    sender_email = "ernie_sebright@hotmail.com"
    password = "Janu2019!"

    # smtp_server = "smtp.gmail.com"
    # port = 587  # For starttls
    # sender_email = "ernie.sebright@gmail.com"
    # password = "Janu2019!" #input("Type your password and press enter: ")
    message = f"""Subject: {subject}\n{message}"""

    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server,port)
        #server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        #server.ehlo() # Can be omitted
        server.login(sender_email, password)
        # TODO: Send email here
        server.sendmail(sender_email, sender_email, message)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit() 

sendmail("TestSub", "TestMsg")