from rest_framework import serializers, validators
from django.contrib.auth.models import User
from .models import Note, NoteAttachment


class NoteSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        note = Note.objects.create(
            user=validated_data['user'],
            text=validated_data['text'],
        )
        attachments = self.context['attachments']
        for attachment in attachments:
            NoteAttachment.objects.create(note=note,
                                          attachment=attachment)
        return note

    class Meta:
        model = Note
        fields = '__all__'


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

        extra_kwargs = {
            "password": {
                "write_only": True
            },
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), "Email already exists!"
                    )
                ]
            }
        }

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')

        user = User.objects.create(
            username=username,
            email=email,
            password=password,
        )

        return user
