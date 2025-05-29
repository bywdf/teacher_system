from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from assessments.models import AssessDepart
from utils.bootstrap import BootStrapModelForm
from utils.pagination import Pagination

# Create your views here.


class AssessDepartModelForm(BootStrapModelForm):
    class Meta:
        model = AssessDepart
        fields = '__all__'


def assessdepart_list(request):
    '''考核部门列表'''
    form = AssessDepartModelForm()
    query = AssessDepart.objects.all()
    page_object = Pagination(request, query)
    context = {
        'form': form,
        'page_string': page_object.html(),
        'queryset': page_object.page_queryset,
    }
    return render(request, 'assessdepart_list.html', context)



@csrf_exempt
def  assessdepart_add(request):
    '''考核部门添加(Ajax请求)'''
    form = AssessDepartModelForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({'status': False, 'error': form.errors})


def  assessdepart_delete(request):
    '''考核部门删除'''
    uid = request.GET.get('uid')
    exists = AssessDepart.objects.filter(id=uid).exists()
    if not exists:
        return JsonResponse({'status': False, 'error': '删除失败，数据不存在'})
    AssessDepart.objects.filter(id=uid).delete()
    return JsonResponse({'status': True})


def  assessdepart_detail(request):
    '''根据ID获取考核部门详情'''
    uid = request.GET.get('uid')
    # row_dict = models.assessdepart.objects.filter(id=uid).values('title').first()
    row_dict = AssessDepart.objects.filter(id=uid).values('name').first()
    if not row_dict:
        return JsonResponse({"status":False, 'error':"数据不存在"})
    result = {
        'status': True,
        'data': row_dict,
    }
    return JsonResponse(result)
    
@csrf_exempt
def  assessdepart_edit(request):
    '''编辑考核部门'''
    uid = request.GET.get('uid')
    row_object = AssessDepart.objects.filter(id=uid).first()
    if not row_object:
        return JsonResponse({"status":False, 'error':"数据不存在,请刷新重试"})

    form = AssessDepartModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    return JsonResponse({'status': False, 'error': form.errors})