from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from .serializers import StudentSerializer
from rest_framework.response import Response
from .models import Student
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import viewsets


def home(request):
    context = {
        "student":"arivazhagan",
        "department":"CSBS",
        "cgpa":8.03,
    }
    return render(request,"home.html",context)

from django.shortcuts import render

def students(request):

    student_list = [

        "Arivazhagan",
        "Rahul",
        "Priya",
        "Kavin",
        "gopikaa vs"

    ]

    context = {

        "students": student_list

    }

    return render(request,"students.html",context)

from rest_framework import status

class StudentList(APIView):

    def get(self, request):

        students = Student.objects.all()

        serializer = StudentSerializer(
            students,
            many=True
        )

        return Response(serializer.data)


    def post(self, request):

        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


from django.shortcuts import get_object_or_404

class StudentDetail(APIView):

    def get(self, request, pk):

        student = get_object_or_404(
            Student,
            pk=pk
        )

        serializer = StudentSerializer(student)

        return Response(serializer.data)
    
    def put(self,request,pk):
        student = get_object_or_404(
            Student,
            pk=pk
        )
        serializer = StudentSerializer(
            student,
            data = request.data
        )
        if serializer.is_valid():
            serializer.save()

        return Response(

            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    def delete(self, request, pk):
        student = get_object_or_404(
            Student,
            pk=pk
        )
        student.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT

        )
    
#viewset

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


    
        
   

# Create your views here.
