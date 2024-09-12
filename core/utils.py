import qrcode
import os
import requests
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.templatetags.static import static
import requests


# Function to generate QR code and save as image
def generate_qr_code(unique_id, user_id):
    qr_folder = 'qr_codes'
    if not os.path.exists(qr_folder):
        os.makedirs(qr_folder)

    qr_file_path = os.path.join(qr_folder, f'{user_id}_qr_code.png')

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(str(unique_id))
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(qr_file_path)

    return qr_file_path  # Return the file path

# Function to send the email with HTML content and embedded images using CID
def send_qr_email(user_email, user_name, user_id, unique_id):
    subject = 'Confirmation Invitation: Resilience and Renewal Conference'

    # Generate the QR code and get the file path
    qr_file_path = generate_qr_code(unique_id, user_id)

    # HTML content for the email
    html_content = f"""
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Event Invitation</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            
            height: 100vh; /* Ensures full background height */
        }}
        table {{
            width: 100%;
            max-width: 600px;
            margin: 50px auto; /* Margin from top to create space */
            background-color: #ffffff;
            border-radius: 8px; /* Smooth corners */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Light shadow for depth */
        }}
        .header {{
            text-align: center;
            padding: 20px 0;
        }}
        .header img {{
            width: 100%;
            height: auto;
            max-width: 600px;
        }}
        .content {{
            padding: 30px;
            background-color: #ffffff;
        }}
        .content p {{
            color: #333;
            font-size: 16px;
            line-height: 1.75;
            text-align: left; /* Align left for formal feel */
            margin-bottom: 20px; /* Space between paragraphs */
        }}
        .qr-code {{
            text-align: center;
            margin: 30px 0;
        }}
        .qr-code img {{
            width: 150px;
        }}
        .footer {{
            text-align: center;
            font-size: 12px;
            color: #888;
            padding: 20px 0;
            background-color: #e0f7fa; /* Cyan background for the footer */
        }}
    </style>
</head>
<body>
    <table cellpadding="10" cellspacing="0" width="100%" style="font-family: Arial, sans-serif; border-collapse: collapse;">
        <!-- Header Section -->
        <tr>
            <td style="text-align: center; padding: 20px;">
                <img src="cid:header_image" alt="Event Header" style="max-width: 100%; height: auto;">
                 <img src="cid:header_image2" alt="Event Header2" style="max-width: 100%; height: auto;">
            </td>
        </tr>
       
        
        <!-- Content Section -->
        <tr>
            <td style="padding: 20px; background-color: #f9f9f9;">
                <p>Dear <strong>{user_name}</strong>,</p>
                <p>Thank you for registering for our upcoming event. We are excited to welcome you to the <strong>“Resilience and Renewal: Women Refugee Health in a Changing Climate Conference”</strong> on <strong>October 1, 2024</strong>.</p>
                
                <!-- Event Date and Time Table -->
                <table cellpadding="10" cellspacing="0" style="margin-top: 20px; border: 1px solid #ddd; border-radius: 5px; background-color: #ffffff;">
                    <tr>
                        <td style="font-weight: bold; border-bottom: 1px solid #ddd;">Date:</td>
                        <td style="font-weight: bold; border-bottom: 1px solid #ddd;">October 1, 2024</td>
                    </tr>
                    <tr>
                        <td style="font-weight: bold; border-bottom: 1px solid #ddd;">Time:</td>
                        <td style="font-weight: bold; border-bottom: 1px solid #ddd;">9:00 AM</td>
                    </tr>
                </table>

                <p>Please arrive at the venue at your allotted registration time and proceed to the registration counter for check-in.<strong>Kindly ensure that the QR code below is ready for scanning at the event entrance.</strong></p>

                <div style="text-align: center; margin: 20px 0;">
                    <img src="cid:qr_code" alt="QR Code" style="max-width: 200px; height: auto;">
                </div>

                <p>We appreciate your participation in this significant event, and we look forward to your presence!</p>
            </td>
        </tr>

        <!-- Footer Section -->
        <tr>
            <td style="text-align: center; padding: 10px; background-color: #333; color: #fff;">
                <p>&copy; 2024 Resilience and Renewal Conference. All rights reserved.</p>
            </td>
        </tr>
    </table>
</body>

</html>
"""



    text_content = f"""
    Dear {user_name},

    Thank you for registering for our upcoming event. We look forward to welcoming you to “Resilience and Renewal: Women Refugee Health in a Changing Climate Conference” on October 1, 2024, at 09:00 A.M.

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

    # Attach the QR code image as MIMEImage and set the Content-ID
    with open(qr_file_path, 'rb') as qr_file:
        qr_image = MIMEImage(qr_file.read())
        qr_image.add_header('Content-ID', '<qr_code>')
        email.attach(qr_image)

    # image_url = 'https://registration-abmr.onrender.com/static/core/images/email_header1.jpg'
    # response = requests.get(image_url)
    # img_data = response.content
    # header_image = MIMEImage(img_data, _subtype = 'jpeg')

    
    # header_image.add_header('Content-ID', '<header_image>')
    # email.attach(header_image)


    # image_url2 = 'https://registration-abmr.onrender.com/static/core/images/email_header2.jpg'
    # response2 = requests.get(image_url2)
    # img_data2 = response.content
    # header_image2 = MIMEImage(img_data2, _subtype = 'jpeg')

    
    # header_image2.add_header('Content-ID', '<header_image2>')
    # email.attach(header_image2)

    # Send the email
    email.send()

    # Clean up the generated QR code file
    os.remove(qr_file_path)

# Example usage:
# send_qr_email('test@example.com', 'John Doe', 'user123', 'unique123')
