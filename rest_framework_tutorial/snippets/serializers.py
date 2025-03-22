from rest_framework import serializers
from .models import LANGUAGE_CHOICES, STYLE_CHOICES, Snippet


# SERIALIZER
class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
    created_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        """
        create and return a new snippet instance, based on the validated data
        spread the validated_data dict
        """
        return Snippet.objects.create(**validated_data)
    
    def update(self, instance: Snippet, validated_data):
        """
        update and return the exsiting snippets data, based on the validated data

        """
        instance.title = validated_data.get("title", instance.title)
        instance.code = validated_data.get("code", instance.code)
        instance.linenos = validated_data.get("linenos", instance.linenos)
        instance.language = validated_data.get("language", instance.language)
        instance.style = validated_data.get("style", instance.style)
        instance.save()
        return instance


# MODEL SERIALIZER
# model serializer abstract the dupplicate fields 
# that are already in models
class SnippetMSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = [
            'id', 'title', 'code', 'linenos', 
            'language', 'style', 'created_at'
        ] 
        # specify fields that you want to be a 
        # part of the serializer
        # Note: it is important that fields should be a part of the models
        # if you want to create a extra fields that are not in the serializer
        # you can create field in this class