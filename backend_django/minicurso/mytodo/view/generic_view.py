from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from typing import Any, Dict, List


@method_decorator(csrf_exempt, name='dispatch')
class GenericView(View):

    def _check_required_attributes(self, attributes: List[str], data_dict: Dict[str, Any]):

        missing = []
        for attribute in attributes:
            if not attribute in data_dict:
                missing.append(attribute)

        if len(missing) > 0:
            return missing
        else:
            return None
