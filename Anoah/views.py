from django.shortcuts import render
from .FakeAnoah import User as AnoahUser
anoah_user = AnoahUser('1765840')
def index(request):
    result = {
        'undo_homework_num': anoah_user.get_undo_homework(1)['homework_count'],
        'name': anoah_user.user_name,
    }
    return render(request,'index.html', result)

def homework(request):
    info = request.GET
    try:
        page = info['page']
    except:
        page = 0
    print(page, type(page))
    result = {
        'undo_homework': anoah_user.get_undo_homework(page),
        'pages_count': str(anoah_user.get_undo_homework_page()-1),
        'page':str(page)
    }
    return render(request,'homework.html', result)