from django.http import HttpResponse
from nsj_gcf_utils.json_util import json_dumps, json_loads
from typing import Any

from mytodo.repository.task_repository import TaskRepository
from mytodo.view.generic_view import GenericView


class TaskView(GenericView):

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._repository = TaskRepository()

    def get(self, request, *args, **kwargs):

        try:
            # Getting ID
            id = kwargs["id"]

            # Getting task
            task = self._repository.find_by_id(id)

            if task is None:
                return HttpResponse('', status=404)

            return HttpResponse(json_dumps(task), status=200, content_type='application/json')
        except Exception as e:
            msg = '{"message": "Unknown error getting task: ' + \
                str(e) + '"}'
            return HttpResponse(content=msg, status=500)

    def put(self, request, *args, **kwargs):

        try:
            # Loading json
            task = json_loads(request.body.decode())

            # Getting ID
            id = kwargs["id"]

            # Checking required attributes
            required_attributes = [
                'description', 'priority', 'complexity', 'created_at', 'status']
            missing_attributes = self._check_required_attributes(
                required_attributes, task)
            if missing_attributes:
                msg = '{"message": "Missing parameters: ' + \
                    str(missing_attributes) + '."'
                return HttpResponse(msg, status=400)

            # Updating task
            self._repository.update(id, task)
            self._repository.update_status(id, task['status'])

            return HttpResponse(content='', status=204)
        except Exception as e:
            msg = '{"message": "Unknown error updating task status: ' + \
                str(e) + '"}'
            return HttpResponse(content=msg, status=500)

    def patch(self, request, *args, **kwargs):

        try:
            # Loading json
            task = json_loads(request.body.decode())

            # Getting ID
            id = kwargs["id"]

            # Checking required attributes
            required_attributes = ['status']
            missing_attributes = self._check_required_attributes(
                required_attributes, task)
            if missing_attributes:
                msg = '{"message": "Missing parameters: ' + \
                    str(missing_attributes) + '."'
                return HttpResponse(msg, status=400)

            # Updating task status
            self._repository.update_status(id, task['status'])

            return HttpResponse(content='', status=204)
        except Exception as e:
            msg = '{"message": "Unknown error updating task status: ' + \
                str(e) + '"}'
            return HttpResponse(content=msg, status=500)
