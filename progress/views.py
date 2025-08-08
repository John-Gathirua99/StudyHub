from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import LessonProgress, QuizResult,Leaderboard,Notification,Quiz
from django.db import models


@login_required
def progress_report_view(request):
    """Display the user's progress report for lessons and quizzes."""
    lesson_progress = LessonProgress.objects.filter(user=request.user)
    quiz_results = QuizResult.objects.filter(user=request.user)

    context = {
        'lesson_progress': lesson_progress,
        'quiz_results': quiz_results,
    }
    return render(request, 'progress/progress_report.html', context)



def leaderboard_view(request):
    leaderboard_data = Leaderboard.generate_ranking()
    return render(request, 'progress/leaderboard.html', {
        'leaderboard': leaderboard_data
    })



def notification_view(request):
    notifications = Notification.objects.filter(recipient=request.user, is_read=False)
    return render(request, 'progress/notifications.html', {
        'notifications': notifications,
        'notification_count': notifications.count()
    })



@login_required
def reply_notification(request, notification_id):
    if request.method == 'POST':
        original = get_object_or_404(Notification, id=notification_id)
        reply_message = request.POST.get('reply_message')

        Notification.objects.create(
            sender=request.user,
            recipient=original.sender,
            message=reply_message
        )
        return redirect('notifications')  
    


from .models import QuizAttempt, QuizResult,Lesson

def submit_quiz(request, quiz_id):
    """Handle quiz submission and save the attempt."""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    user = request.user
    score = calculate_quiz_score(request.POST, quiz)  # Function to calculate score

    # Count the number of previous attempts
    attempt_number = QuizAttempt.objects.filter(user=user, quiz=quiz).count() + 1

    # Save the new attempt
    QuizAttempt.objects.create(user=user, quiz=quiz, score=score, attempt_number=attempt_number)

    # Update or create the best score in QuizResult
    quiz_result, created = QuizResult.objects.get_or_create(user=user, quiz=quiz)
    if created or score > quiz_result.score:
        quiz_result.score = score
        quiz_result.save()

    return redirect('quiz_attempts', quiz_id=quiz.id)

from .models import QuizAttempt

def quiz_attempts_view(request, quiz_id):
    """Display the user's quiz attempt history."""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    attempts = QuizAttempt.objects.filter(user=request.user, quiz=quiz).order_by('-attempt_number')

    return render(request, 'progress/quiz_attempts.html', {'quiz': quiz, 'attempts': attempts})

from django.db.models import Max

def analytics_view(request):
    """Display detailed analytics for the user's progress."""
    user = request.user

    # Quiz analytics
    best_quiz_scores = QuizResult.objects.filter(user=user).aggregate(Max('score'))

    context = {
        'best_quiz_scores': best_quiz_scores,
        # Existing analytics context
    }

    return render(request, 'progress/analytics.html', context)

def mark_lesson_completed(user, lesson):
    """Mark a lesson as completed for the user."""
    lesson_progress, created = LessonProgress.objects.get_or_create(user=user, lesson=lesson)
    if not lesson_progress.is_completed:
        lesson_progress.is_completed = True
        lesson_progress.save()


def user_progress_chart(request):
    user = request.user
    lessons_completed = LessonProgress.objects.filter(user=user, is_completed=True).count()
    total_lessons = Lesson.objects.count()
    
    scores = QuizAttempt.objects.filter(user=user).order_by('created_at')
    dates = [a.created_at.strftime('%Y-%m-%d') for a in scores]
    score_values = [a.score for a in scores]

    return render(request, 'progress/user_chart.html', {
        'dates': dates,
        'score_values': score_values,
        'lessons_completed': lessons_completed,
        'total_lessons': total_lessons
    })

def notify_user(user, message):
    Notification.objects.create(user=user, message=message)




def recommend_materials(request):
    user = request.user
    
    # Lessons not completed by the user
    
    # Quizzes with low scores (e.g., < 70%)
    low_score_quiz_ids = QuizResult.objects.filter(
        user=user, 
        score__lt=0.7 * models.F('total_questions')
    ).values_list('quiz_id', flat=True)

    # Lessons related to these quizzes
    # remedial_lessons = Lesson.objects.filter(quiz__id__in=low_score_quiz_ids).distinct()
    incomplete_lessons = Lesson.objects.exclude(
    id__in=LessonProgress.objects.filter(user=user, is_completed=True).values_list('lesson_id', flat=True)
)
    remedial_lessons = Lesson.objects.filter(quizzes__id__in=low_score_quiz_ids)  # Don't call .distinct() here

    recommendations = (incomplete_lessons | remedial_lessons).distinct()

    return render(request, 'progress/recommedations.html', {
        'recommendations': recommendations
    })



from django.shortcuts import render
from content.models import Lesson
from .models import LearningMaterial
from django.db.models import F

def personalized_recommendations(request):
    user = request.user
    # Lessons not completed
    incomplete_lesson_ids = LessonProgress.objects.filter(
        user=user, is_completed=False
    ).values_list('lesson_id', flat=True)
    incomplete_lessons = Lesson.objects.filter(id__in=incomplete_lesson_ids)

    # Quizzes with low scores
    low_scores = QuizResult.objects.filter(
        user=user, score__lt=F('total_questions') * 0.7
    ).values_list('quiz__lesson_id', flat=True)

    # Lessons needing remedial help
    remedial_lessons = Lesson.objects.filter(id__in=low_scores)

    # Combine
    all_recommended_lessons = (incomplete_lessons | remedial_lessons).distinct()

    # Learning materials for these lessons
    recommended_materials = LearningMaterial.objects.filter(lesson__in=all_recommended_lessons)

    return render(request, 'progress/recommedations.html', {
        'recommended_materials': recommended_materials
    })
