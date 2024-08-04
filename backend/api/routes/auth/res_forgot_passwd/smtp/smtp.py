import smtplib


class SmtpTools:
    def __init__(self, host: str, port: int, email: str, password: str):
        self.email = email

        self.server = smtplib.SMTP_SSL(host=host, port=port, timeout=10)
        self.server.login(email, password)

    def send_email(self, to_email: str, code: str):
        subject = '[Web_Example_Project] Password Reset'
        message = (f'Web_Example_Project Password Reset\n\nHello,\nWe have received a request '
                   f'to reset the password for your Web_Example_Project account: {to_email}.\n\n'
                   f'Your reset password code:{code}')

        self.server.sendmail(self.email, to_email, f"Subject: {subject}\n\n{message}")

    def __del__(self):
        self.server.quit()
