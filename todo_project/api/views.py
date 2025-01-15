from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Task
from django.contrib.auth import login,logout
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .serializers import TaskSerializer,UserSerializer,LoginSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def taskList(request):
    tasks=Task.objects.filter(user=request.user).order_by('-id')
    serializer=TaskSerializer(tasks,many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def taskCreate(request):
    data = {
        'title': request.data.get('title'),
        'user': request.user.id  # Set the user field as the current logged-in user
    }

    serializer = TaskSerializer(data=data)

    # Validate and save the task if the data is valid
    if serializer.is_valid():
        task = serializer.save()  # Save the new task instance to the database
        return Response({"message": "Task created successfully", "task": TaskSerializer(task).data},
                        status=status.HTTP_201_CREATED)

    # Return validation errors if the serializer is not valid
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def taskDetail(request,pk):
    task=Task.objects.get(id=pk)
    serializer=TaskSerializer(task,many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def taskUpdate(request,pk):

    data = {
        'title': request.data.get('title'),
        'completed': request.data.get('completed'),
        'user': request.user.id  # Set the user field as the current logged-in user
    }
    task= Task.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def taskDelete(request,pk):
    task=Task.objects.get(id=pk)
    task.delete()
    return Response(status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
def signUp(request):

    serializer=UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def userList(request):

    users=User.objects.all()
    serializer=UserSerializer(users,many=True)
    return Response(serializer.data)

@api_view(['POST'])
def login_view(request):

    serializer=LoginSerializer(data=request.data)
    if serializer.is_valid():
        user=serializer.validated_data['user']
        login(request,user)
        return Response({"message": "Login successful."}, status=status.HTTP_200_OK)
    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
    return Response({"error": "User is not logged in."}, status=status.HTTP_400_BAD_REQUEST)

