import umail

# Umail really does all the heavy lifting
class Messenger:
    def __init__(self, email, password, recipients):
        self.sender = email
        self.password = password
        self.recipients = recipients

    def send_message(self, message):
        smtp = umail.SMTP("smtp.gmail.com", 587, username=self.sender, password=self.password)
        smtp.to(self.recipients, mail_from=self.sender)
        smtp.write("From: Doorbell <" + self.sender + ">\n")
        smtp.write("To: " + ", ".join(self.recipients) + "\n")
        smtp.write("Subject: Doorbell Alert\n\n")
        smtp.write(message + "\n")
        smtp.send()
        smtp.quit()