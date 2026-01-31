from rest_framework import serializers
from .models import StoreItem, Purchase
from drf_spectacular.utils import extend_schema_field


class StoreItemSerializer(serializers.ModelSerializer):
    is_owned = serializers.SerializerMethodField()

    class Meta:
        model = StoreItem
        fields = [
            "id",
            "name",
            "description",
            "cost",
            "icon_name",
            "category",
            "image",
            "item_data",
            "is_owned",
        ]

    @extend_schema_field(serializers.BooleanField)
    def get_is_owned(self, obj):
        user = self.context.get("request").user
        if user.is_authenticated:
            return Purchase.objects.filter(user=user, item=obj).exists()
        return False
