from django.http import HttpResponse
from nsj_gcf_utils.json_util import json_dumps, json_loads
from typing import Any

from mytodo.repository.task_repository import TaskRepository
from mytodo.view.generic_view import GenericView


class TasksView(GenericView):

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._repository = TaskRepository()

    def get(self, request, *args, **kwargs):

        try:
            status = False
            if request.GET.get('status'):
                status = (request.GET.get('status').lower() == 'true')

            tasks = self._repository.list(status)
            return HttpResponse(json_dumps(tasks), status=200, content_type='application/json')
        except Exception as e:
            msg = '{"message": "Unknown error listing tasks: ' + str(e) + '"}'
            return HttpResponse(content=msg, status=500)

    def post(self, request, *args, **kwargs):

        try:
            # Loading json
            task = json_loads(request.body.decode())

            # Checking required attributes
            required_attributes = ['description', 'priority', 'complexity']
            missing_attributes = self._check_required_attributes(
                required_attributes, task)
            if missing_attributes:
                msg = '{"message": "Missing parameters: ' + \
                    str(missing_attributes) + '."'
                return HttpResponse(msg, status=400)

            # Inserting into database
            id = self._repository.insert_new(task)

            # Retrieving inserted task
            task = self._repository.find_by_id(id)

            return HttpResponse(content=json_dumps(task), status=200)
        except Exception as e:
            msg = '{"message": "Unknown error listing tasks: ' + str(e) + '"}'
            return HttpResponse(content=msg, status=500)
