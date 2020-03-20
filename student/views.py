from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import Student, Levels, School, Grade
from django.core.files.storage import FileSystemStorage


# Create your views here.
def index(request):
    students = Student.objects.all()
    levels = Levels.objects.all()
    i = 1
    for level in levels:
        if i != len(levels):
            level.period += ' |'
            i += 1
    return render(request, 'index.html', {'students': students, 'levels': levels})


def new_student(request):
    levels = Levels.objects.all()
    schools = School.objects.all()
    grades = Grade.objects.all()
    return render(request, 'newStudent.html', {'levels': levels, 'grades': grades, 'schools': schools})


def new_form_submission(request):
    levels = Levels.objects.all()
    student_name = request.POST['studentName']
    class_option = request.POST['classOption']
    gender_male = request.POST.get('male', False)
    gender_female = request.POST.get('female', False)
    birth_date = request.POST.get('birthDate', '2010-04-15')
    grade_option = request.POST['gradeOption']
    public_school = request.POST['publicSchool']
    lives_in = request.POST['livesIn']
    siblings = request.POST['siblings']
    student_notes = request.POST['studentNotes']
    picture_path = request.FILES['pictureFile']

    if gender_male == 'on':
        gender = 'Male'
    elif gender_female == 'on':
        gender = 'Female'
    else:
        gender = 'Unknown'

    #TODO change the name of the file imported to a guid to be sure that picture's name never repeats

    fs = FileSystemStorage()
    fs.save(picture_path.name, picture_path)

    student_data = Student(name=student_name, level_id=class_option, birthdate=birth_date, livesin=lives_in,
                           school=public_school, grade=grade_option, siblings=siblings, picture=picture_path.name,
                           notes=student_notes)
    student_data.save()

    return render(request, 'successful.html', {'levels': levels})


def information(request):
    return HttpResponse('Information')


def successful(request):
    levels = Levels.objects.all()
    return render(request, 'successful.html', {'levels': levels})


def student_info(request):
    levels = Levels.objects.all()
    student = Student.objects.get(id=1)

    levels_aux = Levels.objects.get(id=student.level_id)

    student.level_class = levels_aux.level
    student.level_period = levels_aux.period

    return render(request, 'studentInfo.html', {'levels': levels, 'student': student})
