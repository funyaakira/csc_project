from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

from ..models import Riyosya
# シフト個人カレンダー表示
@method_decorator(login_required, name='dispatch')
class PrintMainView(TemplateView):
    template_name = 'csc_manager/print/main.html'


# 排泄チェック表出力
def print_haisetu_check(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment;filename="createdfile.pdf"'

    font_name = 'HeiseiKakuGo-W5'
    pdfmetrics.registerFont(UnicodeCIDFont(font_name))

    p = canvas.Canvas(response, pagesize=landscape(A3), bottomup=False)
    p.setFont(font_name, 9)
    
    height, width = A3

    row_height = height/20

    riyosyas = Riyosya.objects.filter(
        status=settings._RIYOSYA_STATUS_NYUSYO).order_by('furigana')

    row_point = row_height
    for r in riyosyas:
        p.drawString(100, row_point, r.name)
        row_point += row_height

    p.showPage()
    p.save()

    return response
