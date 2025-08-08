from django.shortcuts import render, get_object_or_404
from .models import Lesson, Quiz
from progress.models import LessonProgress
from progress.models import QuizResult
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
def homepage(request):

    return render(request, 'content/home.html')

# def lesson_list_view(request):
#     """Display a list of all lessons."""
#     lessons = Lesson.objects.all()
#     return render(request, 'content/lesson_list.html', {'lessons': lessons})

def lesson_list_view(request):
    lessons = Lesson.objects.all()

    # Apply filtering based on GET parameters
    if 'q' in request.GET:
        lessons = lessons.filter(topic__icontains=request.GET['q'])

    if 'difficulty' in request.GET:
        lessons = lessons.filter(difficulty_level=request.GET['difficulty'])

    # Sort lessons by topic and difficulty level
    lessons = lessons.order_by('topic', 'difficulty_level')

    paginator = Paginator(lessons, 5)  # 10 lessons per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Retrieve all unique topics
    topics = Lesson.objects.values_list('topic', flat=True).distinct()

    return render(request, 'content/lesson_list.html', {'lessons': lessons, 'topics': topics,'page_obj':page_obj})


@login_required
def lesson_detail_view(request, lesson_id):
    """Display detailed information about a specific lesson."""
    lesson = get_object_or_404(Lesson, id=lesson_id)

    # Mark the lesson as started/completed
    if request.user.is_authenticated:
        progress, created = LessonProgress.objects.get_or_create(user=request.user, lesson=lesson)
        if not progress.is_completed:
            progress.is_completed = True
            progress.save()

    return render(request, 'content/lesson_detail.html', {'lesson': lesson})



@login_required
def quiz_view(request, lesson_id):
    """Display a quiz related to a specific lesson and handle answer submissions."""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    quizzes = Quiz.objects.filter(lesson=lesson)

    if request.method == "POST":
        # Handle answer submissions
        score = 0
        total_questions = len(quizzes)
        student_answers = {}

        # Check each submitted answer
        for quiz in quizzes:
            submitted_answer = request.POST.get(f"question_{quiz.id}")
            student_answers[quiz.id] = submitted_answer
            if submitted_answer == quiz.correct_option:
                score += 1

        # Save the student's answers in the session
        request.session['student_answers'] = student_answers

        # Save the quiz result for each quiz
        for quiz in quizzes:
            QuizResult.objects.create(
                user=request.user,
                quiz=quiz,  # Assigning a Quiz instance
                score=score,
                total_questions=total_questions
            )

        # Provide feedback to the user
        context = {
            'lesson': lesson,
            'quizzes': quizzes,
            'score': score,
            'total_questions': total_questions,
        }
        return render(request, 'content/quiz_result.html', context)

    # Display the quiz if it's a GET request
    return render(request, 'content/quiz.html', {'lesson': lesson, 'quizzes': quizzes})

