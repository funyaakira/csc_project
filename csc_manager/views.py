from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import FormView, TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from .models import Staff, Shift, Shift_knd
import codecs


@login_required
def home(request):
    year = date.today().year
    month = date.today().month
    day = date.today().day
    return redirect('shift_day', year=year, month=month, day=day)


def shift_upload(request):

    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        filepath = settings.MEDIA_ROOT + '/' + filename
        import_shift(filepath)
        uploaded_file_url = fs.url(filename)
        return render(request, 'csc_manager/shift/upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'csc_manager/shift/upload.html')


def import_shift(filepath):

    # とりあえず当月のデータを削除
    f = codecs.open(filepath, 'r', 'utf-8')
    firstLine = f.readline()
    dateF = firstLine.split(",")[0]
    dateF = datetime.strptime(dateF, '%Y/%m/%d')
    dateT = dateF + relativedelta(months=1)
    Shift.objects.filter(date__gte=dateF, date__lt=dateT).delete()
    f.close()

    # シフトデータインポート
    f =  codecs.open(filepath, 'r', 'utf-8')
    line = f.readline()

    while line:
        date = line.split(",")[0]
        date = timezone.datetime.strptime(date, '%Y/%m/%d')
        name = line.split(",")[1].strip()
        short_name = line.split(",")[2].strip()

        print(str(date) + ' ' + name + ' ' + short_name)
        if short_name != '' and name != '':
            try:
                staff = Staff.objects.get(name=name)
                shift_knd = Shift_knd.objects.get(short_name=short_name)
            except Exception:
                print(date)
                print("エラー：" + name)
                print("エラー：" + short_name)
                return

            # 固定シフトが登録されている場合は、それを登録(休み以外)
            if shift_knd.catergory != '休':
                if staff.fixed_shift != None:
                    shift_knd = staff.fixed_shift

            Shift(date=date, shift_knd=shift_knd, staff=staff).save()

        line = f.readline()

    f.close()

    return None
