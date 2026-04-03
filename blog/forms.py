from django import forms
from .models import Post, Comment, UserProfile  # ✅ 新增导入 UserProfile

# 你原来的 PostForm（样式我保留你微调后的版本）
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 100%; font-size:16px; padding:8px;'}),
            'text': forms.Textarea(attrs={'class': 'vLargeTextField', 'style': 'width:100%; height:300px; font-size:14px;'}),
        }

# 你原来的 CommentForm
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your comment...'}),
        }

# ✅ 新增：用户资料表单（昵称+头像），样式和你的保持一致
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nickname', 'avatar']
        widgets = {
            # 沿用你用的 Django 管理员样式类，保持视觉统一
            'nickname': forms.TextInput(attrs={'class': 'vTextField', 'style': 'width: 100%; font-size:16px; padding:8px;'}),
            'avatar': forms.ClearableFileInput(attrs={'style': 'margin-top:10px;'}),
        }