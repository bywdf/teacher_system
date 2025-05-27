from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from assessments import models
from utils.bootstrap import BootStrapModelForm
from utils.pagination import Pagination

# Create your views here.
def testbase(request):
    return render(request, 'base.html')


class TermYearModelForm(BootStrapModelForm):
    class Meta:
        model = models.TermYear
        fields = '__all__'

def termyear_list(request):
    '''学年列表'''
    form = TermYearModelForm()
    queryset = models.TermYear.objects.all()
    page_object = Pagination(request, queryset)
    context = {
        'form': form,
        'page_string': page_object.html(),
        'queryset': page_object.page_queryset,
    }
    return render(request, 'termyear_list.html', context)

@csrf_exempt
def  termyear_add(request):
    '''学年添加(Ajax请求)'''
    form = TermYearModelForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({'status': False, 'error': form.errors})


def  termyear_delete(request):
    '''学年删除'''
    uid = request.GET.get('uid')
    exists = models.TermYear.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({'status': False, 'error': '删除失败，数据不存在'})
    models.TermYear.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})


def  termyear_detail(request):
    '''根据ID获取学年详情'''
    uid = request.GET.get('uid')
    # row_dict = models.TermYear.objects.filter(id=uid).values('title').first()
    row_dict = models.TermYear.objects.filter(id=uid).values('name').first()
    if not row_dict:
        return JsonResponse({"status":False, 'error':"数据不存在"})
    result = {
        'status': True,
        'data': row_dict,
    }
    return JsonResponse(result)
    
@csrf_exempt
def  termyear_edit(request):
    '''编辑学年'''
    uid = request.GET.get('uid')
    row_object = models.TermYear.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status":False, 'error':"数据不存在,请刷新重试"})

    form = TermYearModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({'status': False, 'error': form.errors})