from rest_framework.response import Response
from django.shortcuts import render
from base.models import Book
from base.serializers import BookSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['username'] = user.username
        token['superuser?'] = user.is_superuser
        # ...
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getNotes(request):
	return Response("im protected")












@api_view(['GET'])
def index(request):
    return Response('hello')



@api_view(['GET','POST','DELETE','PUT','PATCH'])
def books(req,id=-1):
    if req.method =='GET':
        if id > -1:
            try:
                temp_book=Book.objects.get(id=id)
                return Response (BookSerializer(temp_book,many=False).data)
            except Book.DoesNotExist:
                return Response ("not found")
        all_books=BookSerializer(Book.objects.all(),many=True).data
        return Response ( all_books)
    if req.method =='POST':
        ser = BookSerializer(data=req.data)
        if ser.is_valid():
            ser.save()
            return Response ("posted")
        else:
            return Response (ser.errors)
    if req.method =='DELETE':
        try:
            temp_book=Book.objects.get(id=id)
        except Book.DoesNotExist:
            return Response ("not found")    
       
        temp_book.delete()
        return Response ("deleted")
    if req.method =='PUT':
        try:
            temp_book=Book.objects.get(id=id)
        except Book.DoesNotExist:
            return Response ("not found")
       
        ser = BookSerializer(data=req.data)

        if ser.is_valid():
            ser.save()
            serialized_data = ser.data
            return Response(serialized_data)
        else:
            return Response(ser.errors)



