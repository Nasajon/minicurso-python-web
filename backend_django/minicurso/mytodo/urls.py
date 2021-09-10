from django.urls import path

from mytodo.view.task_view import TaskView
from mytodo.view.tasks_view import TasksView
# from . import views

urlpatterns = [
    path('tasks', TasksView.as_view(), name='tasks'),
    path('tasks/<str:id>', TaskView.as_view(), name='task'),
]
