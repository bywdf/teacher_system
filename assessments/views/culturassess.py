from django.shortcuts import render, redirect
from assessments.models import TeacherMidAssess, TeacherFinalAssess, TeacherSemesterAssess

from utils.pagination import Pagination
from utils.bootstrap import BootStrapModelForm


class MidAssessModelForm(BootStrapModelForm):
    class Meta:
        model = TeacherMidAssess
        fields = ['semester', 'assessdepart', 'teacher', 'assessdepart_score', 'assessdepart_comment', 'cultura_score', 'cultura_comment', 'total_score', 'total_comment', 'is_delete']
        
def cultura_mid_list(request):
    queryset = TeacherMidAssess.objects.all().order_by('id')
    page_object = Pagination(request, queryset) #
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
    form = 