from django.shortcuts import render
from django.http import HttpResponse
from datetime import date, datetime
from django.shortcuts import render
from .models import Student, Levels, School, Grade
from django.core.files.storage import FileSystemStorage


def levels_to_the_header():
    levels = Levels.objects.all().order_by('id')
    i = 1
    for level in levels:
        if i != len(levels):
            level.period += ' |'
            i += 1
    return levels


def years_old(birth_date_aux):
    today = date.today()
    birth = datetime.strptime(birth_date_aux, '%Y-%m-%d')
    age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    return age


def index(request):
    try:
        students = Student.objects.filter(deleted=False)
        levels_header = levels_to_the_header()
        for student in students:
            student.age = years_old(student.birthDate)
            level_description = Levels.objects.get(id=student.level_id)
            student.level_description = level_description.level
        return render(request, 'index.html', {'students': students, 'levels_header': levels_header})
    except:
        message = 'Something gone wrong. Try again!'
        return render(request, 'successful.html', {'levels_header': levels_header, 'message': message})


def new_student(request):
    try:
        levels_header = levels_to_the_header()
        levels = Levels.objects.all()
        schools = School.objects.all()
        grades = Grade.objects.all()
        return render(request, 'newStudent.html', {'levels': levels, 'grades': grades, 'schools': schools,
                                                   'levels_header': levels_header})
    except:
        message = 'Something gone wrong. Try again!'
        return render(request, 'successful.html', {'levels_header': levels_header, 'message': message})


def add_student(request):
    try:
        levels_header = levels_to_the_header()
        if request.method == 'POST':
            student_name = request.POST['studentName']
            class_option = request.POST.get('classOption', 1)
            gender_male = request.POST.get('male', False)
            gender_female = request.POST.get('female', False)
            birth_date = request.POST.get('birthDate', '2010-04-15')
            grade_option = request.POST.get('gradeOption', 1)
            public_school = request.POST.get('publicSchool', 1)
            lives_in = request.POST['livesIn']
            siblings = request.POST['siblings']
            student_notes = request.POST['studentNotes']
            created_by = request.POST.get('createdBy','admin')

            if gender_male == 'on':
                gender = 'Male'
            elif gender_female == 'on':
                gender = 'Female'
            else:
                gender = 'Unknown'
            picture_path = ''
            if len(request.FILES['pictureFile']) != 0:
                picture_path = request.FILES['pictureFile']
                fs = FileSystemStorage()
                fs.save(picture_path.name, picture_path)

            student_data = Student(name=student_name, level_id=class_option, birthDate=birth_date, livesIn=lives_in,
                                   school=public_school, grade=grade_option, siblings=siblings,
                                   picture=picture_path.name, notes=student_notes, createdAt=datetime.now(),
                                   modifiedAt=datetime.now(), createdBy=created_by, gender=gender)
            student_data.save()
            message = 'The student was created successfully :)'
            return render(request, 'successful.html', {'levels_header': levels_header, 'message': message})
        else:
            message = 'Something gone wrong. Try again!'
            return render(request, 'successful.html', {'levels_header': levels_header, 'message': message})
    except:
        message = 'Something gone wrong. Try again!'
        return render(request, 'successful.html', {'levels_header': levels_header, 'message': message})


def edit_student(request):
    #try:
        levels_header = levels_to_the_header()
        if request.method == 'POST':
            student = Student.objects.get(id=request.POST['studentId'])
            student.name = request.POST['studentName']
            student.level_id = request.POST['classOption']
            student.birthDate = request.POST.get('birthDate', '2010-04-15')
            student.grade = request.POST['gradeOption']
            student.school = request.POST['publicSchool']
            student.livesIn = request.POST['livesIn']
            student.siblings = request.POST['siblings']
            student.notes = request.POST['studentNotes']
            student.modifiedAt = datetime.now()

            gender_male = request.POST.get('male', False)
            gender_female = request.POST.get('female', False)
            if gender_male == 'on':
                student.gender = 'Male'
            elif gender_female == 'on':
                student.gender = 'Female'
            else:
                student.gender = 'Unknown'

            # TODO change the name of the file imported to a guid to be sure that picture's name never repeats

            if len(request.FILES['pictureFile']) != 0:
                picture_path = request.FILES['pictureFile']
                fs = FileSystemStorage()
                fs.save(picture_path.name, picture_path)
                student.picture = picture_path.name

            student.save()
            message = 'The student was updated successfully :)'
            return render(request, 'successful.html', {'levels_header': levels_header, 'message': message})
        else:
            message = 'Something gone wrong. Try again!'
            return render(request, 'successful.html', {'levels_header': levels_header, 'message': message})

    #except:
    #    message = 'Something gone wrong. Try again!'
    #    return render(request, 'successful.html', {'levels_header': levels_header, 'message': message})


def information(request):
    return HttpResponse('Information')


def successful(request):
    levels_header = levels_to_the_header()
    message = 'The student was created successfully :)'
    return render(request, 'successful.html', {'levels_header': levels_header, 'message': message})


def student_info(request, student_id):
    try:
        context = {student_id: student_id}
        levels_header = levels_to_the_header()
        levels = Levels.objects.all()
        student = Student.objects.get(id=student_id)
        schools = School.objects.all()
        grades = Grade.objects.all()

        return render(request, 'studentInfo.html', {'levels': levels, 'student': student, 'grades': grades,
                                                    'schools': schools, 'levels_header': levels_header}, context)
    except:
        message = 'Something gone wrong. Try again!'
        return render(request, 'successful.html', {'levels_header': levels_header, 'message': message})