from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, UserProfile

# 注册表单 - 新增邮箱必填项（老师要求）
class NewUserForm(UserCreationForm):
    # 核心修改：添加邮箱字段，设置为必填（Django自带邮箱格式验证）
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        # 字段包含：用户名、邮箱、密码1、密码2
        fields = ("username", "email", "password1", "password2")

    # 保存用户时，同步保存邮箱字段
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

# 用户资料表单（原有代码，无修改）
from django import forms
from django.contrib.auth.models import User

# 新增：用户资料编辑表单
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # 允许编辑用户名和邮箱
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

# 博客表单（原有代码，无修改）
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Post title'}),
            'text': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Post content'}),
        }

# 评论表单（原有代码，无修改）
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {'body': 'Comment Content'}
        widgets = {'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment'})}