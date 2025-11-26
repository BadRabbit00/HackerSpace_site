from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import News
from .forms import NewsForm

def news_home(request):
    news_items = News.objects.all().order_by('-published_at')
    return render(request, 'news/news_home.html', {'news_items': news_items})

@login_required
@user_passes_test(lambda u: u.is_staff)
def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.published_by = request.user.username
            # Pass description to the instance for the signal
            news._card_description = form.cleaned_data['description']
            news.save()
            messages.success(request, 'News created successfully!')
            return redirect('news_home')
    else:
        form = NewsForm()
    
    return render(request, 'news/create_news.html', {'form': form})
