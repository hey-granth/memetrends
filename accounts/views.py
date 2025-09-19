from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
import logging


logger = logging.getLogger(__name__)
# https://docs.python.org/3.13/library/logging.html#module-level-functions


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

    # changed from register to post to adhere to RESTful conventions and handle post requests appropriately
    def post(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")

        if not username:
            logger.error("Username is required")
            return Response(
                {"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not password:
            logger.error("Password is required")
            return Response(
                {"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        if not email:
            logger.error("Email is required")
            return Response(
                {"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            logger.error("Username already exists")
            return Response(
                {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(email=email).exists():
            logger.error("Email already exists")
            return Response(
                {"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        if not self._validate_password(password):
            logger.error(
                "Password must be at least 8 characters long and contain both letters and numbers."
            )
            return Response(
                {
                    "error": "Password must be at least 8 characters long and contain both letters and numbers"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # it was previously User.objects.create, changed to create_user for proper password hashing. create_user automatically hashes the password, while create just stores it as it is (critical security issue).
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        logger.info(f"New user registered: {username}")
        return Response(
            {"message": "User created successfully"}, status=status.HTTP_201_CREATED
        )
