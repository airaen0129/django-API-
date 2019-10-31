from .models import Essay, Album, Files
from rest_framework import serializers

class EssaySerializer(serializers.ModelSerializer):
    # author를 자동으로 지정
    author_name = serializers.ReadOnlyField(source='author.username')
    #건들지 못하게 readonly로 지정하기

    class Meta:
        model = Essay
        fields = ('pk', 'title', 'body', 'author_name')


class AlbumSerializer(serializers.ModelSerializer):

    author_name = serializers.ReadOnlyField(source='author.username')
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Album
        fields = ('pk', 'author_name', 'image', 'desc')


class FilesSerializer(serializers.ModelSerializer):

    author = serializers.ReadOnlyField(source='author.username')
    myfile = serializers.FileField(use_url=True)

    class Meta:
        model = Files
        fields = ('pk', 'author', 'myfile', 'desc')
