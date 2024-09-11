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

    # Generate the QR code and get the file path
    qr_file_path = generate_qr_code(unique_id, user_id)

    # HTML content of the email
    html_content = f"""
    <html>
        <body style="margin:0; padding:0; background-color:#e6f2f5; font-family:Arial, sans-serif; text-align:center;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="padding: 20px; background-color: #e6f2f5;">
                <tr>
                    <td>
                        <table align="center" cellpadding="0" cellspacing="0" style="max-width:600px; background-color:#ffffff; border-radius:10px; padding:20px; box-shadow:0 0 10px rgba(0,0,0,0.1);">
                            <tr>
                                <td align="center">
                                    <h1 style="color:#006666; margin-bottom:20px;">Resilience and Renewal Conference</h1>
                                    <p style="color:#333; font-size:16px; line-height:1.5; margin-bottom:20px;">
                                        Dear {user_name},
                                    </p>
                                    <p style="color:#333; font-size:16px; line-height:1.5; margin-bottom:20px;">
                                        Thank you for registering for our upcoming event. We look forward to welcoming you to 
                                        <strong>“Resilience and Renewal: Women Refugee Health in a Changing Climate Conference”</strong> on October 1, 2024 at 09:00 A.M.
                                    </p>
                                    <p style="color:#333; font-size:16px; line-height:1.5; margin-bottom:20px;">
                                        Please arrive at the venue at your allotted registration time and make your way to the registration counter to be checked in. 
                                        You will need to have the QR Code below ready for scanning.
                                    </p>
                                    <div style="margin: 20px 0;">
                                        <img src="cid:qr_code" alt="QR Code" style="max-width:150px;"/>
                                    </div>
                                    <p style="font-size:14px; color:#888; margin-top:20px;">
                                        Thank you for being a part of this important event.
                                    </p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
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
        'your-email@example.com',  # Replace with your email
        [user_email],
    )

    # Attach the HTML content
    email.attach_alternative(html_content, "text/html")

    # Attach the QR code image file and mark it as inline
    with open(qr_file_path, 'rb') as qr_file:
        email.attach('qr_code.png', qr_file.read(), 'image/png')
        email.attachments[-1]['Content-ID'] = '<qr_code>'  # Set the content ID for embedding

    # Send the email
    email.send()

    # Remove the generated QR code file after sending the email
    os.remove(qr_file_path)

