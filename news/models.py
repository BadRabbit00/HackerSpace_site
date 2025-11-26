from django.db import models

class News(models.Model):
    title = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='news_photos/')
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    published_by = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    
class NewsCard(models.Model):
    news = models.OneToOneField(News, on_delete=models.CASCADE, related_name='cards')
    description = models.TextField()

    def __str__(self):
        return f"Card for {self.news.title}: {self.news.title}"