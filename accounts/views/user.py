from django.shortcuts import render, redirect
from django import forms
from django.core.exceptions import ValidationError
from django.contrib import messages
from openpyxl import load_workbook

from accounts import models
from utils.pagination import Pagination
from utils.bootstrap import BootStrapModelForm
from utils.encrypt import md5

from accounts.forms import ImportUsersForm



def user_list(request):
    """用户列表"""
    
    # info_dict = request.session['info'] 获取登录信息
    # info_dict[id]
    
    # 构造搜索
    data_dict = {}
    search_data = request.GET.get('q','')
    if search_data:
        data_dict['name__contains']= search_data 
    
    # 根据搜索条件去数据库获取
    queryset = models.User.objects.filter(**data_dict)
    
    # 分页
    page_object = Pagination(request, queryset)
    context = {
        'search_data': search_data,
        'queryset': page_object.page_queryset,     # 分页数据
        'page_string': page_object.html(),         # 生成页码
    }

    return render(request, 'user_list.html', context)


class UserModelForm(BootStrapModelForm):
    
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True),
        )
    
    class Meta:
        model = models.User
        fields = ['username', 'name', 'gender', 'phone', 'department', 'subject', 'password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd:
            raise ValidationError("两次输入的密码不一致")
        return confirm  # 返回什么。此字段就保存此数据库


def user_add(request):
    """添加用户"""
    
    title = '新建用户'
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'change.html', {'form': form, 'title': title})
    
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('accounts:user_list')
    
    return render(request, 'change.html', {'form': form, 'title': title})


class UserEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.User
        fields = ['username', 'name', 'gender', 'phone', 'department', 'subject']


def user_edit(request, nid):
    """编辑用户"""
    # 对象 / None
    title = '编辑用户'
    row_object = models.User.objects.filter(id=nid).first()
    if not row_object:
        return render(request,'error.html', {"msg":"数据不存在"})

    # 要是单独只能修改某几个字段，单独写一个form类
    if request.method == 'GET':
        form = UserEditModelForm(instance=row_object) 
        return render(request, 'change.html', {'form':form, 'title': title})
    form = UserEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('accounts:user_list')
    return render(request, 'change.html', {'form': form, 'title': title})


def user_delete(request):
    """删除用户"""
    nid = request.GET.get('nid')
    models.User.objects.filter(id=nid).delete()
    return redirect('accounts:user_list')


class UserRestModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True),
        )
    
    class Meta:
        model = models.User
        fields = ['password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }  
        
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = md5(pwd)
        
        # 去数据库校验新输入的密码和之前的密码是否是一样的
        exists = models.User.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError('密码不能与之前的相同')
        return md5(pwd)
    
    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd and pwd!=None:
            raise ValidationError("两次输入的密码不一致")
        return confirm  # 返回什么。此字段就保存此数据库


def user_reset(request, nid):
    """重置密码"""
   
    row_object = models.User.objects.filter(id=nid).first()
    if not row_object:
        return render(request,'error.html', {"msg":"数据不存在"})
    
    title = '重置密码 - {}'.format(row_object.username)
    if request.method == 'GET':
        form =  UserRestModelForm()
        return render(request, 'change.html', {'form': form, 'title': title})
    
    form =  UserRestModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('accounts:user_list')
    return render(request, 'change.html', {'form': form, 'title': title})



def import_users(request):
    if request.method == 'POST':
        form = ImportUsersForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            
            # 验证文件类型
            if not excel_file.name.endswith(('.xlsx', '.xls')):
                messages.error(request, "错误：只支持 .xlsx 或 .xls 格式文件")
                return render(request, 'import_users.html', {'form': form})
            
            try:
                wb = load_workbook(excel_file)
                ws = wb.active
                
                success_count = 0
                skip_count = 0
                skip_list = []
                error_list = []
                
                # 创建学科名称到实例的映射（提高性能）
                subjects = {subject.title: subject for subject in models.Subject.objects.all()}
                # 创建部门名称到实例的映射（提高性能）
                departments = {dept.title: dept for dept in models.Department.objects.all()}
                
                # 从第二行开始读取（假设第一行是标题）
                for row_index, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
                    # 跳过空行
                    if not any(row):
                        continue
                    
                    try:
                        username, name, subject_name, dept_name, phone = row[:5]
                        
                        # 检查用户是否存在
                        if models.User.objects.filter(username=username).exists():
                            skip_count += 1
                            skip_list.append(f"{username}（已存在）")
                            continue
                        
                        # 获取或创建学科实例
                        subject_instance = subjects.get(subject_name)
                        if not subject_instance:
                            # 如果学科不存在，设置为空值
                            subject_instance = None
                        
                        # 获取或创建部门实例
                        dept_instance = departments.get(dept_name)
                        if not dept_instance:
                            # 如果部门不存在，设置为空值
                            dept_instance = None
                    
                        
                        # 创建新用户
                        models.User.objects.create(
                            username=username,
                            password=md5('123456'),
                            name=name,
                            subject=subject_instance,
                            department=dept_instance,
                            phone=phone
                        )
                        success_count += 1
                        
                    except Exception as e:
                        error_list.append(f"第 {row_index} 行错误: {str(e)}")
                        continue
                
                # 生成结果消息
                result_msg = f"导入完成！成功: {success_count}条"
                if skip_count > 0:
                    result_msg += f", 跳过: {skip_count}条"
                if skip_list:
                    messages.warning(request, f"跳过的用户: {', '.join(skip_list[:5])}" + ("..." if len(skip_list) > 5 else ""))
                if error_list:
                    messages.error(request, f"错误行: {', '.join(error_list[:3])}" + ("..." if len(error_list) > 3 else ""))
                
                messages.success(request, result_msg)
                return render(request, 'import_result.html')  # 重定向回导入页面显示消息
            
            except Exception as e:
                messages.error(request, f"处理文件时出错: {str(e)}")
    
    else:
        form = ImportUsersForm()
    
    return render(request, 'import_result.html', {'form': form})