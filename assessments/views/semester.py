from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from assessments import models
from utils.bootstrap import BootStrapModelForm
from utils.pagination import Pagination
from utils.user_decorator import superuser_required, admin_or_superuser_required

# Create your views here.
class SemesterModelForm(BootStrapModelForm):
    class Meta:
        model = models.Semester
        fields = '__all__'


@admin_or_superuser_required
def semester_list(request):
    '''学年列表'''
    form = SemesterModelForm()
    queryset = models.Semester.objects.all()
    page_object = Pagination(request, queryset)
    context = {
        'form': form,
        'page_string': page_object.html(),
        'queryset': page_object.page_queryset,
    }
    return render(request, 'semester_list.html', context)


@superuser_required
@csrf_exempt
def  semester_add(request):
    '''学年添加(Ajax请求)'''
    form = SemesterModelForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({'status': False, 'error': form.errors})


@superuser_required
def  semester_delete(request):
    '''学年删除'''
    uid = request.GET.get('uid')
    exists = models.Semester.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({'status': False, 'error': '删除失败，数据不存在'})
    models.Semester.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})


def  semester_detail(request):
    '''根据ID获取学年详情'''
    uid = request.GET.get('uid')
    # row_dict = models.Semester.objects.filter(id=uid).values('title').first()
    row_dict = models.Semester.objects.filter(id=uid).values('year').first()
    if not row_dict:
        return JsonResponse({"status":False, 'error':"数据不存在"})
    result = {
        'status': True,
        'data': row_dict,
    }
    return JsonResponse(result)
    
@csrf_exempt
@superuser_required
def  semester_edit(request):
    '''编辑学年'''
    uid = request.GET.get('uid')
    row_object = models.Semester.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status":False, 'error':"数据不存在,请刷新重试"})

    form = SemesterModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({'status': False, 'error': form.errors})