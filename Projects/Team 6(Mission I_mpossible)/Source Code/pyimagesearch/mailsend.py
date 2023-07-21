import smtplib
from email.mime.text import MIMEText

class mailSend:
    def __init__(self, userEmail):
        self.smtpServer = "smtp.naver.com"
        self.projectEmail = "wjstmdnr@naver.com"
        f = open('pw.txt', 'r')
        self.projectPw = f.readline()
        self.smtpPort = 587
        self.userEmail = str(userEmail)

    def send(self, title, content):
            
        message = MIMEText(content, _charset="utf8")

        message['Subject'] = title 
        message['From'] = self.projectEmail
        message['To'] = self.userEmail
                
        smtp = smtplib.SMTP(self.smtpServer, self.smtpPort)
        smtp.ehlo
        smtp.starttls()

        smtp.login(self.projectEmail, self.projectPw)

        smtp.sendmail(message['From'], message['To'].split(','), message.as_string())

        smtp.quit()