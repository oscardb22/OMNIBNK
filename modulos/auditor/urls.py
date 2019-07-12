from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from .views import LisLog

urlpatterns = [
    url(r'^lis/log/$',
        permission_required(raise_exception=True, perm='admin.view_log')
        (login_required(LisLog.as_view(), login_url=reverse_lazy('users:login'))),
        name='lis_log'),
]
