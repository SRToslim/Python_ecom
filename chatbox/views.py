from django.core import serializers
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from chatbox.models import Chatting, GuestUser
from dashboard.utils import USER_TYPE_CUSTOMER
from userauth.models import User
from userauth.utils import get_client_ip


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        sender = request.user
        recipient = request.POST.get('recipient_id')
        message_text = request.POST.get('message_text')

        if message_text:
            if request.user.is_authenticated:
                message = Chatting.objects.create(sender=sender, recipient=recipient, text=message_text)
            else:
                guest_ip = get_client_ip(request)
                guest_user, created = GuestUser.objects.get_or_create(name="Guest", ip=guest_ip)
                message = Chatting.objects.create(guest_sender=guest_user.id, recipient=recipient, text=message_text)
        else:
            return HttpResponseBadRequest("Message text cannot be empty")

        guest = GuestUser.objects.get(id=guest_user.id)

        data = {
            'sender': request.user.id,
            'recipient': recipient,
            'message_id': message.id,
            'text': message.text,
            'guest_sender': guest.id
        }

        return JsonResponse(data, safe=False)


# def CustomerQuery(request):
#     if request.method == "POST":
#         message = request.POST.get("message")
#         customer_id = request.POST.get("customerId")
#
#         if request.user.is_authenticated:
#             sender = request.user
#             recipient = None
#             guest_sender = None
#             guest_recipient, created = GuestUser.objects.get_or_create(name='Guest', id=customer_id)
#         else:
#             sender = None
#             recipient = None
#             guest_sender, created = GuestUser.objects.get_or_create(name='Guest', id=customer_id)
#             guest_recipient = None
#
#         chat_message = Chatting(
#             sender=sender,
#             recipient=recipient,
#             guest_sender=guest_sender,
#             guest_recipient=guest_recipient,
#             text=message,
#         )
#         chat_message.save()
#
#         response_data = {"message": message}
#         return JsonResponse(response_data)
#     else:
#         return JsonResponse({"error": "Invalid request method"})


def ChatBox(request):
    customers = User.objects.filter(user_type=USER_TYPE_CUSTOMER).order_by('-id')
    context = {
        'customers': customers
    }
    return render(request, 'admin/chat/index.html', context)


# def searchUser(request):
#     search = request.GET.get('q', '')
#     print('Received search query:', search)
#
#     customer = User.objects.filter(user_type=USER_TYPE_CUSTOMER, username__icontains=search)
#
#     results = [{'id': user.id, 'username': user.username, 'full_name': user.profile.full_name} for user in customer]
#
#     return JsonResponse({'results': search_results})


def searchUser(request, search):
    customer = User.objects.filter(user_type=USER_TYPE_CUSTOMER, username__icontains=search)

    print('Received search query:', customer)

    data = serializers.serialize('json', customer)

    return JsonResponse({'results': data}, safe=False)
    # html = f'<div class ="friend-drawer friend-drawer--onhover" data-userId="{ customer.id }" >'
    # html += f'<img class="profile-image" src="{customer.profile.image.url}" alt="">'
    # html += '<div class ="text" >'
    # html += f'<h6> {customer.profile.full_name} <br />'
    # html += f'<span class ="time text-muted small" > {customer.username} </span> </h6>'
    # html += f'<p class ="text-muted"> Hey, you\'re arrested!</p>'
    # html += f'</div>'
    # html += f'<span class ="time text-muted small"> 13:21</span>'
    # html += f'</div>'
    # html += f'<hr>'
    # return html
