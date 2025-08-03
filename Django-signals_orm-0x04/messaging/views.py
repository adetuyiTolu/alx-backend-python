from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User


@login_required
def delete_user(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('home')  # Redirect to homepage after deletion
