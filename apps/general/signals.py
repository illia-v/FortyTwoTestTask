from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import ActionOnInstance


@receiver(post_save)
@receiver(post_delete)
def create_db_entity_about_action_on_instance(sender, **kwargs):
    if sender.__name__ == 'ActionOnInstance':
        return

    if kwargs.get('created', None) is not None:
        action = 1 if kwargs['created'] else 2
    else:
        action = 3

    ActionOnInstance.objects.create(
        app_name=sender._meta.app_label,
        model_name=sender.__name__,
        model_id=getattr(kwargs['instance'], 'id', None),
        instance=str(kwargs['instance'].__dict__),
        action=action
    )
