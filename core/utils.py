import qrcode
import os
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives  # Updated import







def generate_qr_code(unique_id, user_id):
    # Create a folder to store QR codes (if it doesn't exist)
    qr_folder = 'qr_codes'
    if not os.path.exists(qr_folder):
        os.makedirs(qr_folder)

    # File path to save the QR code
    qr_file_path = os.path.join(qr_folder, f'{user_id}_qr_code.png')

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(str(unique_id))
    qr.make(fit=True)

    # Save the QR code to file
    img = qr.make_image(fill='black', back_color='white')
    img.save(qr_file_path)

    return qr_file_path  # Return the file path



def generate_qr_code(unique_id, user_id):
    # Create a folder to store QR codes (if it doesn't exist)
    qr_folder = 'qr_codes'
    if not os.path.exists(qr_folder):
        os.makedirs(qr_folder)

    # File path to save the QR code
    qr_file_path = os.path.join(qr_folder, f'{user_id}_qr_code.png')

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(str(unique_id))
    qr.make(fit=True)

    # Save the QR code to file
    img = qr.make_image(fill='black', back_color='white')
    img.save(qr_file_path)

    return qr_file_path  # Return the file path


def send_qr_email(user_email, user_name, user_id, unique_id):
    subject = 'Confirmation Invitation: Resilience and Renewal Conference'
    
    # URL of your background image on the server
    background_image_url = 'http://127.0.0.1:8000/static/core/images/desktop_background_image.png'

    # Generate the QR code and get the file path
    qr_file_path = generate_qr_code(unique_id, user_id)

    # HTML content of the email
    html_content = f"""
    <html>
        <head>
            <style>
                body {{
                    background-color: #e6f2f5;
                    font-family: 'Arial', sans-serif;
                    margin: 0;
                    padding: 0;
                }}
                .email-wrapper {{
                    background-image: url('{background_image_url}');
                    background-size: cover;
                    background-position: center;
                    padding: 20px;
                    width: 100%;
                    height: 100%;
                    margin: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }}
                .email-container {{
                    background-color: rgba(255, 255, 255, 0.9);
                    padding: 30px;
                    width: 600px;
                    border-radius: 15px;
                    box-shadow: 0px 0px 15px rgba(0, 0, 0, 0.1);
                    text-align: center;
                }}
                h1 {{
                    color: #006666;
                    margin-bottom: 20px;
                }}
                p {{
                    color: #333;
                    font-size: 16px;
                    line-height: 1.5;
                    margin-bottom: 20px;
                }}
                .qr-code {{
                    text-align: center;
                    margin: 20px 0;
                }}
                .footer {{
                    font-size: 12px;
                    color: #888;
                    text-align: center;
                    margin-top: 30px;
                }}
            </style>
        </head>
        <body>
            <div class="email-wrapper">
                <div class="email-container">
                    <h1>Resilience and Renewal Conference</h1>
                    <p>Dear {user_name},</p>
                    <p>
                        Thank you for registering for our upcoming event. We look forward to welcoming you to 
                        <strong>“Resilience and Renewal: Women Refugee Health in a Changing Climate Conference”</strong> on October 1, 2024 at 09:00 A.M.
                    </p>
                    <p>
                        Please arrive at the venue at your allotted registration time and make your way to the registration counter to be checked in. 
                        You will need to have the QR Code below ready for scanning.
                    </p>
                    <div class="qr-code">
                        <img src="cid:qr_code.png" alt="QR Code" />
                    </div>
                    <div class="footer">
                        <p>Thank you for being a part of this important event.</p>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """

    text_content = f"""
    Dear {user_name},

    Thank you for registering for our upcoming event. We look forward to welcoming you to “Resilience and Renewal: Women Refugee Health in a Changing Climate Conference” on October 1, 2024 at 09:00 A.M.

    Please arrive at the venue at your allotted registration time and make your way to the registration counter to be checked in. You will need to have the QR Code below ready for scanning.

    Thank you for being a part of this important event.
    """

    # Create the email
    email = EmailMultiAlternatives(
        subject,
        text_content,
        'adityathapliyal307@gmail.com',  # Replace with your email
        [user_email],
    )

    # Attach the HTML content
    email.attach_alternative(html_content, "text/html")

    # Attach the QR code image file and mark it as inline (cid:qr_code.png for embedding in HTML)
    with open(qr_file_path, 'rb') as qr_file:
        email.attach('qr_code.png', qr_file.read(), 'image/png')

    # Send the email
    email.send()

    # Remove the generated QR code file after sending the email
    os.remove(qr_file_path)
