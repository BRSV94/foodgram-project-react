from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, status, generics
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, ChangePasswordSerializer
from .permissions import IsOwnerProfile


class MyProfileViewSet(viewsets.GenericViewSet):

    def retrieve(self, request, *args, **kwargs):
        instance = User.objects.get(pk=self.request.user.pk)
        serializer = UserSerializer(instance)
        return Response(serializer.data)


class ChangePasswordView(generics.UpdateAPIView):
        serializer_class = ChangePasswordSerializer
        model = User
        permission_classes = (IsOwnerProfile,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                if self.object.check_password(serializer.data.get("current_password")):
                    self.object.set_password(serializer.data.get("new_password"))
                    self.object.save()
                    return Response(status=status.HTTP_204_NO_CONTENT)

            return Response(status=status.HTTP_400_BAD_REQUEST)