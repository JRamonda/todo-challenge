from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task
from datetime import datetime
import logging

logger = logging.getLogger('main')

logger.info('Iniciando ejecucion del programa')

class CustomLoginView(LoginView):
  template_name = 'base/login.html'
  fields = '__all__'
  redirect_authenticated_user = True

  def get_success_url(self):
    return reverse_lazy('tasks')


class RegisterPage(FormView):
  template_name = 'base/register.html'
  form_class = UserCreationForm
  success_url = reverse_lazy('tasks')

  def form_valid(self, form):
    user = form.save()
    if user is not None:
      logger.info('Se ha registrado exitosamente al usuario')
      login(self.request, user)
    return super(RegisterPage, self).form_valid(form)
    
  #Redireccionar usuario autenticado
  def get(self, *args, **kwargs):
    if self.request.user.is_authenticated:
      logger.info('El usuario ya se encuentra logeado')

      return redirect('tasks')
    return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
  model = Task
  context_object_name = 'tasks'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['tasks'] = context['tasks'].filter(user=self.request.user)

    context['count'] = context['tasks'].filter(complete=False).count()
    search_input = self.request.GET.get('search-area') or ''

    if search_input:
      # checking if format matches the date
      res = True
      
      # using try-except to check for truth value
      try:
          res = bool(datetime.strptime(search_input, "%Y-%m-%d"))
      except ValueError:
          res = False

      if res:
        context['tasks'] = context['tasks'].filter(create__contains=search_input)
      else:
        context['tasks'] = context['tasks'].filter(title__startswith=search_input)

      logger.info('Se ha buscado una tarea')

    context['search_input'] = search_input

    return context


class TaskCreate(LoginRequiredMixin, CreateView):
  model = Task
  fields = ['title', 'description', 'complete']
  success_url = reverse_lazy('tasks')

  def form_valid(self, form):
    form.instance.user = self.request.user
    logger.info('Se ha creado una tarea')
    return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
  model = Task
  fields = ['title', 'description', 'complete']
  success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
  model = Task
  context_object_name = 'task'
  success_url = reverse_lazy('tasks')