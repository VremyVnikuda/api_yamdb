from rest_framework import serializers


def check_for_me_name(value):
    if value == 'me':
        raise serializers.ValidationError('Имя me запрещено')
