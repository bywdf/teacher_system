'''
自定义的分页组件,以后如果想要使用这个分页组件，你需要做如下几件事：

# 导入
from utils.pagination import Pagination

# 在视图函数中
def pretty_list(request):

    # 1.根据自己的实际情况去筛选自己的数据
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by('-level')

    # 2.实例化分页对象
    page_object = Pagination(request, queryset)

    context = {
        'queryset': page_object.page_queryset,     # 分页数据
        'page_string': page_object.html()         # 生成页码
    }
    
    return render(request, 'pretty_list.html', context)

# 在HTML页面中for循环的table标签后面添加ul：

    {% for obj in queryset %}
        {{obj.xx}}
    {% endfor %}
      
    <ul class="pagination" style="float:left;">   
      {{ page_string }}
    </ul>

'''

from django.utils.safestring import mark_safe
# from django.http.request import QueryDict
import copy

class Pagination(object):
    
    def __init__(self, request, queryset, page_size = 20, page_param='page', plus = 5):
        '''
        request: 请求的对象
        queryset: 符合条件的数据（根据这个数据给他进行分页处理）
        page_size: 每页显示多少条数据
        page_param: 在URL中传递的获取分页的参数, 例如：/pretty/list/?page=12
        plus: 显现当前页的 前或后几页（根据页码来）
        '''
        
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        
        self.query_dict = query_dict
        
        self.page_param = page_param

        page = request.GET.get(page_param, '1')
        
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page = page 
        self.page_size = page_size     # 每页显示数据
        
        # 根据用户想要访问的页码，计算出起止位置
        self.start = (page -1) * page_size
        self.end = page * page_size
        
        self.page_queryset = queryset[self.start:self.end]
          
         # 数据总条数
        total_count = queryset.count()
        # select * from 表 order by id desc/asc     -id/id
        
        # math.ceil() 向上取整更好, 总页码
        total_page_count, div = divmod(total_count, page_size)
        if div:
             total_page_count += 1
        self.total_page_count =  total_page_count
        
        self.plus = plus
        
        
    def html(self):
               
        # 计算出，显示当前页的前5页，后5页
        if self.total_page_count <= 2 * self.plus + 1:
            # 数据库中数据比较少，都没有达到11页
            start_page = 1
            end_page = self.total_page_count
        else:
            # 数据库中的数据比较多 > 11 页
            
            # 当页前小于5(处理小的极值)
            if self.page <= self.plus:
                start_page = 1
                end_page = 2*self.plus
            else:
                # 当前页 > 5
                # 当前页+5 > 总页面
                if (self.page + self.plus) > self.total_page_count:
                    start_page = self.total_page_count - 2*self.plus
                    end_page = self.total_page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus
        # 用elif改更美观
            
        # 页码
        page_str_list = []
        
        self.query_dict.setlist(self.page_param, [1])   
        
        #首页
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))
        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page-1]) 
            prev =  '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev =  '<li><a href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(prev)
        
        # 页面
        for i in range(start_page, end_page + 1):
            if i == self.page:
                self.query_dict.setlist(self.page_param, [i])
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                self.query_dict.setlist(self.page_param, [i])
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)
        
        # 下一页  
        if self.page < self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.page+1])
            next =  '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            next =  '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_str_list.append(next)
        
        #  尾页
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))    
        
        search_string = '''
            <li> 
            <form style='float: left; margin-left: -1px;' method='get'>
                    <input name='page'
                        style='position: relative; float:left; display: inline-block; width: 80px; border-radius: 0;'
                        type="text" class='form-control' placeholder='页码'>
                    <button style='border-radius: 0;' type="submit" class='btn btn-default'>跳转</button>
            </form>
            </li>
        '''
        
        page_str_list.append(search_string)
        
        page_string = mark_safe("".join(page_str_list)) 
        return page_string