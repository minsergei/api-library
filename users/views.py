from rest_framework import generics
from users.models import User
from users.permissions import IsManager
from users.serializers import UserSerializer


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр профиля пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserCreateAPIView(generics.CreateAPIView):
    """Создание пользователя"""
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.is_active == ('True')
        user.save()


class UserListAPIView(generics.ListAPIView):
    """Вывод списка пользователей"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsManager,)


class UserUpdateAPIView(generics.UpdateAPIView):
    """Редактирование профиля пользователя"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (IsManager,)


class UserDestroyAPIView(generics.DestroyAPIView):
    """Удаление пользователя"""
    queryset = User.objects.all()
    permission_classes = (IsManager,)
