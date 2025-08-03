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


@login_required
def unread_inbox(request):

    unread_messages = (
        Message.unread.unread_for_user(request.user)
        .only('id', 'content', 'timestamp', 'sender')
    )
    return render(request, 'messaging/unread_inbox.html', {'messages': unread_messages})


def get_thread(message):
    thread = []
    for reply in message.replies.all().order_by('timestamp'):
        thread.append({
            'message': reply,
            'replies': get_thread(reply)
        })
    return thread
