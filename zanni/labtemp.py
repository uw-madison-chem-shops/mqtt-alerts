import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg["Subject"] = "Testing smtplib and email from Python."
msg["From"] = "zannibot@chem.wisc.edu"
msg["To"] = ",".join(["blaise.thompson@wisc.edu", "wjeong25@wisc.edu", "jagapen@wisc.edu"])
msg.set_content("This is a test message. Foo, bar, baz.")

with smtplib.SMTP_SSL("localhost") as s:
    s.send_message(msg)
