from django.db import models

# Create your models here.

"""
버전 관리
"""
class Version(models.Model):
    version = models.CharField(max_length=10)
    osType = models.CharField(max_length=10, default='android')

    def __str__(self):
        return self.version


"""
유저모델
"""
class UserModel(models.Model):
    u_id = models.AutoField(primary_key=True)
    id = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    email = models.EmailField()

    def __str__(self):
        return self.id

"""
게시판 
"""
class PostModel(models.Model):
    name = models.CharField(max_length=255)
    content = models.CharField(max_length=255)

    def __str__(self):
        return self.name

"""
댓글
"""
class Comment(models.Model):
    PostModel = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    reg_date = models.DateField('REG_DATE',auto_now_add=True)

    def __str__(self):
        return self.PostModel

"""
퀴즈
"""
class Quiz(models.Model):
    
    image = models.ImageField()
    value = models.CharField(max_length=255)
    reg_date = models.DateField('REG_DATE',auto_now_add=True)

    def __str__(self):
        return self.PostModel

"""
카테고리
"""
class Category(models.Model):
    c_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return self.name

class ChangeWordModel(models.Model):
    original_sentence = models.CharField(max_length=600, null=True)

    def __str__(self):
        return str(self.original_sentence) 
