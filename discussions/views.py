from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import DiscussionThread, ThreadMessage, PrivateMessage
from .forms import ThreadMessageForm, PrivateMessageForm,ReplyMessageForm
from django.contrib.auth.models import User
@login_required
def thread_list(request):
    threads = DiscussionThread.objects.all().order_by('-created_at')
    return render(request, 'discussions/thread_list.html', {'threads': threads})


@login_required
def thread_detail(request, thread_id):
    thread = get_object_or_404(DiscussionThread, id=thread_id)
    messages = thread.messages.all().order_by('-created_at')
    if request.method == 'POST':
        form = ThreadMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.thread = thread
            message.author = request.user
            message.save()
            return redirect('thread_detail', thread_id=thread.id)
    else:
        form = ThreadMessageForm()
    return render(request, 'discussions/thread_detail.html', {'thread': thread, 'messages': messages, 'form': form})


@login_required
def inbox(request):
    # Fetch all messages where the logged-in user is the recipient
    messages = PrivateMessage.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'discussions/inbox.html', {'messages': messages})


@login_required
def user_messages(request):
    # Fetch received messages (where the logged-in user is the recipient)
    received_messages = PrivateMessage.objects.filter(recipient=request.user).order_by('-created_at')

    # Fetch sent messages (where the logged-in user is the sender)
    sent_messages = PrivateMessage.objects.filter(sender=request.user).order_by('-created_at')

    # Pass both received and sent messages to the template
    return render(request, 'discussions/messages.html', {
        'received_messages': received_messages,
        'sent_messages': sent_messages
    })

# reply = PrivateMessage.objects.create(
#     sender=user2,
#     recipient=user1,
#     content="This is a reply.",
#     parent_message=original_message
# )
@login_required
def reply_message_view(request, message_id):
    # Get the message to reply to
    original_message = PrivateMessage.objects.get(id=message_id)
    
    # Handle the reply form submission
    if request.method == 'POST':
        form = ReplyMessageForm(request.POST)
        if form.is_valid():
            # Create a new message object (reply)
            reply_content = form.cleaned_data['content']
            reply_message = PrivateMessage(
                sender=request.user,
                recipient=original_message.sender,
                content=reply_content,
                parent_message=original_message,
            )
            reply_message.save()
            return redirect('inbox')  # Redirect to inbox after sending the reply
    
    else:
        form = ReplyMessageForm()
    
    return render(request, 'discussions/reply_message.html', {'form': form, 'original_message': original_message})
@login_required
def user_thread(request, other_user_id):
    # Get the other user (the user the logged-in user is communicating with)
    other_user = get_object_or_404(User, id=other_user_id)

    # Fetch messages sent or received between the logged-in user and the other user
    messages = PrivateMessage.objects.filter(
        (Q(sender=request.user) & Q(recipient=other_user)) | (Q(sender=other_user) & Q(recipient=request.user))
    ).order_by('created_at')  # Order by oldest to newest

    # Pass the messages and other user to the template
    return render(request, 'discussion/thread_detail.html', {
        'messages': messages,
        'other_user': other_user,
    })

@login_required
def send_private_message(request):
    users = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        form = PrivateMessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            recipient_id = request.POST.get('recipient')
            message.recipient = get_object_or_404(User, id=recipient_id)
            message.save()
            return JsonResponse({'status': 'success'}, status=200)  # Return JSON response
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    else:
        form = PrivateMessageForm()
    return render(request, 'discussions/send_message.html', {'form': form, 'users': users})