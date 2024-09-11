from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import User
from django.http import HttpResponse


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print('form has not been saved yet')    
            # Save the user to the database
            user = form.save()

            # Generate the QR code for the user's unique_id
            
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

