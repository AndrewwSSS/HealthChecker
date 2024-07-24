from django import template

register = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    result = request.GET.copy()
    for param, value in kwargs.items():
        if value is not None:
            result[param] = value
        else:
            result.pop(param, 0)
    return result.urlencode()
