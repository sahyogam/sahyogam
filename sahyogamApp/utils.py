# from django.core.mail import send_mail
# from django.conf import settings

# def send_otp_email(email, otp):
#     subject = "Your Sahyogam Registration OTP"
#     message = f"Your OTP for verification is {otp}. It is valid for 3 minutes."
#     from_email = settings.DEFAULT_FROM_EMAIL
#     send_mail(subject, message, from_email, [email])




from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_otp_email(email, otp):
    subject = "Your Sahyogam Registration OTP"
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [email]

    text_content = f"Your OTP is {otp}. It is valid for 3 minutes."  # plain text fallback

    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; text-align: center; background-color: #f9f9f9; padding: 20px;">
        <div style="max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            
            <!-- Logo -->
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/99/Example_logo.svg/200px-Example_logo.svg.png" alt="Sahyogam Logo" style="width: 100px; margin-bottom: 15px;">
            
            <h2 style="color: #4CAF50;">Sahyogam OTP Verification</h2>
            <p style="font-size: 16px;">Your One-Time Password is:</p>
            <h1 style="color: #333; letter-spacing: 3px;">{otp}</h1>
            <p style="font-size: 14px; color: #555;">Valid for <strong>3 minutes</strong>. Please do not share it with anyone.</p>

            <!-- Fun animation -->
            <img src="https://media.giphy.com/media/5GoVLqeAOo6PK/giphy.gif" alt="OTP Animation" style="width: 100%; max-width: 300px; margin-top: 15px; border-radius: 8px;">

            <p style="margin-top: 20px; font-size: 12px; color: gray;">This is an automated email from Sahyogam.</p>
        </div>
    </body>
    </html>
    """

    msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
