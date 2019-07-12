from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView, View, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.views.generic.edit import ModelFormMixin
from .forms import UsersForm, MovieForm
from .models import Users, Movie
from modulos.auditor.views import log_actualizado, log_registro
from django.urls import reverse_lazy

from .serializers import UsersSerializer, MovieSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404


class Panel(TemplateView):
    template_name = "base.html"

    def dispatch(self, *args, **kwargs):
        return super(Panel, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(Panel, self).get_context_data(**kwargs)
        return context


class Login(View):
    @staticmethod
    def get(request):
        if request.user:
            if request.user.is_active:
                return HttpResponseRedirect(reverse_lazy('users:base'))
        return render(request, 'inicio.html')

    @staticmethod
    def post(request):
        if request.method == 'POST':
            username = request.POST['usu']
            password = request.POST['passwd']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, "Login exitoso")
                    return HttpResponseRedirect(reverse_lazy('users:base'))
                else:
                    messages.warning(request, "Usuario invalido")
                    return HttpResponseRedirect(reverse_lazy('users:login'))
            else:
                messages.warning(request, "Login invalido")
                return HttpResponseRedirect(reverse_lazy('users:login'))
        else:
            return HttpResponseRedirect(reverse_lazy('users:login'))


def exit(request):
    if request.user:
        messages.success(request, "We will wait for you.")
        logout(request)
    return HttpResponseRedirect('/')


# User
class Rus(CreateView):
    template_name = 'formadmin.html'
    form_class = UsersForm
    model = Users

    def get_form_kwargs(self):
        kwargs = super(ModelFormMixin, self).get_form_kwargs()
        kwargs.update({'instance': self.object})
        kwargs.update({'request': self.request})
        return kwargs

    def get_success_url(self):
        messages.success(self.request, "User created")
        return reverse_lazy('users:base')

    def get_context_data(self, **kwargs):
        context = super(Rus, self).get_context_data(**kwargs)
        context['tit_cont'] = 'Create'
        context['sub_tit_cont'] = ' user'
        return context

    def form_valid(self, form):
        form.instance.set_password(form.instance.password)
        form.instance.pro = self.request.user
        if form.has_changed:
            log_registro(form.instance, self.request.user, {"fields": form.changed_data})
        return super(Rus, self).form_valid(form)


# Movies
class LisMov(ListView):
    template_name = 'movies/lis.html'
    model = Movie
    paginate_by = 30

    def get_queryset(self):
        qs = Movie.objects.all()
        nom = self.request.GET.get('nom', None)
        if nom:
            qs = qs.filter(title__icontains=nom)
        return qs

    def get_context_data(self, **kwargs):
        context = super(LisMov, self).get_context_data(**kwargs)
        tot = len(self.get_queryset())
        context["tot"] = tot
        context['tit_cont'] = 'List'
        context['sub_tit_cont'] = ' of moviess'
        nom = self.request.GET.get('nom', None)
        if nom:
            context["nom"] = nom
        return context


class RegMov(CreateView):
    template_name = 'formadmin.html'
    form_class = MovieForm
    model = Movie

    def get_form_kwargs(self):
        kwargs = super(ModelFormMixin, self).get_form_kwargs()
        kwargs.update({'instance': self.object})
        kwargs.update({'request': self.request})
        return kwargs

    def get_success_url(self):
        messages.success(self.request, "Movie created")
        return reverse_lazy('users:lis_mov')

    def get_context_data(self, **kwargs):
        context = super(RegMov, self).get_context_data(**kwargs)
        context['tit_cont'] = 'Create'
        context['sub_tit_cont'] = ' movie'
        return context

    def form_valid(self, form):
        form.instance.title = form.instance.title.upper()
        form.instance.cre = self.request.user
        if form.has_changed:
            log_registro(form.instance, self.request.user, {"fields": form.changed_data})
        return super(RegMov, self).form_valid(form)


class UpdMov(UpdateView):
    template_name = 'formadmin.html'
    form_class = MovieForm
    model = Movie

    def get_form_kwargs(self):
        kwargs = super(ModelFormMixin, self).get_form_kwargs()
        kwargs.update({'instance': self.object})
        kwargs.update({'request': self.request})
        return kwargs

    def get_object(self, queryset=None):
        qs = Movie.objects.get(pk=self.kwargs['pk'])
        return qs

    def get_success_url(self):
        messages.success(self.request, "Movie is update")
        return reverse_lazy('users:lis_mov')

    def get_context_data(self, **kwargs):
        context = super(UpdMov, self).get_context_data(**kwargs)
        context['tit_cont'] = 'Update'
        context['sub_tit_cont'] = ' movies'
        return context

    def form_valid(self, form):
        form.instance.title = form.instance.title.upper()
        if not form.instance.cre:
            form.instance.cre = self.request.user
        if form.has_changed:
            log_actualizado(form.instance, self.request.user, {"fields": form.changed_data})
        return super(UpdMov, self).form_valid(form)


class DelMov(DeleteView):
    template_name = 'del.html'
    model = Movie

    def get_success_url(self):
        messages.success(self.request, "Movie is delete")
        return reverse_lazy('users:lis_mov')

    def get_context_data(self, **kwargs):
        context = super(DelMov, self).get_context_data(**kwargs)
        context['tit_cont'] = 'Delete'
        context['sub_tit_cont'] = ' movies'
        return context


# RESTFULAPI
class ApiLogin(viewsets.ModelViewSet):
    authentication_classes = (BasicAuthentication, )
    permission_classes = (IsAuthenticated,)
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


# User
class ApiRus(CreateAPIView):
    serializer_class = UsersSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.pro = self.request.user
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        log_registro(serializer, self.request.user, {"fields": []})
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# Movies
class ApiLisMov(ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        qs = Movie.objects.all()
        nom = self.request.GET.get('nom', None)
        if nom:
            qs = qs.filter(title__icontains=nom)
        return qs


class ApiRegMov(CreateAPIView):
    serializer_class = MovieSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def form_valid(self, form):
        form.instance.title = form.instance.title.upper()
        form.instance.cre = self.request.user
        if form.has_changed:
            log_registro(form.instance, self.request.user, {"fields": form.changed_data})
        return super(RegMov, self).form_valid(form)


class ApiUpdMov(UpdateAPIView):
    serializer_class = MovieSerializer

    def get_object(self):
        qs = Movie.objects.get(pk=self.kwargs['pk'])
        return qs

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.cre:
            instance.cre = self.request.user
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        log_actualizado(instance, self.request.user, {"fields": []})
        return Response(serializer.data)


class ApiDelMov(DestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_object(self):
        obj = get_object_or_404(Movie, id=self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj


class MovieDetail(RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
