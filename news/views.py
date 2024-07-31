from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm  # Assuming you have a custom login form if needed
from .models import CrawlHackerNews, Vote
import logging
from .forms import CommentForm
from .models import Comment_Form
from .forms import RegisterForm
from .documents import CrawlHackerNewsDocument 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import LinkForm
from news.models import CrawlHackerNews
from django.http import JsonResponse
# from .forms import ReplyForm
from .models import Comment_Form, Comment_Reply
from .forms import CommentForm, ReplyForm
from .models import Comment_Form, Comment




logger = logging.getLogger(__name__)

def news_list(request):
    news_items = CrawlHackerNews.objects.all().order_by('-date')
    paginator = Paginator(news_items, 10)  # Show 10 news items per page
    user = request.user
    print(user)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print("page1:",page_obj)

    return render(request, 'news_list.html', {'page_obj': page_obj,"user":user})

# def search(request):
#     query = request.GET.get('q')
#     if query:
#         news_items = CrawlHackerNews.objects.filter(title__icontains=query).order_by('-date')
#     else:
#         news_items = CrawlHackerNews.objects.none()

#     paginator = Paginator(news_items, 10)  # Show 10 news items per page
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     return render(request, 'news_list.html', {'page_obj': page_obj, 'query': query})

def login_view(request):
    if request.method == 'POST':
            print(request.POST)
            form = LoginForm(request, data=request.POST)
            
        # if form.is_valid():
           
            username = request.POST['username']
            password = request.POST['password']  # Use cleaned_data here
            print(username, password)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, "Invalid username or password.")
        # else:
        #     print("Form is not valid:", form.errors)
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
            form = RegisterForm(request.POST)
       
            user = form.save()
            login(request, user)
            return redirect('index')  # Redirect to the home page or any other page
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})



@login_required
def comments_view(request):
    comments = Comment_Form.objects.all()
    comment_form = CommentForm()
    reply_forms = {comment.id: ReplyForm() for comment in comments}

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'comment_form':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.name = request.user.username
                new_comment.email = request.user.email
                new_comment.save()
                return redirect('comments_view')
        elif form_type.startswith('reply_form_'):
            comment_id = int(form_type.split('_')[-1])
            comment = get_object_or_404(Comment_Form, id=comment_id)
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                new_reply = reply_form.save(commit=False)
                new_reply.comment = comment
                new_reply.user = request.user
                new_reply.save()
                return redirect('comments_view')

    context = {
        'comments': comments,
        'comment_form': comment_form,
        'reply_forms': reply_forms
    }
    return render(request, 'comment_list.html', context)
def comment_success_view(request):
    return render(request, 'comment_success.html')

# @login_required
def index(request):
    news_items = CrawlHackerNews.objects.all().order_by('-date')
    logger.info(f"Fetched news items: {news_items}")  # Logging for debugging
    print(f"Fetched news items: {news_items}")  # Print for debugging
    return render(request, 'news/index.html', {'news_items': news_items})


@login_required
def detail(request, news_id):
    news_item = get_object_or_404(CrawlHackerNews, pk=news_id)
    print(news_item)
    return render(request, 'news/detail.html', {'news_item': news_item, 'news_id': news_id})


def vote(request, news_id):
    if request.method == 'POST':
        user = request.user
        news = CrawlHackerNews.objects.get(id=news_id)
        vote_type = request.POST.get('vote_type')

        vote, created = Vote.objects.get_or_create(user=user, news=news)
        if vote_type == 'upvote':
            vote.vote_type = 'upvote'
        else:
            vote.vote_type = 'downvote'
        vote.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
def search(request):
    query = request.GET.get('q')
    if query:
        news_items = CrawlHackerNews.objects.filter(title__icontains=query)
    else:
        news_items = CrawlHackerNews.objects.none()

    # Pagination
    paginator = Paginator(news_items, 10)  # Show 10 news items per page
    page = request.GET.get('page')
    
    try:
        news_items = paginator.page(page)
    except PageNotAnInteger:
        news_items = paginator.page(1)
    except EmptyPage:
        news_items = paginator.page(paginator.num_pages)

    return render(request, 'news/search.html', {
        'news_items': news_items,
        'query': query
    })


def comment_list(request):
    comment_forms = Comment_Form.objects.all()
    comments = Comment.objects.select_related('news', 'user').all()
    return render(request, 'comment_list.html', {
        'comment_forms': comment_forms,
        'comments': comments,
    })

def submit_link(request):
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.user = request.user
            link.save()
            return redirect('link_success')  # Redirect to a relevant view after submission
    else:
        form = LinkForm()
    
    return render(request, 'submit_link.html', {'form': form})

def link_success_view(request):
    return render(request, 'comment_success.html')

from .models import LinkSubmission

def link_submission_list(request):
    links = LinkSubmission.objects.all()
    return render(request, 'link_submission_list.html', {'links': links})