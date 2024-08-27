from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('Logout/', views.Logout, name="Logout"),
    path('home/', views.home, name="home"),
    path('AddUser/', views.AddUser, name="AddUser"),
    path('SuperuserMonitoringTool/<int:id>', views.SuperuserMonitoringTool, name="SuperuserMonitoringTool"),
    path('AddChurchBranchForm/', views.AddChurchBranchForm, name="AddChurchBranchForm"),
    path('AddChurchBranch/', views.AddChurchBranch, name="AddChurchBranch"),
    path('AddStudent/', views.AddStudent, name="AddStudent"),
    path('AddTeacher/', views.AddTeacher, name="AddTeacher"),
    path('AddCommitteeMember/', views.AddCommitteeMember, name="AddCommitteeMember"),
    path('AddLCDC_Management/', views.AddLCDC_Management, name="AddLCDC_Management"),
    path('StartAttendance', views.StartAttendance, name="StartAttendance"),
    path('AttendanceList', views.AttendanceList, name="AttendanceList"),
    path('SelectAttendanceDate', views.SelectAttendanceDate, name="SelectAttendanceDate"),

    path('AddStudentForm/', views.AddStudentForm, name="AddStudentForm"),
    path('AddTeacherForm/', views.AddTeacherForm, name="AddTeacherForm"),
    path('AddCommitteeMemberForm/', views.AddCommitteeMemberForm, name="AddCommitteeMemberForm"),
    path('AddLCDC_ManagementForm/', views.AddLCDC_ManagementForm, name="AddLCDC_ManagementForm"),

    path('ViewAllStudents', views.ViewAllStudents, name="ViewAllStudents"),
    path('ViewAllTeachers', views.ViewAllTeachers, name="ViewAllTeachers"),
    path('ViewAllCommitteeMembers', views.ViewAllCommitteeMembers, name="ViewAllCommitteeMembers"),
    path('ViewAllLCDC_Management', views.ViewAllLCDC_Management, name="ViewAllLCDC_Management"),
    path('ViewAllAttendance', views.ViewAllAttendance, name="ViewAllAttendance"),
    path('ViewAllBranches', views.ViewAllBranches, name="ViewAllBranches"),
    path('ViewAllUsers', views.ViewAllUsers, name="ViewAllUsers"),

    path('deleteStudent/<int:id>', views.deleteStudent, name='deleteStudent'),
    path('deleteTeacher/<int:id>', views.deleteTeacher, name='deleteTeacher'),
    path('deleteCommitteeMember/<int:id>', views.deleteCommitteeMember, name='deleteCommitteeMember'),
    path('deleteLCDC_Management/<int:id>', views.deleteLCDC_Management, name='deleteLCDC_Management'),
    path('deleteUser/<int:id>', views.deleteUser, name='deleteUser'),
    
    path('updateStudent/<int:id>', views.updateStudent, name='updateStudent'),
    path('updateTeacher/<int:id>', views.updateTeacher, name='updateTeacher'), 
    path('updateCommitteeMember/<int:id>', views.updateCommitteeMember, name='updateCommitteeMember'), 
    path('updateLCDC_Management/<int:id>', views.updateLCDC_Management, name='updateLCDC_Management'),
    path('ViewAttendance/<int:id>', views.ViewAttendance, name='ViewAttendance'),
]