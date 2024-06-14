# qrcodes/views.py
from django.shortcuts import render, redirect
from .models import QRCode
import qrcode
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import string
import random

def generate_edit_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

def generate_security_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

def create_qr(request):
    if request.method == 'POST':
        edit_code = generate_edit_code()
        security_code = generate_security_code()
        unique_url = f"http://127.0.0.1:8000/qrcodes/update/{edit_code}/"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(unique_url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        # Salva il codice QR nel database
        qr_code = QRCode.objects.create(url=unique_url, edit_code=edit_code, security_code=security_code)
        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")
        return response
    return render(request, 'qrcodes/create_qr.html')

def update_qr(request, edit_code):
    try:
        qr_code = QRCode.objects.get(edit_code=edit_code)
    except QRCode.DoesNotExist:
        return HttpResponse("Codice di modifica non valido")
    
    if request.method == 'POST':
        if 'content' in request.FILES:
            new_content = request.FILES['content']
            if new_content.size > 5 * 1024 * 1024:  # 5 MB
                return HttpResponse("Il file caricato è troppo grande. Massimo 5 MB.")
            
            file_name = default_storage.save(new_content.name, ContentFile(new_content.read()))
            file_url = default_storage.url(file_name)
            qr_code.file_url = file_url
            qr_code.save()
            return redirect('success_page', edit_code=edit_code)
        else:
            return HttpResponse("Nessun file caricato.")
    
    if qr_code.file_url:
        return redirect('view_content', edit_code=edit_code)

    return render(request, 'qrcodes/update_qr.html', {'qr_code': qr_code})

def success_page(request, edit_code):
    qr_code = QRCode.objects.get(edit_code=edit_code)
    return render(request, 'qrcodes/success.html', {'qr_code': qr_code})

def view_content(request, edit_code):
    try:
        qr_code = QRCode.objects.get(edit_code=edit_code)
    except QRCode.DoesNotExist:
        return HttpResponse("Codice non valido")
    
    return render(request, 'qrcodes/view_content.html', {'qr_code': qr_code})

def instructions_page(request, edit_code):
    try:
        qr_code = QRCode.objects.get(edit_code=edit_code)
    except QRCode.DoesNotExist:
        return HttpResponse("Codice non valido")
    
    return render(request, 'qrcodes/instructions.html', {'qr_code': qr_code})
