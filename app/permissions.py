from rest_framework import permissions


class GlobalDefaultPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        model_permission_codename = self.__get_model_permission_codename(
            method=request.method,
            view=view,
        )

        if not model_permission_codename:
            return False

        return request.user.has_perm(model_permission_codename)

    def __get_model_permission_codename(self, method, view):
        try:
            if hasattr(view, "queryset") and view.queryset is not None:
                model = view.queryset.model
            elif hasattr(view, "get_queryset"):
                model = view.get_queryset().model
            else:
                return None

            model_name = model._meta.model_name
            app_label = model._meta.app_label
            action = self.__get_action_suffix(method)
            if not action:
                return None
            return f"{app_label}.{action}_{model_name}"
        except AttributeError:
            return None

    def __get_action_suffix(self, method):
        method_actions = {
            "GET": "view",
            "POST": "add",
            "PUT": "change",
            "PATCH": "change",
            "DELETE": "delete",
            "OPTIONS": "view",
            "HEAD": "view",
        }
        return method_actions.get(method, "")
