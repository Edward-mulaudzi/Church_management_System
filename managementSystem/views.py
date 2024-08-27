from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import *
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.template import loader
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model
import collections

global current_date
current_date = datetime.date.today().strftime("%Y-%m-%d")
    

def logged_in_user_function(request):
    global logged_in_user
    if request.user.is_superuser:
        logged_in_user="superuser"
    elif request.user.is_admin:
        logged_in_user="admin"
    elif request.user.is_user:
        logged_in_user="user"

def checkIfDateAlreadyExist(request, date):
    attendance_dates = Attendance_date.objects.filter(branch=request.user.branch)
    for attendance_date in attendance_dates:
        if attendance_date.date == date:
            return True   
    return False

def index(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            
            if user is not None:
                login(request,user)
                return redirect(home)
            else:
                messages.error(request, "nvalid credentials!")
        else:
            messages.error(request, "error validating form!")
    return render(request, "index.html",{'form':form})

def Logout(request):
    logout(request)
    return redirect(index)

@login_required
def SuperuserMonitoringTool(request,id):
    logged_in_user_function(request)
    branch = church_branch.objects.get(id=id)
    students = Role.objects.filter(role='Learner',branch=branch)
    students_count = Role.objects.filter(role='Learner',branch=branch).count()
    committee_members = Role.objects.filter(role='Committee',branch=branch)
    committee_members_count = Role.objects.filter(role='Committee',branch=branch).count()
    return render(request, "MonitoringTool.html",{
        'students':students,
        'students_count': students_count,
        'committee_members':committee_members,
        'committee_members_count': committee_members_count,
        'logged_in_user':logged_in_user
        })

@login_required
def home(request):
    logged_in_user_function(request)
    branch =request.user.branch
    students_count = Role.objects.filter(role='Learner',branch=request.user.branch).count()
    teachers_count = Role.objects.filter(role='Teacher',branch=request.user.branch).count()
    committee_members_count = Role.objects.filter(role='Committee',branch=request.user.branch).count()
    attendance_list_count = Attendance_List.objects.filter(branch=request.user.branch).count()
    LCDC_Management_count = Role.objects.filter(role='LCDC_Management',branch=request.user.branch).count()
    return render(request, "home.html",{
        'logged_in_user':logged_in_user,
        'students_count':students_count,
        'teachers_count':teachers_count,
        'committee_members_count':committee_members_count,
        'attendance_list_count':attendance_list_count,
        'LCDC_Management_count':LCDC_Management_count,
        'branch':branch
        })

########################################################################################################################################################
# STUDENT VIEWS
##############################################################################################################

@login_required
def AddStudentForm(request):
    logged_in_user_function(request)
    return render(request, "student/AddStudentForm.html",{'logged_in_user':logged_in_user})

@login_required
def AddStudent(request):
    logged_in_user_function(request)
    if request.method == 'POST':
        full_name = request.POST['full_name']
        gender= request.POST['gender']
        grade= request.POST['grade']
        id_number= request.POST['id_number']
        place= request.POST['place']
        parent_contact= request.POST['parent_contact']
        institution_name= request.POST['institution_name']
        field_of_study= request.POST['field_of_study']
        check_box =request.POST.get('checkbox')

        new_student= church_member(
            full_name = full_name,
            gender = gender,
            grade = grade,
            id_number = id_number,
            place = place,
            parent_contact = parent_contact,
            institution_name=institution_name,
            field_of_study=field_of_study,
            branch=request.user.branch
        )
        new_student.save()
        role = Role(id=None,role="Learner",structure='Sunday School',member=new_student, branch=request.user.branch)
        role.save()
        messages.success(request, "Student was successfully created!")
        if check_box == "checked":
            return render(request, "student/AddStudentForm.html",{'logged_in_user':logged_in_user})
        else:
            return HttpResponseRedirect(reverse('ViewAllStudents'))

@login_required
def ViewAllStudents(request):
    logged_in_user_function(request)
    students = Role.objects.filter(role='Learner',branch=request.user.branch)
    students_count = Role.objects.filter(role='Learner',branch=request.user.branch).count()
    return render(request, "student/ViewAllStudents.html",{
        'students':students,
        'students_count': students_count,
        'logged_in_user':logged_in_user
    })

@login_required  
def updateStudent(request,id):
    logged_in_user_function(request)
    studentUpdate = church_member.objects.get(id=id)
    if request.method == 'POST':
        full_name = request.POST['full_name']
        gender= request.POST['gender']
        grade= request.POST['grade']
        id_number= request.POST['id_number']
        place= request.POST['place']

        studentUpdate.full_name = full_name
        studentUpdate.gender = gender
        studentUpdate.grade = grade
        studentUpdate.id_number = id_number
        studentUpdate.place = place
        studentUpdate.save()
        messages.success(request, "Student was successfully updated!")
        return HttpResponseRedirect(reverse("ViewAllStudents"))
    return render(request, "student/updateStudent.html",{
        'studentUpdate': studentUpdate,
        'logged_in_user':logged_in_user
    })

@login_required
def deleteStudent(request,id):
    logged_in_user_function(request)
    student = church_member.objects.get(id=id)
    if request.method == 'POST':
        student.delete()
        messages.info(request, "Student was successfully Deleted!")
        return HttpResponseRedirect(reverse('ViewAllStudents'))
    return render(request, "student/deleteStudent.html",{'logged_in_user':logged_in_user})

##############################################################################################################################################################
# TEACHER VIEWS
###############################################################################################################################################################

@login_required
def AddTeacherForm(request):
    logged_in_user_function(request)
    return render(request, "teacher/AddTeacherForm.html",{'logged_in_user':logged_in_user})

@login_required
def AddTeacher(request):
    logged_in_user_function(request)
    if request.method == 'POST':
        full_name = request.POST['full_name']
        gender= request.POST['gender']
        id_number= request.POST['id_number']
        place= request.POST['place']
        check_box =request.POST.get('checkbox')

        new_teacher= church_member(
            full_name = full_name,
            gender = gender,
            id_number = id_number,
            place = place,
            branch=request.user.branch
        )
        new_teacher.save()
        messages.success(request, "Teacher was successfully created!")
        role = Role(id=None,role="Teacher",structure='Sunday School',member=new_teacher,branch=request.user.branch)
        role.save()
        if check_box == "checked":
            return render(request, "teacher/AddTeacherForm.html",{'logged_in_user':logged_in_user})
        else:
            return HttpResponseRedirect(reverse('ViewAllTeachers'))

@login_required
def ViewAllTeachers(request):
    logged_in_user_function(request)
    teachers = Role.objects.filter(role='Teacher',branch=request.user.branch)
    teachers_count = Role.objects.filter(role='Teacher',branch=request.user.branch).count()
    return render(request, "teacher/ViewAllTeachers.html",{
        'teachers':teachers,
        'teachers_count': teachers_count,
        'logged_in_user':logged_in_user
    })

@login_required
def updateTeacher(request,id):
    logged_in_user_function(request)
    teacherUpdate = church_member.objects.get(id=id)
    if request.method == 'POST':
        full_name = request.POST['full_name']
        gender= request.POST['gender']
        id_number= request.POST['id_number']
        place= request.POST['place']

        teacherUpdate.full_name = full_name
        teacherUpdate.gender = gender
        teacherUpdate.id_number = id_number
        teacherUpdate.place = place
        teacherUpdate.save()
        messages.success(request, "Teacher was successfully created!")
        return HttpResponseRedirect(reverse("ViewAllTeachers"))
    return render(request, "teacher/updateTeacher.html",{
        'teacherUpdate': teacherUpdate,
        'logged_in_user':logged_in_user
    })

@login_required
def deleteTeacher(request,id):
    logged_in_user_function(request)
    teacher = church_member.objects.get(id=id)
    if request.method == 'POST':
        teacher.delete()
        messages.info(request, "Teacher was successfully Deleted!")
        return HttpResponseRedirect(reverse('ViewAllTeachers'))
    return render(request, "teacher/deleteTeacher.html",{'logged_in_user':logged_in_user})

########################################################################################################
# COMMITTEE VIEWS
##########################################################################################################

@login_required
def AddCommitteeMemberForm(request):
    logged_in_user_function(request)
    return render(request, "committee/AddCommitteeMemberForm.html",{'logged_in_user':logged_in_user})

@login_required
def AddCommitteeMember(request):
    logged_in_user_function(request)
    if request.method == 'POST':
        full_name = request.POST['full_name']
        gender= request.POST['gender']
        id_number= request.POST['id_number']
        place= request.POST['place']
        check_box =request.POST.get('checkbox')

        new_committe_member= church_member(
            full_name = full_name,
            gender = gender,
            id_number = id_number,
            place = place,
            branch=request.user.branch
        )
        new_committe_member.save()
        role = Role(id=None,role="Committee",structure='Sunday School',member=new_committe_member,branch=request.user.branch)
        role.save()
        messages.success(request, "Committee Member was successfully created!")
        if check_box == "checked":
            return render(request, "committee/AddCommitteeMemberForm.html",{'logged_in_user':logged_in_user})
        else:
            return HttpResponseRedirect(reverse('ViewAllCommitteeMembers'))

@login_required
def ViewAllCommitteeMembers(request):
    logged_in_user_function(request)
    committee_members = Role.objects.filter(role='Committee',branch=request.user.branch)
    committee_members_count = Role.objects.filter(role='Committee',branch=request.user.branch).count()
    return render(request, "committee/ViewAllCommitteeMembers.html",{
        'committee_members':committee_members,
        'committee_members_count': committee_members_count,
        'logged_in_user':logged_in_user
    })

@login_required
def updateCommitteeMember(request,id):
    logged_in_user_function(request)
    committee_member_update = church_member.objects.get(id=id)
    if request.method == 'POST':
        full_name = request.POST['full_name']
        gender= request.POST['gender']
        id_number= request.POST['id_number']
        place= request.POST['place']

        committee_member_update.full_name = full_name
        committee_member_update.gender = gender
        committee_member_update.id_number = id_number
        committee_member_update.place = place
        committee_member_update.save()
        messages.success(request, "Committee Member was successfully Updated!")
        return HttpResponseRedirect(reverse("ViewAllCommitteeMembers"))
    return render(request, "committee/updateCommitteeMember.html",{
        'committee_member_update': committee_member_update,
        'logged_in_user':logged_in_user
    })

@login_required
def deleteCommitteeMember(request,id):
    logged_in_user_function(request)
    committee_member = church_member.objects.get(id=id)
    if request.method == 'POST':
        committee_member.delete()
        messages.info(request, "Committee Member was successfully deleted!")
        return HttpResponseRedirect(reverse('ViewAllCommitteeMembers'))
    return render(request, "committee/deleteCommitteeMember.html",{'logged_in_user':logged_in_user})

##########################################################################################################
# ATTENDANCE
##########################################################################################################

@login_required
def StartAttendance(request):
    logged_in_user_function(request)
    church_members= Role.objects.filter(branch=request.user.branch)
    attendance_date_count = Attendance_date.objects.filter(branch=request.user.branch).count()
    if filter_date ==current_date:
        show_date = "Today"
    else:
        show_date = filter_date
    if attendance_date_count==0:
        for member in church_members:
            add_to_attendance_table= Attendance(date=filter_date, attendance="Absent", structure="Sunday School",member=member.member,role=member.role,branch=request.user.branch )
            add_to_attendance_table.save() 
            messages.success(request, "Attendance Register was successfully created!")
        add_attendance_date= Attendance_date(date=filter_date,branch=request.user.branch)
        add_attendance_date.save()
    else:
        if checkIfDateAlreadyExist(request, filter_date)==False:
            for member in church_members:
                add_to_attendance_table= Attendance(date=filter_date, attendance="Absent", structure="Sunday School",member=member.member,role=member.role,branch=request.user.branch )
                add_to_attendance_table.save() 
            add_attendance_date= Attendance_date(date=filter_date,branch=request.user.branch)
            add_attendance_date.save()
            messages.success(request, "Attendance Register was successfully created!")
    return render(request, "StartAttendance.html",{
        'attendance_members':Attendance.objects.filter(date=filter_date,branch=request.user.branch),
        'date':show_date,
        'current_date':current_date,
        'logged_in_user':logged_in_user
    })

@login_required
def AttendanceList(request):
    logged_in_user_function(request)
    attendance_dates = Attendance_date.objects.filter(branch=request.user.branch)
    attendance_list = Attendance_List.objects.filter(branch=request.user.branch)
    attendance_list_count = Attendance_List.objects.filter(branch=request.user.branch).count()
    if attendance_list_count>0:
        attendance_list.delete()
    for attendance_date in attendance_dates:
        students_present = Attendance.objects.filter(date=attendance_date,attendance="Present",role="Learner",branch=request.user.branch).count()
        students_absent = Attendance.objects.filter(date=attendance_date,attendance="Absent",role="Learner",branch=request.user.branch).count()
        students_total = Attendance.objects.filter(date=attendance_date,role="Learner",branch=request.user.branch).count()
        teachers_present = Attendance.objects.filter(date=attendance_date,attendance="Present",role="Teacher",branch=request.user.branch).count()
        teachers_absent = Attendance.objects.filter(date=attendance_date,attendance="Absent",role="Teacher",branch=request.user.branch).count()
        teachers_total = Attendance.objects.filter(date=attendance_date,role="Teacher",branch=request.user.branch).count()
        committee_present = Attendance.objects.filter(date=attendance_date,attendance="Present",role="Committee",branch=request.user.branch).count()
        committee_absent = Attendance.objects.filter(date=attendance_date,attendance="Absent",role="Committee",branch=request.user.branch).count()
        committee_total = Attendance.objects.filter(date=attendance_date,role="Committee",branch=request.user.branch).count()
        health_present = Attendance.objects.filter(date=attendance_date,attendance="Present",role="Health",branch=request.user.branch).count()
        health_absent = Attendance.objects.filter(date=attendance_date,attendance="Absent",role="Health",branch=request.user.branch).count()
        health_total = Attendance.objects.filter(date=attendance_date,role="Health",branch=request.user.branch).count()
        LCDC_Management_present = Attendance.objects.filter(date=attendance_date,attendance="Present",role="LCDC_Management",branch=request.user.branch).count()
        LCDC_Management_absent = Attendance.objects.filter(date=attendance_date,attendance="Absent",role="LCDC_Management",branch=request.user.branch).count()
        LCDC_Management_total = Attendance.objects.filter(date=attendance_date,role="LCDC_Management",branch=request.user.branch).count()

        list =Attendance_List(
            date=attendance_date,
            students_present=students_present,
            students_absent=students_absent,
            students_total= students_total,
            teachers_present=teachers_present,
            teachers_absent=teachers_absent,
            teachers_total=teachers_total,
            committee_present=committee_present,
            committee_absent=committee_absent,
            committee_total=committee_total,
            health_present=health_present,
            health_absent=health_absent,
            health_total=health_total,
            LCDC_Management_present=LCDC_Management_present,
            LCDC_Management_absent=LCDC_Management_absent,
            LCDC_Management_total=LCDC_Management_total,
            branch=request.user.branch
        )
        list.save()
    return render(request, "AttendanceList.html",{
        'attendance_list_count': Attendance_List.objects.filter(branch=request.user.branch).count(),
        'attendance_list': Attendance_List.objects.filter(branch=request.user.branch).order_by('-date').values(),
        'current_date':current_date,
        'logged_in_user':logged_in_user
    })

@login_required
def ViewAttendance(request,id):
    logged_in_user_function(request)
    global attendance_date
    
    attendance = Attendance_List.objects.get(id=id)
    attendance_date = attendance.date

    if attendance_date ==current_date:
        show_date = "Today"
    else:
        show_date = attendance_date

    
    if request.method == 'POST':
        attendance_members = Attendance.objects.filter(branch=request.user.branch)
        attendance_status = request.POST.getlist('checkAttendance[]')

        status_list = Attendance.objects.filter(branch=request.user.branch,attendance="Present")
        previous_attendance_status=[]
        for i in status_list:
            previous_attendance_status.append(str(i.id))

        if(collections.Counter(previous_attendance_status)==collections.Counter(attendance_status)):
            messages.error(request, "No changes made!")
            print(previous_attendance_status)
            print(attendance_status)

        else:
            for member in attendance_members:
                if str(member.id) in attendance_status:
                    attendance_member = Attendance.objects.get(id=member.id)
                    attendance_member.attendance="Present"
                    attendance_member.save()
                else:
                    attendance_member = Attendance.objects.get(id=member.id)
                    attendance_member.attendance="Absent"
                    attendance_member.save()
            messages.success(request, "Attendance Status was successfully updated!")
           

        return render(request, "ViewAttendance.html",{
            'attendance_members':Attendance.objects.filter(date=attendance_date,branch=request.user.branch),
            'date':show_date,
            'logged_in_user':logged_in_user
        })
    return render(request, "ViewAttendance.html",{
        'attendance_members':Attendance.objects.filter(date=attendance_date,branch=request.user.branch),
        'date':show_date,
        'logged_in_user':logged_in_user
    })

@login_required
def SelectAttendanceDate(request):
    logged_in_user_function(request)
    global filter_date
    if request.method == 'POST':
        date =request.POST['date']
        filter_date=date
        if checkIfDateAlreadyExist(request, date) == True:
            return render(request, "AttendanceList.html",{
                'attendance_list_count': "1",
                'attendance_list': Attendance_List.objects.filter(date=date,branch=request.user.branch),
                'current_date':current_date,
                'logged_in_user':logged_in_user
            })
        else:
            return HttpResponseRedirect(reverse("StartAttendance"))

@login_required
def ViewAllAttendance(request):
    church_members= Role.objects.all()
    attendance_date_count = Attendance_date.objects.filter(branch=request.user.branch).count()
    if request.method == 'POST':
        date =request.POST['date']
        if attendance_date_count==0:
            for member in church_members:
                add_to_attendance_table= Attendance(date=date, attendance="Absent", structure="Sunday School",member=member.member,role=member.role,)
                add_to_attendance_table.save() 
            add_attendance_date= Attendance_date(date=date)
            add_attendance_date.save()
        else:
            if checkIfDateAlreadyExist(request, date)==False:
                for member in church_members:
                    add_to_attendance_table= Attendance(date=date, attendance="Absent", structure="Sunday School",member=member.member,role=member.role )
                    add_to_attendance_table.save() 
                add_attendance_date= Attendance_date(date=date)
                add_attendance_date.save()
        return render(request, "StartAttendance.html",{
            'attendance_members':Attendance.objects.filter(date=date),
            'date':date,
            'current_date':current_date

        })
    attendance_members =Attendance.objects.filter(date=filter_date)
    return render(request, "StartAttendance.html",{
        'attendance_members':attendance_members,
        'date':filter_date,
        'current_date':current_date
    })

############################################################################################################################
# SUPERUSER
#############################################################################################################################

@login_required
def AddChurchBranchForm(request):
    logged_in_user_function(request)
    if request.user.is_superuser:
        return render(request, "AddChurchBranchForm.html",{'logged_in_user':logged_in_user})
    return reverse('index')

@login_required
def AddChurchBranch(request):
    logged_in_user_function(request)
    if request.user.is_superuser:
        if request.method == 'POST':
            branch_name = request.POST['branch_name']
            fb_number= request.POST['fb_number']
            branch_head= request.POST['branch_head']
            centre_name= request.POST['centre_name']
            check_box =request.POST.get('checkbox')

            new_branch= church_branch(
                branch_name = branch_name,
                fb_number = fb_number,
                branch_head = branch_head,
                centre_name = centre_name
            )
            new_branch.save()
            if check_box == "checked":
                return render(request, "AddChurchBranchForm.html",{'logged_in_user':logged_in_user})
            else:
                return HttpResponseRedirect(reverse('ViewAllBranches'))
    return reverse('index')

@login_required
def ViewAllBranches(request):
    logged_in_user_function(request)
    if request.user.is_superuser:
        church_branches = church_branch.objects.all()
        church_branches_count = church_branch.objects.all().count()
        return render(request, "ViewAllBranches.html",{
            'church_branches':church_branches,
            'church_branches_count': church_branches_count,
            'logged_in_user':logged_in_user
        })

@login_required
def AddUser(request):
    if request.user.is_superuser:
        logged_in_user_function(request)
        if request.method == 'POST':
            form = AddUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                messages.success(request, "User was successfully created!")
                return redirect(index)
            else:
                messages.error(request, "Form is not valid!")
        else:
            form = AddUserForm()
        return render(request, "users/AddUser.html",{'form':form,'logged_in_user':logged_in_user})
   
    elif request.user.is_admin:
        logged_in_user_function(request)
        if request.method == 'POST':
            form = AdminAddUserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.branch = request.user.branch
                messages.success(request, "User was successfully created!")
                user.save()
                return redirect(index)
            else:
                messages.error(request, "Form is not valid!")
        else:
            form = AdminAddUserForm()
        return render(request, "users/AddUser.html",{'form':form,'logged_in_user':logged_in_user})
    else:
        return redirect(index)

@login_required
def deleteUser(request,id):
    logged_in_user_function(request)
    user = User.objects.get(id=id)
    if request.method == 'POST':
        user.delete()
        return HttpResponseRedirect(reverse('ViewAllUsers'))
    return render(request, "users/deleteUser.html",{'logged_in_user':logged_in_user})

@login_required
def ViewAllUsers(request):
    logged_in_user_function(request)
    if request.user.is_superuser:
        users = User.objects.all()
        users_count = User.objects.all().count()
        return render(request, "users/ViewAllUsers.html",{
            'users':users,
            'users_count': users_count,
            'logged_in_user':logged_in_user
        })
    else:
        users = User.objects.filter(branch=request.user.branch)
        users_count = User.objects.filter(branch=request.user.branch).count()
        return render(request, "users/ViewAllUsers.html",{
            'users':users,
            'users_count': users_count,
            'logged_in_user':logged_in_user
        })

############################################################################################################
# LCDC MANAGEMENT
#################################################################################################################

@login_required
def AddLCDC_ManagementForm(request):
    logged_in_user_function(request)
    return render(request, "LCDC_Management/AddLCDC_ManagementForm.html", {'logged_in_user':logged_in_user})

@login_required
def AddLCDC_Management(request):
    logged_in_user_function(request)
    if request.method == 'POST':
        full_name = request.POST['full_name']
        gender= request.POST['gender']
        id_number= request.POST['id_number']
        place= request.POST['place']
        check_box =request.POST.get('checkbox')

        new_LCDC_Management= church_member(
            full_name = full_name,
            gender = gender,
            id_number = id_number,
            place = place,
            branch=request.user.branch
        )
        new_LCDC_Management.save()
        role = Role(id=None,role="LCDC_Management",structure='Sunday School',member=new_LCDC_Management)
        role.save()
        if check_box == "checked":
            return render(request, "LCDC_Management/AddLCDC_ManagementForm.html",{'logged_in_user':logged_in_user})
        else:
            return HttpResponseRedirect(reverse('ViewAllLCDC_Management'))

@login_required
def ViewAllLCDC_Management(request):
    logged_in_user_function(request)
    LCDC_Management = Role.objects.filter(role='LCDC_Management',branch=request.user.branch)
    LCDC_Management_count = Role.objects.filter(role='LCDC_Management',branch=request.user.branch).count()
    return render(request, "LCDC_Management/ViewAllLCDC_Management.html",{
        'LCDC_Management':LCDC_Management,
        'LCDC_Management_count': LCDC_Management_count,
        'logged_in_user':logged_in_user,
        'logged_in_user':logged_in_user
    }) 

@login_required
def updateLCDC_Management(request,id):
    logged_in_user_function(request)
    LCDC_Management_update = church_member.objects.get(id=id)
    if request.method == 'POST':
        full_name = request.POST['full_name']
        gender= request.POST['gender']
        id_number= request.POST['id_number']
        place= request.POST['place']

        LCDC_Management_update.full_name = full_name
        LCDC_Management_update.gender = gender
        LCDC_Management_update.id_number = id_number
        LCDC_Management_update.place = place
        LCDC_Management_update.save()
        return HttpResponseRedirect(reverse("ViewAllLCDC_Management"))
    return render(request, "LCDC_Management/updateLCDC_Management.html",{
        'LCDC_Management_update': LCDC_Management_update,
        'logged_in_user':logged_in_user,
        'logged_in_user':logged_in_user
    })

@login_required
def deleteLCDC_Management(request,id):
    logged_in_user_function(request)
    LCDC_Management = church_member.objects.get(id=id)
    if request.method == 'POST':
        LCDC_Management.delete()
        return HttpResponseRedirect(reverse('ViewAllLCDC_Management'))
    return render(request, "LCDC_Management/deleteLCDC_Management.html", {'logged_in_user':logged_in_user})

################################################################################################################