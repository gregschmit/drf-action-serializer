"""
This module implements an example ``ModelAdminSerializer`` and ViewSet for the
Django ``Group`` model.
"""

from django.contrib.auth.models import Group
from rest_framework.viewsets import ModelViewSet

from .serializers import ModelActionSerializer


class GroupActionSerializer(ModelActionSerializer):
    """
    An example serializer for the Django ``Group`` model, where the ``list`` action
    causes less fields to be serialized than normal.
    """

    class Meta:
        model = Group
        fields = ("id", "name", "permissions")
        action_fields = {"list": {"fields": ("id", "name")}}


class GroupViewSet(ModelViewSet):
    """
    An example viewset for the Django ``Group`` model.
    """

    serializer_class = GroupActionSerializer
    queryset = Group.objects.all()
