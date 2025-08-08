# views.py
from django.shortcuts import render
from .models import EducationalContent,Dataset,KcsePastPaper
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import KcsePastPaper, SubjectNote, SharedResource, Notification, Profile
from .forms import SubjectNoteForm, SharedResourceForm, KcsePastPaperForm
from django.contrib.auth.decorators import login_required, user_passes_test
from users.models import Profile
# import openai
# from django.conf import settings
# from django.http import JsonResponse
# from .models import ChatMessage

# openai.api_key = settings.OPENAI_API_KEY
def educational_content_list(request):
    # Fetch all educational content and sort by content type (video, file, photo)
    content_items = EducationalContent.objects.all().order_by('content_type')

    return render(request, 'ai_engine/educational_content_list.html', {'content': content_items})


def dataset_list(request):
    datasets = Dataset.objects.all()
    return render(request, 'ai_engine/datasets.html', {'datasets': datasets})

def kcse_papers(request):
    papers = KcsePastPaper.objects.all().order_by('-year', 'subject')
    return render(request, 'ai_engine/kcse_papers.html', {'papers': papers})






def is_teacher(user):
    return hasattr(user, 'profile') and user.profile.is_teacher

def kcse_papers(request):
    papers = KcsePastPaper.objects.all().order_by('-year', 'subject')
    return render(request, 'ai_engine/kcse_papers.html', {'papers': papers})

def subject_notes(request):
    notes = SubjectNote.objects.all().order_by('subject', 'topic')
    return render(request,'ai_engine/subject_notes.html', {'notes': notes})

def shared_resources(request):
    resources = SharedResource.objects.filter(approved=True).order_by('-upload_date')
    return render(request, 'ai_engine/shared_resources.html', {'resources': resources})

@login_required
def submit_note(request):
    if request.method == 'POST':
        form = SubjectNoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.uploaded_by = request.user
            note.save()
            return redirect('subject_notes')
    else:
        form = SubjectNoteForm()
    return render(request, 'ai_engine/submit_notes.html', {'form': form})

@login_required
def submit_resource(request):
    if request.method == 'POST':
        form = SharedResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save(commit=False)
            resource.uploaded_by = request.user
            if is_teacher(request.user):
                resource.approved = True
            resource.save()
            return redirect('shared_resources')
    else:
        form = SharedResourceForm()
    return render(request, 'ai_engine/submit_resource.html', {'form': form})

@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    students = Profile.objects.all()
    pending_resources = SharedResource.objects.filter(approved=False)
    my_notes = SubjectNote.objects.filter(uploaded_by=request.user)
    return render(request, 'ai_engine/teacher_dashboard.html', {
        'students':students,
        'pending_resources': pending_resources,
        'my_notes': my_notes,
    })

@login_required
@user_passes_test(is_teacher)
def approve_resource(request, resource_id):
    resource = get_object_or_404(SharedResource, id=resource_id)
    resource.approved = True
    resource.save()
    # Notify uploader
    Notification.objects.create(
        recipient=resource.uploaded_by,
        message=f"Your resource '{resource.title}' was approved!",
        link="/shared-resources/"
    )
    return redirect('teacher_dashboard')

@login_required
def user_notifications(request):
    notes = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    for note in notes.filter(is_read=False):
        note.is_read = True
        note.save()
    return render(request, 'ai_engine/notifications.html', {'notifications': notes})




# def chat_bot_view(request):
#     if request.method == "POST":
#         user_input = request.POST.get("message")
#         user = request.user

#         # Call OpenAI
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",  # or "gpt-4" if available
#             messages=[
#                 {"role": "system", "content": "You are a helpful educational assistant."},
#                 {"role": "user", "content": user_input}
#             ]
#         )

#         bot_reply = response['choices'][0]['message']['content']

#         # Optionally save the conversation
#         ChatMessage.objects.create(user=user, message=user_input, response=bot_reply)

# #         return JsonResponse({'reply': bot_reply})

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json


# def chat_page(request):
#     return render(request, "ai_engine/chat_bot.html")



# def mock_chat(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             user_message = data.get('message', '')
#         except (json.JSONDecodeError, AttributeError):
#             return JsonResponse({"error": "Invalid JSON"}, status=400)
#         return JsonResponse({"response": f"You said: {user_message}"})
#     return JsonResponse({"error": "Only POST requests allowed"}, status=405)

