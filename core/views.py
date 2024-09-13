from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm
from .models import User
from .utils import send_qr_email
from django.http import HttpResponse

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

            return redirect('success')
    else:
        print('invalid form')
        form = RegistrationForm()

    return render(request, 'core/register.html', {'form': form})

def success(request):
    return render(request, 'core/success.html')


#Function to verify if the user whose qr code was scanned, exists in the database
def verify_qr_code(request, user_id):
   user = get_object_or_404(User, pk=user_id, unique_id=unique_id)
   return render(request, 'verify_qr_code.html', {'user': user})
    # return render(request, 'verify_qr_code.html', {'user': user})

