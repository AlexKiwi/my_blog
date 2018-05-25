# coding=utf-8
from __future__ import unicode_literals

UNDIFINED_ERROR = 11000
SYSTEM_ERROR = 11001
ERROR_CHECK_PARAM = 10001
ERROR_DB_OP = 10002
ERROR_TIME_OUT = 10003
ERROR_CHECK_SIGN = 10004
ERROR_CHECK_LOGIN = 10005
ERROR_SIGNATURE_EXPIRED = 10006
ERROR_LOGIN_UNDIFINED = 10007
ERROR_FIND_MODULE = 10008
ERROR_FORBIT = 10009
ERROR_METHOD_FORBIT =10010


class ZhError(object):
    UNDIFINED_ERROR = '未定义的错误'
    SYSTEM_ERROR = '系统错误'
    ERROR_CHECK_PARAM = '验证参数失败'
    ERROR_DB_OP = '服务器开了会小差'
    ERROR_TIME_OUT = '请求时间过长'
    ERROR_CHECK_SIGN = '验证签名失败'
    ERROR_CHECK_LOGIN = "用户未登录"
    ERROR_SIGNATURE_EXPIRED = '签名过期'
    ERROR_LOGIN_UNDIFINED = '未知登录错误'
    ERROR_FIND_MODULE = '操作的对象不存在'
    ERROR_FORBIT = '对不起您没有操作的权限'
    ERROR_METHOD_FORBIT = '该请求方法不被允许'


if __name__ == '__main__':
    import re, sys
    for attr in dir(ZhError):
        if not re.match(r'^__', attr):
            print('|' + str(getattr(sys.modules[__name__], attr)) + ' | ' + getattr(ZhError, attr) + '|')
