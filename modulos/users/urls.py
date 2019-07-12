from django.urls import path
from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .views import Login, Panel, exit
from .views import Rus, LisMov, RegMov, UpdMov, DelMov
from .views import ApiLogin, ApiRus, ApiLisMov, ApiRegMov, ApiUpdMov, ApiDelMov, MovieDetail

urlpatterns = [
    url(r'^$', Login.as_view(), name='login'),
    url(r'^salir/$', exit, name='salir'),
    url(r'^start/$',
        login_required(Panel.as_view(), login_url=reverse_lazy('users:login')), name='base'),
    url(r'^reg/usu/$', login_required(Rus.as_view(), login_url=reverse_lazy('users:login')), name='rus'),
    # MODULOS
    url(r'^lis/mov/$', login_required(LisMov.as_view(), login_url=reverse_lazy('users:login')), name='lis_mov'),
    url(r'^reg/mov/$', login_required(RegMov.as_view(), login_url=reverse_lazy('users:login')), name='reg_mov'),
    url(r'^upd/(?P<pk>\d+)/mov/$', login_required(UpdMov.as_view(), login_url=reverse_lazy('users:login')),
        name='upd_mov'),
    url(r'^del/(?P<pk>\d+)/mov/$', login_required(DelMov.as_view(), login_url=reverse_lazy('users:login')),
        name='del_mov'),
    # RESTful API
    path('restfulapi/login/', ApiLogin, name='api_login'),
    path('restfulapi/salir/', exit, name='api_salir'),
    path(r'restfulapi/reg/usu/', login_required(ApiRus.as_view(), login_url=reverse_lazy('users:login')),
         name='api_rus'),
    # MODULOS
    path('restfulapi/lis/mov/', login_required(ApiLisMov.as_view(), login_url=reverse_lazy('users:login')),
         name='api_lis_mov'),
    path('restfulapi/reg/mov/', login_required(ApiRegMov.as_view(), login_url=reverse_lazy('users:login')),
         name='api_reg_mov'),
    path('restfulapi/upd/<int:pk>/mov/', login_required(ApiUpdMov.as_view(), login_url=reverse_lazy('users:login')),
         name='api_upd_mov'),
    path('restfulapi/del/<int:pk>/mov/', login_required(ApiDelMov.as_view(), login_url=reverse_lazy('users:login')),
         name='api_del_mov'),
    path('restfulapi/det/<int:pk>/mov/', login_required(MovieDetail.as_view(), login_url=reverse_lazy('users:login')),
         name='api_det_mov'),

]
