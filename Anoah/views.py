from django.shortcuts import render
from .FakeAnoah import User as AnoahUser

def index(request):
    anoah_user = AnoahUser('1765840')
    result = {
        'name': anoah_user.user_name,
        'undo_homework': anoah_user.get_undo_homework(),
    }
    return render(request,'index.html', result)

def homework(request):
    info = request.GET
    result = {
        'title': info['title'],
        'end_time': info['end'],
        'start_time': info['start'],
        'teacher': info['teacher'],
        'class_name': info['class'],
        'subject': info['subject']
    }
    return render(request,'homework.html', result)