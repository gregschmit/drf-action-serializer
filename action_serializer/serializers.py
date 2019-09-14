"""
This module implements the ``ModelActionSerializer`` which is a ``ModelSerializer`` but
which accepts more ``Meta`` attributes for per-action configurations of the fields.
"""

from rest_framework.serializers import *


class ModelActionSerializer(ModelSerializer):
    """
    Similar to ModelSerializer, except now in `get_field_names` and `get_extra_kwargs`,
    if a key for the current action exists in the `Meta.action_fields` dictionary, then
    abide by the `fields`, `exclude`, and `extra_kwargs` keys of the resulting
    dictionary.
    """

    def get_action_config(self):
        """
        Return the configuration in the `Meta.action_fields` dictionary for this view's
        action.
        """
        view = getattr(self, "context", {}).get("view", None)
        action = getattr(view, "action", None)
        action_fields = getattr(self.Meta, "action_fields", {})
        return action_fields.get(action, None)

    def get_field_names(self, declared_fields, info):
        """
        Returns the list of all field names that should be created when instantiating
        this serializer class. This is based on the default set of fields, but also
        takes into account the `Meta.fields` or `Meta.exclude` options if they have been
        specified, and also the `fields` and `exclude` properties for the action in
        `Meta.action_fields` dictionary.
        """

        action_config = self.get_action_config()
        if action_config:
            fields = action_config.get("fields", None)
            exclude = action_config.get("exclude", None)
        else:
            fields = getattr(self.Meta, "fields", None)
            exclude = getattr(self.Meta, "exclude", None)

        if fields and fields != ALL_FIELDS and not isinstance(fields, (list, tuple)):
            raise TypeError(
                'The `fields` option must be a list or tuple or "__all__". '
                "Got %s." % type(fields).__name__
            )

        if exclude and not isinstance(exclude, (list, tuple)):
            raise TypeError(
                "The `exclude` option must be a list or tuple. Got %s."
                % type(exclude).__name__
            )

        assert not (fields and exclude), (
            "Cannot set both 'fields' and 'exclude' options on "
            "serializer {serializer_class}.".format(
                serializer_class=self.__class__.__name__
            )
        )

        assert not (fields is None and exclude is None), (
            "Creating a ModelSerializer without either the 'fields' attribute "
            "or the 'exclude' attribute has been deprecated since 3.3.0, "
            "and is now disallowed. Add an explicit fields = '__all__' to the "
            "{serializer_class} serializer.".format(
                serializer_class=self.__class__.__name__
            ),
        )

        if fields == ALL_FIELDS:
            fields = None

        if fields is not None:
            return fields

        # Use the default set of field names if `Meta.fields` is not specified.
        fields = self.get_default_field_names(declared_fields, info)

        if exclude is not None:
            # If `Meta.exclude` is included, then remove those fields.
            for field_name in exclude:
                assert field_name not in self._declared_fields, (
                    "Cannot both declare the field '{field_name}' and include "
                    "it in the {serializer_class} 'exclude' option. Remove the "
                    "field or, if inherited from a parent serializer, disable "
                    "with `{field_name} = None`.".format(
                        field_name=field_name, serializer_class=self.__class__.__name__
                    )
                )

                assert field_name in fields, (
                    "The field '{field_name}' was included on serializer "
                    "{serializer_class} in the 'exclude' option, but does "
                    "not match any model field.".format(
                        field_name=field_name, serializer_class=self.__class__.__name__
                    )
                )
                fields.remove(field_name)

        return fields

    def get_extra_kwargs(self):
        """
        Return a dictionary mapping field names to a dictionary of
        additional keyword arguments.
        """
        action_config = self.get_action_config()
        if action_config:
            extra_kwargs = copy.deepcopy(action_config.get("extra_kwargs", {}))
        else:
            extra_kwargs = copy.deepcopy(getattr(self.Meta, "extra_kwargs", {}))

        read_only_fields = getattr(self.Meta, "read_only_fields", None)
        if read_only_fields is not None:
            if not isinstance(read_only_fields, (list, tuple)):
                raise TypeError(
                    "The `read_only_fields` option must be a list or tuple. "
                    "Got %s." % type(read_only_fields).__name__
                )
            for field_name in read_only_fields:
                kwargs = extra_kwargs.get(field_name, {})
                kwargs["read_only"] = True
                extra_kwargs[field_name] = kwargs

        else:
            # Guard against the possible misspelling `readonly_fields` (used
            # by the Django admin and others).
            assert not hasattr(self.Meta, "readonly_fields"), (
                "Serializer `%s.%s` has field `readonly_fields`; "
                "the correct spelling for the option is `read_only_fields`."
                % (self.__class__.__module__, self.__class__.__name__)
            )

        return extra_kwargs
