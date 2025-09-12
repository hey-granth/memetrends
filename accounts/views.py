from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def _validate_password(self, password: str) -> bool:
        if len(password) < 8:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char.isalpha() for char in password):
            return False
        return True

    def register(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")

        if not username:
            return Response(
                {"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not password:
            return Response(
                {"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not email:
            return Response(
                {"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not self._validate_password(password):
            return Response(
                {
                    "error": "Password must be at least 8 characters long and contain both letters and numbers"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create(username=username, password=password, email=email)
        user.save()
        return Response(
            {"message": "User created successfully"}, status=status.HTTP_201_CREATED
        )
