from functools import wraps
from flask import g,redirect,url_for
def login_required(func):
    @wraps(func)#wraps 是一个装饰器，它用于从原始函数中复制函数的名称和文档字符串，以及其他相关的属性。这在使用装饰器时非常有用，因为装饰器会改变原始函数的一些特征。如果没有使用 functools.wraps，那么在装饰后的函数中将不再能够访问原始函数的名称和文档字符串1。简而言之，wraps 保留了被装饰函数的元信息，使其在装饰后的函数中仍然可用。如果你在自定义装饰器中使用了 @wraps，那么被装饰的函数将保留其原始函数的属性，
    def inner(*args, **kwargs):
        if g.user:#判断是否登录
            return func(*args, **kwargs)
        else:
            return redirect(url_for("auth.login"))
    return inner