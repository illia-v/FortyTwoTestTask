from django.test import TestCase

from ..models import ActionOnInstance
from hello.tests.model_instances import person_info


class TestCreateDbEntityAboutActionOnInstanceSignalHandler(TestCase):
    def setUp(self):
        person_info_obj = person_info()
        self.person_info_obj_str = str(person_info_obj.__dict__)
        self.last_ActionOnInstance_instance_creation = (
            ActionOnInstance.objects.last())

        person_info_obj.first_name = 'I'
        person_info_obj.save()
        self.last_ActionOnInstance_instance_editing = (
            ActionOnInstance.objects.last())

        person_info_obj.delete()
        self.last_ActionOnInstance_instance_deletion = (
            ActionOnInstance.objects.last())

    def test_handler_creates_ActionOnInstance_instance(self):
        """
        Ensures that `create_db_entity_about_action_on_instance` creates
        instance of `ActionOnInstance`
        """
        self.assertEqual(
            self.last_ActionOnInstance_instance_creation.instance,
            self.person_info_obj_str,
            'Should create `ActionOnInstance` instance'
        )

    def test_handler_creates_ActionOnInstance_instance_about_creation(self):
        """
        Ensures that `create_db_entity_about_action_on_instance` creates
        instance of `ActionOnInstance` about creation of object
        """
        self.assertEqual(self.last_ActionOnInstance_instance_creation.action,
                         1, 'Should create `ActionOnInstance` instance '
                         'when instance of any model is created')

    def test_handler_creates_ActionOnInstance_instance_about_editing(self):
        """
        Ensures that `create_db_entity_about_action_on_instance` creates
        instance of `ActionOnInstance` about editing of object
        """
        self.assertEqual(self.last_ActionOnInstance_instance_editing.action,
                         2, 'Should create `ActionOnInstance` instance '
                         'when instance of any model is edited')

    def test_handler_creates_ActionOnInstance_instance_about_deletion(self):
        """
        Ensures that `create_db_entity_about_action_on_instance` creates
        instance of `ActionOnInstance` about deletion of object
        """
        self.assertEqual(self.last_ActionOnInstance_instance_deletion.action,
                         3, 'Should create `ActionOnInstance` instance '
                         'when instance of any model is deleted')
