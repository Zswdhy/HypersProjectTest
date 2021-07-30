from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

from User.models import User
from utils.my_validation_error import MyValidationError


class UserModelSerializer(serializers.ModelSerializer):
    password_2 = serializers.CharField(label='确认密码', write_only=True)  # 确认密码

    class Meta:
        model = User
        fields = ['username', 'password', 'password_2', 'email', 'category']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_2']:
            raise MyValidationError({'code': '400', 'message': '两次密码不一致'})
        return attrs

    def create(self, validated_data):
        del validated_data['password_2']
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['username'] = self.user.username
        data['category'] = self.user.category
        return data
