from django.db import models
from django.contrib.auth.models import AbstractUser


class church_branch(models.Model):
    branch_name = models.CharField(max_length=100)
    fb_number = models.CharField(max_length=100)
    branch_head = models.CharField(max_length=200)
    centre_name = models.CharField(max_length=100)

    def __str__(self):
        return self.branch_name

class User(AbstractUser):
    is_superuser= models.BooleanField('Is superuser', default=False)
    is_admin= models.BooleanField('Is admin', default=False)
    is_user= models.BooleanField('Is user', default=False)
    branch = models.ForeignKey(church_branch, on_delete=models.CASCADE,null=True)


class church_member(models.Model):
    full_name = models.CharField(max_length=250)
    gender = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    id_number = models.CharField(max_length=13)
    place = models.CharField(max_length=150)
    parent_contact = models.CharField(max_length=150)
    institution_name = models.CharField(max_length=150)
    field_of_study = models.CharField(max_length=150)
    branch = models.ForeignKey(church_branch, on_delete=models.CASCADE)


    def __str__(self):
        return f'Church Member: {self.full_name}'   
    
class Role(models.Model):
    role = models.CharField(max_length=250)
    structure = models.CharField(max_length=250)
    member = models.ForeignKey(church_member, on_delete=models.CASCADE)
    branch = models.ForeignKey(church_branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.role
    
class Attendance(models.Model):
    date = models.CharField(max_length=250)
    attendance = models.CharField(max_length=250)
    structure = models.CharField(max_length=250)
    member = models.ForeignKey(church_member, on_delete=models.CASCADE)
    role= models.CharField(max_length=250)
    branch = models.ForeignKey(church_branch, on_delete=models.CASCADE)

    def __str__(self):
        return self.attendance
    
    
class Attendance_date(models.Model):
    date = models.CharField(max_length=250)
    branch = models.ForeignKey(church_branch, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.date
    
class Attendance_List(models.Model):
    date = models.CharField(max_length=250)
    students_present = models.CharField(max_length=250)
    students_absent = models.CharField(max_length=250)
    students_total = models.CharField(max_length=250)
    teachers_present = models.CharField(max_length=250)
    teachers_absent = models.CharField(max_length=250)
    teachers_total = models.CharField(max_length=250)
    committee_present = models.CharField(max_length=250)
    committee_absent = models.CharField(max_length=250)
    committee_total = models.CharField(max_length=250)
    health_present = models.CharField(max_length=250)
    health_absent = models.CharField(max_length=250)
    health_total = models.CharField(max_length=250)
    LCDC_Management_present = models.CharField(max_length=250)
    LCDC_Management_absent = models.CharField(max_length=250)
    LCDC_Management_total = models.CharField(max_length=250)
    branch = models.ForeignKey(church_branch, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.date
    


