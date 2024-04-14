"""
This file contains custom renderers for format of responses of APIs in this project
"""

from rest_framework import renderers
import json


class DefaultRenderer(renderers.JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if not renderer_context["response"].exception:
            response = ""

            if "ErrorDetail" in str(data):
                response = json.dumps(
                    {
                        "success": True,
                        "status_code": renderer_context["response"].status_code,
                        "message": data["message"],
                        "errors": data["data"],
                    }
                )
            else:
                response = json.dumps(
                    {
                        "success": True,
                        "status_code": renderer_context["response"].status_code,
                        "message": data["message"],
                        "results": data["data"],
                    }
                )

            return response

        return super().render(data, accepted_media_type=accepted_media_type, renderer_context=renderer_context)
