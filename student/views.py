from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from datetime import date, datetime
from django.shortcuts import render
from .models import Student, Levels, School, Grade
from django.core.files.storage import FileSystemStorage

# TODO: Everytime some student change the level we need to update one table that allow us to know how long the student was in the same level.
# TODO: Create a page to attendance list where we will see all the students from a class and we'll be able to check if they are in the class
#TODO: We need to be able to change the attendance list
#TODO: Create graphs where we will see how many students coming for class and in general everyday
#TODO: Update the file to the folder


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
        students = Student.objects.all()
        levels_header = levels_to_the_header()
        level_desc = 'All Students'
        for student in students:
            student.age = years_old(student.birthDate)
            level_description = Levels.objects.get(id=student.level_id)
            student.level_description = level_description.level

        return render(request, 'studentsByClass.html', {'students': students, 'levels_header': levels_header,
                                                        'level_desc': level_desc, 'attendenca': False})
    except:
        message = 'Something gone wrong. Try again!'
        return successful(request=request, message=message)


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
        return successful(request=request, message=message)


def add_student(request):
    # try:
    context = {}
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
        created_by = request.POST.get('createdBy', 'admin')
        picture_path = request.FILES['pictureFile']
        if gender_male == 'on':
            gender = 'Male'
        elif gender_female == 'on':
            gender = 'Female'
        else:
            gender = 'Unknown'

        fs = FileSystemStorage()
        name = fs.save(picture_path.name, picture_path)
        print(picture_path.name)
        print(picture_path)

        context['url'] = fs.url(name)

        student_data = Student(name=student_name, level_id=class_option, birthDate=birth_date, livesIn=lives_in,
                               school=public_school, grade=grade_option, siblings=siblings,
                               picture=name, notes=student_notes, createdAt=datetime.now(),
                               modifiedAt=datetime.now(), createdBy=created_by, gender=gender)

        student_data.save()
        message = 'The student was created successfully :)'
        return successful(request=request, message=message)
    else:
        message = 'Something gone wrong. Try again!'
        return successful(request=request, message=message)


# except:
#    message = 'Something gone wrong. Try again!'
#    return render(request, 'successful.html', {'levels_header': levels_header, 'message': message})


def edit_student(request):
    # try:
    if request.method == 'POST':
        student = Student.objects.get(id=request.POST['studentId'])
        student.name = request.POST['studentName']
        student.level_id = request.POST['classOption']
        student.birthDate = request.POST.get('birthDate', '2010-04-15')
        student.grade = request.POST.get('gradeOption', 13)
        student.school = request.POST.get('publicSchool', 7)
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

        if request.POST['pictureFile']:
            picture_path = request.FILES['pictureFile']
            fs = FileSystemStorage()
            fs.save(picture_path.name, picture_path)
            student.picture = picture_path.name

        student.save()
        message = 'The student was updated successfully :)'
        return successful(request=request, message=message)
    else:
        message = 'Something gone wrong. Try again!'
        return successful(request=request, message=message)


# except:
#    message = 'Something gone wrong. Try again!'
#    return render(request, 'successful.html', {'levels_header': levels_header, 'message': message})


def student_class(request, levelId):
    # try:
    context = {levelId: int(levelId)}
    students = Student.objects.filter(level_id=int(levelId))
    levels_header = levels_to_the_header()
    level_aux = Levels.objects.get(id=int(levelId))
    level_desc = level_aux.level + ' - ' + level_aux.period
    for student in students:
        student.age = years_old(student.birthDate)
        level_description = Levels.objects.get(id=student.level_id)
        student.level_description = level_description.level

    return render(request, 'studentsByClass.html', {'students': students, 'levels_header': levels_header,
                                                    'level_desc': level_desc, 'attendance': True}, context)
    # except:
    #    message = 'Something gone wrong. Try again!'
    #    return successful(request=request, message=message)


def information(request):
    levels_header = levels_to_the_header()
    return render(request, 'information.html', {'levels_header': levels_header})


def settings(request):
    levels_header = levels_to_the_header()
    levels = Levels.objects.all()
    school = School.objects.all()
    grades = Grade.objects.all()
    return render(request, 'settings.html', {'levels_header': levels_header, 'publicschool': school, 'levels': levels,
                                             'grades': grades})


def successful(request, message):
    levels_header = levels_to_the_header()
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
    return successful(request=request, message=message)


def public_school_edit(request, school_id):
    context = {school_id: int(school_id)}
    levels_header = levels_to_the_header()
    school = School.objects.get(id=int(school_id))
    return render(request, 'publicSchool.html', {'school': school, 'levels_header': levels_header, 'description': school.name}, context)


def public_school_add(request):
    levels_header = levels_to_the_header()
    description = 'New Public School'
    return render(request, 'publicSchool.html', {'levels_header': levels_header, 'description': description,
                                                 'new': True})


def school_save(request):
    if request.method == 'POST':
        active = False
        if request.POST.get('active'):
            active = True
        if request.POST['schoolId'] == '':
            public_school = School(name=request.POST['schoolName'], createdBy=request.POST['createdBy'],
                                   createdAt=datetime.now(), modifiedAt=datetime.now(), active=active)
            public_school.save()
            message = 'The public school was created successfully :)'
        else:
            public_school = School.objects.get(id=request.POST['schoolId'])
            public_school.name = request.POST['schoolName']
            public_school.createdBy = request.POST['createdBy']
            public_school.modifiedAt = datetime.now()
            public_school.active = active
            public_school.save()
            message = 'The public school was updated successfully :)'
        return successful(request=request, message=message)
    else:
        message = 'Something goes wrong! Try again :('
        return successful(request=request, message=message)


def grade_edit(request, grade_id):
    context = {grade_id: int(grade_id)}
    levels_header = levels_to_the_header()
    grade = Grade.objects.get(id=int(grade_id))
    return render(request, 'grade.html', {'grade': grade, 'levels_header': levels_header, 'description': grade.name},
                  context)


def grade_add(request):
    levels_header = levels_to_the_header()
    description = "New Public School's Grade"
    return render(request, 'grade.html', {'levels_header': levels_header, 'description': description, 'new': True})


def grade_save(request):
    if request.method == 'POST':
        active = True
        if request.POST['gradeId'] == '':
            grade = Grade(name=request.POST['grade'], createdBy=request.POST['createdBy'],
                                   createdAt=datetime.now(), modifiedAt=datetime.now(), deleted=active)
            grade.save()
            message = "The public school' grade was created successfully :)"
        else:
            grade = Grade.objects.get(id=request.POST['gradeId'])
            grade.name = request.POST['grade']
            grade.createdBy = request.POST['createdBy']
            grade.modifiedAt = datetime.now()
            grade.deleted = active
            grade.save()
            message = "The public school's grade was updated successfully :)"
        return successful(request=request, message=message)
    else:
        message = 'Something goes wrong! Try again :('
        return successful(request=request, message=message)


def level_edit(request, level_id):
    context = {level_id: int(level_id)}
    levels_header = levels_to_the_header()
    level = Levels.objects.get(id=int(level_id))
    return render(request, 'level.html', {'level': level, 'levels_header': levels_header,
                                          'description': level.level + '-' + level.period}, context)


def level_add(request):
    levels_header = levels_to_the_header()
    description = "New Cristina School's Level"
    return render(request, 'level.html', {'levels_header': levels_header, 'description': description, 'new': True})


def level_save(request):
    if request.method == 'POST':
        deleted = False
        status = False
        if request.POST.get('active'):
            status = True
        if request.POST['levelId'] == '':
            level = Levels(level=request.POST['level'], period=request.POST['period'], status=status,
                           createdBy=request.POST['createdBy'], createdAt=datetime.now(),
                           modifiedAt=datetime.now(), deleted=deleted)
            level.save()
            message = "The new level was created successfully :)"
        else:
            level = Levels.objects.get(id=request.POST['levelId'])
            level.level = request.POST['level']
            level.period = request.POST['period']
            level.createdBy = request.POST['createdBy']
            level.modifiedAt = datetime.now()
            level.deleted = deleted
            level.status = status
            level.save()
            message = "The level was updated successfully :)"
        return successful(request=request, message=message)
    else:
        message = 'Something goes wrong! Try again :('
        return successful(request=request, message=message)