from django import template

register = template.Library()


@register.filter
def others(queryset, user):
    return queryset.exclude(email=user)

