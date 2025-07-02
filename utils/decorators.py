# utils/decorators.py
def login_exempt(view_func):
    """
    标记视图为不需要登录验证
    """
    view_func.login_exempt = True
    return view_func