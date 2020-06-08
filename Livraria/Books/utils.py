from django.http import HttpResponseNotAllowed


def allowed_method(http_verb):
    def decorator(my_func):
        def internal(*args, **kwargs):
            request = args[0]
            if not request.method == http_verb:
                return HttpResponseNotAllowed('Method not allowed, must be ' + http_verb)
            original_result = my_func(*args, **kwargs)
            return original_result
        return internal
    return decorator
