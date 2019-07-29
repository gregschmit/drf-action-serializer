"""
Tests for the drf-action-serializer package.
"""
# pylint: disable=unused-variable

import os

from django.db import models
from django.test import TestCase

from . import version
from .serializers import ModelActionSerializer


def dedent(blocktext):
    return '\n'.join([line[12:] for line in blocktext.splitlines()[1:-1]])


class RegularFieldsModel(models.Model):
    """
    A model class for testing regular flat fields.
    """
    auto_field = models.AutoField(primary_key=True)
    boolean_field = models.BooleanField(default=False)
    char_field = models.CharField(max_length=100)
    date_field = models.DateField()
    decimal_field = models.DecimalField(max_digits=3, decimal_places=1)
    email_field = models.EmailField(max_length=100)
    float_field = models.FloatField()
    integer_field = models.IntegerField()

    def method(self):
        return 'method'


class ModelActionSerializerTestCase(TestCase):
    """
    Tests for the ModelActionSerializer.
    """

    def test_action_fields(self):
        """
        Ensure `action_fields` are used if the context declares a list view.
        """
        class TestSerializer(ModelActionSerializer):
            class Meta:
                model = RegularFieldsModel
                fields = ('char_field')
                action_fields = {
                    'list': {'fields': ('auto_field', 'char_field')}
                }

        expected = dedent("""
            TestSerializer(context={'view': <class 'action_serializer.tests.ActionView'>}):
                auto_field = IntegerField(read_only=True)
                char_field = CharField(max_length=100)
        """)
        context = {'view': type('ActionView', (object,), {'action': 'list'})}
        self.assertEqual(repr(TestSerializer(context=context)), expected)

    def test_action_fields_different_action(self):
        """
        Ensure normal `fields` are used if the context view action is different
        than what is defined in the `action_fields`
        """
        class TestSerializer(ModelActionSerializer):
            class Meta:
                model = RegularFieldsModel
                fields = ('char_field',)
                action_fields = {
                    'list': {'fields': ('auto_field', 'char_field')}
                }

        expected = dedent("""
            TestSerializer(context={'view': <class 'action_serializer.tests.ActionView'>}):
                char_field = CharField(max_length=100)
        """)
        context = {'view': type('ActionView', (object,), {'action': 'create'})}
        self.assertEqual(repr(TestSerializer(context=context)), expected)

    def test_action_extra_kwargs(self):
        """
        Ensure `action_fields` `extra_kwargs` are used if they are defined and
        the context view action matches.
        """
        class TestSerializer(ModelActionSerializer):
            class Meta:
                model = RegularFieldsModel
                fields = ('char_field')
                action_fields = {
                    'list': {
                        'fields': ('auto_field', 'char_field'),
                        'extra_kwargs': {
                            'auto_field': {
                                'required': False,
                                'read_only': False,
                            },
                        }
                    }
                }

        expected = dedent("""
            TestSerializer(context={'view': <class 'action_serializer.tests.ActionView'>}):
                auto_field = IntegerField(read_only=False, required=False)
                char_field = CharField(max_length=100)
        """)
        context = {'view': type('ActionView', (object,), {'action': 'list'})}
        self.assertEqual(repr(TestSerializer(context=context)), expected)

    def test_action_exclude(self):
        """
        Ensure `action_fields` `exclude` is used if it is defined and the
        context view action matches.
        """
        auto_field = models.AutoField(primary_key=True)
        boolean_field = models.BooleanField(default=False)
        char_field = models.CharField(max_length=100)
        date_field = models.DateField()
        decimal_field = models.DecimalField(max_digits=3, decimal_places=1)
        email_field = models.EmailField(max_length=100)
        float_field = models.FloatField()
        integer_field = models.IntegerField()
        class TestSerializer(ModelActionSerializer):
            class Meta:
                model = RegularFieldsModel
                fields = ('char_field')
                action_fields = {'list': {'exclude': (
                    'boolean_field',
                    'date_field',
                    'float_field',
                    'integer_field',
                )}}

        expected = dedent("""
            TestSerializer(context={'view': <class 'action_serializer.tests.ActionView'>}):
                auto_field = IntegerField(read_only=True)
                char_field = CharField(max_length=100)
                decimal_field = DecimalField(decimal_places=1, max_digits=3)
                email_field = EmailField(max_length=100)
        """)
        context = {'view': type('ActionView', (object,), {'action': 'list'})}
        self.assertEqual(repr(TestSerializer(context=context)), expected)


class VersionTestCase(TestCase):
    """
    Tests for versioning script.
    """

    def setUp(self):
        # put us into the package directory
        os.chdir(os.path.normpath(os.path.dirname(os.path.abspath(__file__))))

    def test_version_is_str(self):
        self.assertTrue(isinstance(version.get_version(), str))

    def test_stamp_unstamp(self):
        stamp_location = './VERSION_STAMP'
        try:
            os.remove(stamp_location)
        except OSError:
            pass
        version.stamp_directory('.')
        self.assertTrue(os.path.exists(stamp_location))
        self.assertTrue(os.path.isfile(stamp_location))
        version.unstamp_directory('.')
        self.assertFalse(os.path.exists(stamp_location))
