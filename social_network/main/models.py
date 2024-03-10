from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from PIL import Image


# resizing images
def save(self, *args, **kwargs):
    super().save()

    img = Image.open(self.avatar.path)

    if img.height > 100 or img.width > 100:
        new_img = (100, 100)
        img.thumbnail(new_img)
        img.save(self.avatar.path)


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField(default="It's empty")

    def __str__(self):
        return self.user.username


class Post(models.Model):
    datetime = models.DateTimeField(verbose_name=u"Дата", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u"Автор", related_name="posts")
    text = models.CharField(max_length=1000, verbose_name=u"Текст", null=True, blank=True)
    image = models.FileField(verbose_name=u"Картинка", null=True, blank=True)

    class Meta:
        ordering = ["-datetime"]


class Comment(models.Model):
    datetime = models.DateTimeField(verbose_name=u"Дата", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u"Автор", related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=u"Пост", related_name="comments")
    text = models.CharField(max_length=1000, verbose_name=u"Текст", null=True, blank=True)

    class Meta:
        ordering = ["datetime"]


class FriendList(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends")

    def __str__(self):
        return self.user.username

    def add_friend(self, account):
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()

    def remove_friend(self, account):
        if account in self.friends.all():
            self.friends.remove(account)
            self.save()

    def unfriend(self, removee):
        remover_friends_list = self

        remover_friends_list.remove_friend(removee)

        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):
        if friend in self.friends.all():
            return True
        return False


class FriendRequest(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend()
            sender_friend_list = FriendList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()


class Reciever(models.Model):
    receiver_name = models.TextField(max_length=1000, verbose_name=u"Текст", null=True, blank=True)