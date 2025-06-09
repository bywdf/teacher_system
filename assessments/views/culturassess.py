from django.shortcuts import render, redirect
from assessments.models import TeacherMidAssess, TeacherFinalAssess, TeacherSemesterAssess

from utils.pagination import Pagination
from utils.bootstrap import BootStrapModelForm

from django.contrib.auth.models import User


class MidAssessModelForm(BootStrapModelForm):
    class Meta:
        model = TeacherMidAssess
        # 排除字段
        fields = '__all__'
        exclude = ['total_workload', 'workload_score', 'total_score']


def cultura_mid_list(request):
    queryset = TeacherMidAssess.objects.all().order_by('id')
    page_object = Pagination(request, queryset)
    content = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
    }
    return render(request, 'cultura_mid_list.html', content)


def cultura_mid_delete(request):
    pass


def cultura_mid_edit(request):
    pass


def cultura_mid_add(request):
    pass
