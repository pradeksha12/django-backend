from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, Data
from .serializers import UserSerializer, DataSerializer


# User Signup
class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Login
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "token": str(refresh.access_token)
            })
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# User List (Admin only)
class UserListView(APIView):
    permission_classes = [IsAdminUser]  # Ensure only Admin can access this

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


# User Detail (GET, PUT, DELETE)
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]  # Ensure only Admins can access this

    def get(self, request, id):
        user = User.objects.filter(id=id).first()
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        user = User.objects.filter(id=id).first()
        if user:
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User updated successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        user = User.objects.filter(id=id).first()
        if user:
            user.delete()
            return Response({"message": "User deleted successfully"})
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


# Data Detail (GET, PUT, DELETE)
class DataDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can access this

    def get(self, request, id):
        data = Data.objects.filter(id=id).first()
        if data:
            serializer = DataSerializer(data)
            return Response(serializer.data)
        return Response({"message": "Data not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        data = Data.objects.filter(id=id).first()
        if data:
            serializer = DataSerializer(data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Data updated successfully"})
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Data not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        data = Data.objects.filter(id=id).first()
        if data:
            data.delete()
            return Response({"message": "Data deleted successfully"})
        return Response({"message": "Data not found"}, status=status.HTTP_404_NOT_FOUND)