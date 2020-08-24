from django.shortcuts import render
from .FakeAnoah import User as AnoahUser
from users.models import UserSelf
from django.contrib.auth.decorators import login_required

def index(request):
    if request.user.is_authenticated:
        anoah_user = AnoahUser(UserSelf.objects.get(userName=request.user.username).anoahName.replace('e',''))
        result = {
            'undo_homework_num': anoah_user.get_undo_homework(1)['homework_count'],
            'name': anoah_user.user_name
        }
    else:
        result = {}
    return render(request,'index.html', result)

@login_required
def homework(request):
    anoah_user = AnoahUser(UserSelf.objects.get(userName=request.user.username).anoahName.replace('e',''))
    info = request.GET
    try:
        page = info['page']
    except:
        page = 0
    result = {
        'undo_homework': anoah_user.get_undo_homework(page),
        'pages_count': str(anoah_user.get_undo_homework_page()-1),
        'page':str(page)
    }
    return render(request,'homework.html', result)