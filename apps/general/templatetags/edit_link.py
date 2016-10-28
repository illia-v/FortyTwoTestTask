from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag
def edit_link(model_instance):
    """
    A template tag which accepts any object and renders a link to its
    admin edit page
    """
    try:
        return reverse(
            'admin:%s_%s_change' % (model_instance._meta.app_label,
                                    model_instance._meta.module_name),
            args=(model_instance.pk,)
        )
    except AttributeError:
        raise ValueError('The tag accepts only a model instance')
