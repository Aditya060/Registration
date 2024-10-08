import json
import os
from io import BytesIO
import qrcode
from .models import ScannedQRCode
from django.views.decorators.csrf import csrf_exempt


from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.staticfiles import finders  # Add this import

from .forms import RegistrationForm
from .models import User
from .utils import send_qr_email

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfReader, PdfWriter

import arabic_reshaper
from bidi.algorithm import get_display
import qrcode  # Only if generating QR codes locally
from PIL import Image  # Ensure all necessary components are imported


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print('form has not been saved yet')    
            # Save the user to the database
            user = form.save()

           
            # local_background_image_path = "/Users/adityathapliyal/Desktop/Registration-Final/Registration/core/static/core/images/new_back.png"
            # online_background_image_url = "https://registration-abmr.onrender.com/static/core/images/desktop_background_image.png"
            
            print('form has been saved')
            
            # Send the QR code via email to the user's email address
            send_qr_email(user.email, user.name, user.id, user.unique_id)

            print('email has been sent')

            return redirect('success', unique_id=user.unique_id)
    else:
        print('invalid form')
        form = RegistrationForm()

    return render(request, 'core/register.html', {'form': form})

def success(request, unique_id):
    # Now the unique_id is passed as a parameter in the URL
    return render(request, 'core/success.html', {'unique_id': unique_id})

#Function to verify if the user whose qr code was scanned, exists in the database
# def verify_qr_code(request, unique_id):
#     try:
#         user = User.objects.get(unique_id=unique_id)
#         return render(request, 'core/verify_qr_code.html', {'user': user})
#     except User.DoesNotExist:
#         # Custom user not found message
#         return render(request, 'core/verify_qr_code.html', {'user': None, 'error_message': 'User not found. Please check your registration details.'})


# def verify_qr_code(request, unique_id):
#     try:
#         user = get_object_or_404(User, unique_id=unique_id)
#         return JsonResponse({'status': 'success', 'message': 'User found', 'user_id': user.id})
#     except User.DoesNotExist:
#         return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)
# View for the QR code scanner page
# @login_required
def qr_scanner_view(request):
    return render(request, 'core/scanner.html')

#Function to verify if the user whose qr code was scanned, exists in the database

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def verify_qr_code(request):
    if request.method == 'POST':
        try:
            # Load the request data
            data = json.loads(request.body)
            qr_code = data.get('qr_code')

            print(f"QR Code received: {qr_code}")

            # Check if the user exists
            # qr_code = qr_code[46:-1]

            user = get_object_or_404(User, unique_id=qr_code)
            print(f"User found: {user.name}")

            # If the user is found, return success response
            return JsonResponse({'exists': True, 'name': user.name})

        except User.DoesNotExist:
            print("User not found for the given QR code.")
            return JsonResponse({'exists': False}, status=404)
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    

# def print_badge(request, qr_code):
#     # Fetch the user associated with the qr_code
#         user = get_object_or_404(User, unique_id=qr_code)
        
#         context = {
#             'user': user,
#             'qr_code': qr_code,
#         }
#         return render(request, 'core/print_badge.html', context)
    

# def print_badge(request, unique_id):
#     # Generate the path to the badge template
#     badge_template_path = finders.find('core/images/badge_template.pdf')
    
#     # Load user information based on unique_id
#     user = get_object_or_404(User, unique_id=unique_id)
    
#     # Prepare the response as PDF
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'inline; filename=badge_{user.name}.pdf'

#     # Create a new PDF in memory
#     buffer = BytesIO()

#     # Use PdfReader to read the template
#     template_pdf = PdfReader(open(badge_template_path, "rb"))
#     writer = PdfWriter()

#     # Create a ReportLab canvas to overlay the QR code and user information
#     packet = BytesIO()
#     c = canvas.Canvas(packet, pagesize=letter)

#     # Add QR code (you can generate the QR code as an image and draw it on the canvas)
#     qr_code_url = f'https://tap4.link/verify/{unique_id}/'
#     qr_code_image = ImageReader(f'https://api.qrserver.com/v1/create-qr-code/?data={qr_code_url}&size=150x150')
#     # Add QR code (move right and down)
#     # Set QR code position
#     qr_code_x = 220  # Adjust this value to move it more to the right
#     qr_code_y = 200  # Adjust this value to move it down
#     c.drawImage(qr_code_image, x=qr_code_x, y=qr_code_y, width=150, height=150)

#     # Add user name centered above the QR code
#     name_font_size = 30  # Adjust size to be 3x current size
#     company_font_size = 20  # Adjust size to be 2x current size

#     # Set font for the name (bold)
#     c.setFont("Helvetica-Bold", name_font_size)
#     name_text = user.name
#     name_text_width = c.stringWidth(name_text, "Helvetica-Bold", name_font_size)
#     name_x = qr_code_x + (150 - name_text_width) / 2  # Center the name above the QR code
#     name_y = qr_code_y + 200  # Position directly above the QR code
#     c.drawString(name_x, name_y, name_text)

#     # Set font for the company (bold)
#     c.setFont("Helvetica-Bold", company_font_size)
#     company_text = user.company
#     company_text_width = c.stringWidth(company_text, "Helvetica-Bold", company_font_size)
#     company_x = qr_code_x + (150 - company_text_width) / 2  # Center the company above the QR code
#     company_y = name_y - 30  # Position just above the name
#     c.drawString(company_x, company_y, company_text)



#     # Finalize the overlay
#     c.save()

#     # Move to the beginning of the StringIO buffer
#     packet.seek(0)

#     # Add the overlay to the first page of the template
#     overlay_pdf = PdfReader(packet)
#     page = template_pdf.pages[0]
#     page.merge_page(overlay_pdf.pages[0])

#     # Add the page to the writer
#     writer.add_page(page)

#     # Write the final output to the response
#     writer.write(response)
#     return response

    
def print_badge(request, unique_id):
    # Generate the path to the badge template
    badge_template_path = finders.find('core/images/badge_template.pdf')
    

    # Load user information based on unique_id
    user = get_object_or_404(User, unique_id=unique_id)

    # Prepare the response as PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=badge_{user.name}.pdf'

    # Create a new PDF in memory
    buffer = BytesIO()

    # Use PdfReader to read the template
    template_pdf = PdfReader(open(badge_template_path, "rb"))
    writer = PdfWriter()

    # Create a ReportLab canvas to overlay the QR code and user information
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)

    # Register and use an Arabic-compatible font (e.g., 'Amiri')
    arabic_font_path = finders.find('core/images/Amiri-Regular.ttf')
    pdfmetrics.registerFont(TTFont('Amiri', arabic_font_path))

    # Add QR code (you can generate the QR code as an image and draw it on the canvas)
    qr_code_url = f'https://tap4.link/verify/{unique_id}/'
    
    
    # # Create the QR code with specific data
    # qr = qrcode.QRCode(
    #     version=1,
    #     error_correction=qrcode.constants.ERROR_CORRECT_L,
    #     box_size=10,
    #     border=4,
    # )
    
    # # Add the data to the QR code
    # qr.add_data(qr_code_url)  # qr_code_url is the data for the QR code
    # qr.make(fit=True)
    
    # # Create the image of the QR code
    # img = qr.make_image(fill='black', back_color='white')
    
    # # Save the image locally (optional, if you want to keep a copy)
    # # qr_file_path = 'qr_code.png'
    # # img.save(qr_file_path)
    
    # # Convert to ImageReader object for further use in reports
    # qr_code_image = ImageReader(img)

    qr_code_image = ImageReader(f'https://api.qrserver.com/v1/create-qr-code/?data={qr_code_url}&size=150x150')

    # Set QR code position
    qr_code_x = 220  # Adjust this value to move it more to the right
    qr_code_y = 200  # Adjust this value to move it down
    c.drawImage(qr_code_image, x=qr_code_x, y=qr_code_y, width=150, height=150)

    # Add user name centered above the QR code
    name_font_size = 38  # Adjust size to be 3x current size
    company_font_size = 25  # Adjust size to be 2x current size

    # Arabic reshaping and bidirectional text handling
    reshaped_name = arabic_reshaper.reshape(user.name)  # Reshape for proper Arabic display
    bidi_name = get_display(reshaped_name)  # Apply bidirectional algorithm to render properly

    reshaped_company = arabic_reshaper.reshape(user.company)
    bidi_company = get_display(reshaped_company)

    # Set font for the name (bold)
    c.setFont("Amiri", name_font_size)
    name_text_width = c.stringWidth(bidi_name, "Amiri", name_font_size)
    name_x = qr_code_x + (150 - name_text_width) / 2  # Center the name above the QR code
    name_y = qr_code_y + 200  # Position directly above the QR code
    c.drawString(name_x, name_y, bidi_name)

    # Set font for the company (bold)
    c.setFont("Amiri", company_font_size)
    company_text_width = c.stringWidth(bidi_company, "Amiri", company_font_size)
    company_x = qr_code_x + (150 - company_text_width) / 2  # Center the company above the QR code
    company_y = name_y - 30  # Position just above the name
    c.drawString(company_x, company_y, bidi_company)

    # Finalize the overlay
    c.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)

    # Add the overlay to the first page of the template
    overlay_pdf = PdfReader(packet)
    page = template_pdf.pages[0]
    page.merge_page(overlay_pdf.pages[0])

    # Add the page to the writer
    writer.add_page(page)

    # Write the final output to the response
    writer.write(response)
    return response


@csrf_exempt
def scan_qr_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            uid = data.get('qr_code')

            # Debug: Print the received UID
            print(f"Received UID from QR code: {uid}")

            # Validate UID
            if not uid:
                return JsonResponse({'exists': False, 'message': 'Invalid QR code data received'}, status=400)

            # Check if UID already exists in the ScannedQRCode database
            if ScannedQRCode.objects.filter(uid=uid).exists():
                # Find the user with this UID in the User table (using unique_id field)
                user = User.objects.filter(unique_id=uid).first()

                # Debug: Print the user object if found
                print(f"User found: {user}")

                # If user is found, add the name to the response
                if user:
                    return JsonResponse({'exists': True, 'message': f'Found - {user.name}'})
                else:
                    return JsonResponse({'exists': True, 'message': 'UID exists but user not found'})
            else:
                # UID does not exist, so create a new entry with status = 1
                ScannedQRCode.objects.create(uid=uid, status=1)
                # Attempt to find the user after inserting UID
                user = User.objects.filter(unique_id=uid).first()
                return JsonResponse({'exists': False, 'message': f'Found {user.name if user else "no user found"}'})
        except Exception as e:
            # Log the error and return a proper error message
            print(f"Error occurred: {str(e)}")
            return JsonResponse({'error': 'An error occurred while saving to the database'}, status=500)

    # Handle GET request to render the template
    return render(request, 'core/scanner.html')
