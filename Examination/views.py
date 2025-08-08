from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Exam, Question, StudentExam, StudentAnswer,ExamFileMessage
from .forms import StudentAnswerForm,ExamFileMessageForm
from django.utils import timezone
from users.models import Profile  # <- adjust as needed

@login_required
def exam_list(request):
    profile = request.user.users_profile  # or .profile per your related_name
    # Get all exams for which the student has a submission
    submitted_exam_ids = StudentExam.objects.filter(student=profile).values_list('exam_id', flat=True)
    # Only show exams NOT in that set
    exams = Exam.objects.exclude(id__in=submitted_exam_ids)
    return render(request, 'Examination/exam_list.html', {'exams': exams})


@login_required
def submitted_exam_list(request):
    profile = request.user.users_profile  # or .profile as appropriate
    student_exams = StudentExam.objects.select_related('exam').filter(student=profile)
    # Prepare a list of dicts with both exam and student_exam
    exam_data = [
        {
            'exam': se.exam,
            'student_exam': se
        } for se in student_exams
    ]
    return render(request, 'Examination/submitted_exam_list.html', {'exam_data': exam_data})


@login_required
def exam_students_list(request, exam_id):
    # Only allow teachers
    profile = request.user.users_profile
    if profile.role != 'teacher':
        return HttpResponse("You are not authorized to view this page.", status=403)
    exam = get_object_or_404(Exam, id=exam_id)
    # Get all student profiles who took this exam
    student_exams = StudentExam.objects.filter(exam=exam).select_related('student')
    students = [se.student for se in student_exams]
    return render(request, 'Examination/exam_students_list.html', {
        'exam': exam,
        'students': students,
    })
# Take exam
@login_required
def take_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    student_profile = request.user.users_profile  # or request.user.profile depending on your related_name
    student_exam, created = StudentExam.objects.get_or_create(student=student_profile, exam=exam)

    if request.method == 'POST':
        for question in exam.questions.all():
            answer_text = request.POST.get(f'answer_{question.id}', '')
            StudentAnswer.objects.update_or_create(
                student_exam=student_exam,
                question=question,
                defaults={'answer_text': answer_text}
            )
        return redirect('exam_submitted_confirmation')

    answers = {a.question_id: a for a in student_exam.answers.all()}
    return render(request, 'Examination/take_exam.html', {
        'exam': exam,
        'answers': answers
    })
@login_required
def submit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    student = request.user.student  # adjust if you're using another related name

    student_exam = get_object_or_404(StudentExam, exam=exam, student=student)

    if request.method == 'POST':
        # Save answers logic here...

        student_exam.submitted = True      # ✅ This is what was missing
        student_exam.submitted_at = timezone.now()  # Optional but good
        student_exam.save()

        return redirect('exam_submitted_confirmation')  # or any success page

    return render(request, 'Examination/take_exam.html', {
        'exam': exam,
        'student_exam': student_exam
    })

@login_required
def exam_submitted(request, student_exam_id):
    student_exam = get_object_or_404(StudentExam, id=student_exam_id)
    # student_exam.graded = True
    student_exam.submitted = True
    exam = student_exam.exam
    answers = StudentAnswer.objects.filter(student_exam=student_exam).select_related('question')
    return render(request, 'Examination/exam_submitted.html', {
        'exam': exam,
        'student_exam': student_exam,
        'answers': answers,
    })
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def exam_submitted_confirmation(request):
    return render(request, 'Examination/exam_submitted_confirmation.html')

# Teacher grades exam
@login_required
def grade_exam(request, student_exam_id):
    student_exam = get_object_or_404(StudentExam, id=student_exam_id)
    profile = request.user.users_profile  # or request.user.profile depending on your related_name
    if profile.role != 'teacher':
        return HttpResponse("You are not authorized to grade exams.", status=403)
    if request.method == 'POST':
        total = 0
        for answer in student_exam.answers.all():
            marks = int(request.POST.get(f'marks_{answer.id}', 0))
            answer.marks_awarded = marks
            answer.checked_by = profile  # <--- fixed
            answer.checked_at = timezone.now()
            answer.save()
            total += marks
        student_exam.total_marks = total
        student_exam.graded = True
        student_exam.submitted = True
        student_exam.save()
        return redirect('exam_graded', student_exam.id)
    return render(request, 'Examination/grade_exam.html', {
        'student_exam': student_exam,
    })

@login_required
def exam_graded(request, student_exam_id):
    return render(request, 'Examination/exam_graded.html', {'student_exam_id': student_exam_id})

@login_required
def submitted_exams(request):
    exams = StudentExam.objects.filter(graded=False)
    
    return render(request, 'Examination/submitted_exams.html', {'exams': exams})

@login_required
def submissions(request):
    if request.user.username != "Mwalimu":
        return render(request, 'Examination/404.html', status=403)

    submissions = StudentExam.objects.filter(submitted=True).select_related('student__user', 'exam')
    
    submission_data = []
    for submission in submissions:
        answers = StudentAnswer.objects.filter(student_exam=submission).select_related('question')
        total_awarded = sum((ans.marks_awarded or 0) for ans in answers)
        total_possible = sum((ans.question.max_marks or 0) for ans in answers)
        submission_data.append({
            'submission': submission,
            'answers': answers,
            'total_awarded': total_awarded,
            'total_possible': total_possible,
        })

    return render(request, 'Examination/submissions.html', {
        'submission_data': submission_data
    })


def exam_leaderboard(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    # Get all graded StudentExams for this exam, order by total_marks descending
    student_exams = StudentExam.objects.filter(exam=exam, graded=True).select_related('student__user').order_by('-total_marks')
    return render(request, 'Examination/exam_leaderboard.html', {
        'exam': exam,
        'student_exams': student_exams,
    })



@login_required
def send_exam_file(request, exam_id, student_id):
    exam = get_object_or_404(Exam, id=exam_id)
    receiver = get_object_or_404(Profile, id=student_id)
    sender = request.user.users_profile  # or .profile

    # Only allow teachers to send files
    if sender.role != 'teacher':
        return HttpResponse("Unauthorized", status=403)

    if request.method == 'POST':
        form = ExamFileMessageForm(request.POST, request.FILES)
        if form.is_valid():
            file_msg = form.save(commit=False)
            file_msg.exam = exam
            file_msg.sender = sender
            file_msg.receiver = receiver
            file_msg.save()
            return redirect('exam_students_list', exam_id=exam.id)
    else:
        form = ExamFileMessageForm()

    return render(request, 'Examination/send_exam_file.html', {
        'form': form,
        'exam': exam,
        'receiver': receiver,
    })

@login_required
def exam_received_files(request, exam_id):
    user_profile = request.user.users_profile
    exam = get_object_or_404(Exam, id=exam_id)
    files = ExamFileMessage.objects.filter(exam=exam, receiver=user_profile)
    return render(request, 'Examination/exam_received_files.html', {
        'exam': exam,
        'files': files,
    })