from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm,UserRegistrationForm
from django.shortcuts import get_list_or_404,redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.
def index (request):
    return render (request,'index.html')


def Tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})

@login_required
def Tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')   
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Tweet
from .forms import TweetForm

@login_required
def Tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    
    if request.method == 'POST':
        form = TweetForm(request.POST, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('tweet_list')  # Adjust redirect as needed
    else:
        form = TweetForm(instance=tweet)
    
    return render(request, 'tweet_form.html', {'form': form})



@login_required
def Tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        return redirect('tweet_list')  # Redirect to the tweet list after deletion
    return render(request, 'confirm_delete.html', {'tweet': tweet})


def register (request):
    if request.method=='POST':
      form=UserRegistrationForm(request.POST)
      if form.is_valid():
         user = form.save(commit=False)
         user.set_password(form.cleaned_data['password1'])
         user.save()
         login(request,user)
         return redirect('tweet_list')
    else:
     form=UserRegistrationForm
     return render (request,'registration/register.html', {'form':form})