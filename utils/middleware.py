
import logging
import re

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from airtic.models import User


class TestMiddlware(MiddlewareMixin):
    def process_request(self, request):
        # 对所有的请求都进行登录状态的校验
        path = request.path
        not_need_chenk = ['/airtic/register/', '/airtic/login/', '/leading/.*/', '/media/.*/']
        for chenk_path in not_need_chenk:
            if re.match(chenk_path, path):
                # 匹配上，不需要校验
                return None

        try:
            user_id = request.session['user_id']
            user = User.objects.get(pk=user_id)
            request.user = user
            return None
        except Exception as e:
            return HttpResponseRedirect(reverse('airtic:login'))


