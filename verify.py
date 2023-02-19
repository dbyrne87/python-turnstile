import requests

def cloudflarecheck(request, bot): ##(bot is the cf-turnstile-response passed from the frontend)
    url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
    data = {'secret': '3x0000000000000000000000000000000AA', 'response': bot, 'remoteip': request.META.get("REMOTE_ADDR")}
    resp = requests.post(url, data=data)
    json_list = resp.json()
    success = list(json_list.values())[0]  
    print(success)   
    if success != True:
        return False    
    return True
  

  
from .forms import ContactForm
from django.views.decorators.http import require_POST
###sample function to use above cloudflarecheck function  
@require_POST
def formfootermail(request):        
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            bot = contact_form.cleaned_data['bottoken'] ##(cf-turnstile-response value)
            if cloudflarecheck(request, bot) == True: 
              name = contact_form.cleaned_data['name']
                email = contact_form.cleaned_data['email']
                phone = contact_form.cleaned_data['phone']
                content = contact_form.cleaned_data['message']
                html = render_to_string('email.html', {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'content': content
                    })

                from_email = <FROM_EMAIL>
                subject = "CONTACT FORM"
                try:
                    send_mail(subject, html, from_email, ["<TO_EMAIL>",], )
                    success = 'Thank You! Your message has been sent successfully'
                    return JsonResponse(success, status=200, safe=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.') 
            else:            
                return JsonResponse('Looks like you are a robot...', status=400, safe=False)         
        else:
            return JsonResponse(contact_form.errors, status=400, safe=False) 
