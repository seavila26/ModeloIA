from rest_framework import serializers

from disco_optico.models import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('name','user')