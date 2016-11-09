from django.test import TestCase

from . import model_instances


class TestConversation(TestCase):
    """
    A test case for a model `Conversation`
    """
    def setUp(self):
        self.conversation = model_instances.conversation()

    def test_init(self):
        """
        Ensures that the instance of the model `Conversation` can be
        created
        """
        self.assertIsNotNone(self.conversation.pk, 'Should have an instance')

    def test_person_info_unicode(self):
        """
        Ensures that the method `__unicode__` of the model `Conversation`
        returns a valid string
        """
        interlocutors = self.conversation.interlocutors
        self.assertEqual(self.conversation.__unicode__(),
                         '%s-%s' % (interlocutors.first().username,
                                    interlocutors.last().username),
                         'Method `__unicode__` of the  model `Conversation`'
                         'should return a valid string')


class TestMessage(TestCase):
    """
    A test case for a model `Message`
    """
    def setUp(self):
        self.message = model_instances.message()

    def test_init(self):
        """
        Ensures that the instance of the model `Message` can be
        created
        """
        self.assertIsNotNone(self.message.pk, 'Should have an instance')

    def test_person_info_unicode(self):
        """
        Ensures that the method `__unicode__` of the model `Message`
        returns a valid string
        """
        self.assertEqual(self.message.__unicode__(),
                         '%s: %s' % (self.message.sender, self.message.body),
                         'Method `__unicode__` of the model `Message`'
                         'should return a valid string')
