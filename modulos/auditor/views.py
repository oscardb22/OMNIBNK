from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.views.generic import ListView
import json


class LisLog(ListView):
    template_name = 'log/lis.html'
    model = LogEntry
    paginate_by = 30

    def get_queryset(self):
        if not self.request.user.is_staff:
            raise Http404
        qs = LogEntry.objects.all().order_by('-action_time')
        nom = self.request.GET.get('nom', None)
        con = self.request.GET.get('con', None)
        obj_id = self.request.GET.get('obj_id', None)
        objeto = self.request.GET.get('objeto', None)
        accion = self.request.GET.get('accion', None)
        fec_ini = self.request.GET.get('fec_ini', None)
        if obj_id:
            qs = qs.filter(object_id=obj_id)
        if objeto:
            qs = qs.filter(object_repr__istartswith=objeto)
        if accion:
            qs = qs.filter(action_flag=accion)
        if fec_ini:
            qs = qs.filter(action_time__range=('{} 00:00:01'.format(fec_ini), '{} 23:59:59'.format(fec_ini)))
        if con:
            qs = qs.filter(content_type__model__istartswith=con)
        if nom:
            qs = qs.filter(user__username__istartswith=nom)

        return qs

    def get_context_data(self, **kwargs):
        context = super(LisLog, self).get_context_data(**kwargs)
        nom = self.request.GET.get('nom', None)
        context["tot"] = len(self.get_queryset())
        context["tit_cont"] = 'Registro'
        context["sub_tit_cont"] = ' de eventos'
        con = self.request.GET.get('con', None)
        obj_id = self.request.GET.get('obj_id', None)
        objeto = self.request.GET.get('objeto', None)
        accion = self.request.GET.get('accion', None)
        fec_ini = self.request.GET.get('fec_ini', None)
        if obj_id:
            context["obj_id"] = obj_id
        if objeto:
            context["objeto"] = objeto
        if accion:
            context["accion"] = accion
        if fec_ini:
            context["fec_ini"] = fec_ini
        if con:
            context["con"] = con
        if nom:
            context["nom"] = nom
        return context


def log_actualizado(object, user, change_message=''):
    change_message = json.dumps({"changed": change_message})
    LogEntry.objects.log_action(
        user_id=user.pk,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=str(object),
        action_flag=CHANGE,
        change_message=change_message
    )


def log_registro(object, user, change_message=''):
    change_message = json.dumps({"added": change_message})
    LogEntry.objects.log_action(
        user_id=user.pk,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=str(object),
        action_flag=ADDITION,
        change_message=change_message
    )


def log_eliminado(object, user, change_message=''):
    LogEntry.objects.log_action(
        user_id=user.pk,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.pk,
        object_repr=str(object),
        action_flag=DELETION,
        change_message=change_message
    )
