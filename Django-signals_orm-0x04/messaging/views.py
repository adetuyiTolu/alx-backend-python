from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import Message


@login_required
def delete_user(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')  # Redirect to homepage after deletion


@login_required
def inbox(request):

    messages = Message.objects.filter(
        sender=request.user) | Message.objects.filter(receiver=request.user)
    messages = messages.select_related(
        'sender', 'receiver').order_by('-timestamp')

    threads = []
    for msg in messages:
        threads.append({
            'message': msg,
            'replies': get_thread(msg)
        })

    return render(request, 'messaging/inbox.html', {'threads': threads})


def get_thread(message):
    thread = []
    for reply in message.replies.all().order_by('timestamp'):
        thread.append({
            'message': reply,
            'replies': get_thread(reply)
        })
    return thread
