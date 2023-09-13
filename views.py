from django.shortcuts import render
from datetime import datetime

def current_time(request):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return render(request, 'timeapp/current_time.html', {'current_time': current_time})
