from rest_framework.serializers import ModelSerializer
from .models import Student


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"
        
class StaffSerializer(ModelSerializer):
    class Meta:
        model = Staff
        fields = "__all__"
