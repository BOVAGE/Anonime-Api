from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model
from .serializers import MessageSerializer
from .models import Message
from .permissions import IsRecipientOrWriteOnly

# Create your views here.
@api_view(['GET','POST'])
@permission_classes([IsRecipientOrWriteOnly])
def ListCreateMessageView(request, recipient_username):
    recipient = get_user_model().objects.get(username=recipient_username)
    if request.method == 'GET':
        messages = request.user.messages.all()
        serializer = MessageSerializer(messages, many=True)
        data = {
                'status': 'successful',
                'data': serializer.data
            }
        return Response(data, status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(recipient=recipient)
            data = {
                'status': 'created',
                'data': serializer.data
            }
            return Response(data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

@api_view(['GET','DELETE'])
@permission_classes([IsRecipientOrWriteOnly])
def RetrieveDeleteMessageView(request, recipient_username, message_id):
    try:
        message = request.user.messages.get(id=message_id)
    except Message.DoesNotExist:
        raise NotFound("Message with that Id not found!")
    serializer = MessageSerializer(message)
    if request.method == "GET":
        data = {
            'status': 'successful',
            'data': serializer.data
        }
        return Response(data, status.HTTP_200_OK)
    elif request.method == 'DELETE':
        message.delete()
        data = {
            'status': 'deleted',
        }
        return Response(data, status.HTTP_204_NO_CONTENT)
        