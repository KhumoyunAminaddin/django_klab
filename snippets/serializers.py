from django.contrib import auth
from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class DetailSnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ["id", "title", "code", "linenos", "language", "style", "owner"]
        depth = 1


class SnippetSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Snippet
        fields = ["id", "title", "url", "code"]

    def create(self, validated_data): # POST request
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data): # PUT request
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get("title", instance.title)
        instance.code = validated_data.get("code", instance.code)
        instance.linenos = validated_data.get("linenos", instance.linenos)
        instance.language = validated_data.get("language", instance.language)
        instance.style = validated_data.get("style", instance.style)
        instance.save() # sql code execute
        return instance


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = auth.get_user_model()
        fields = "__all__"
