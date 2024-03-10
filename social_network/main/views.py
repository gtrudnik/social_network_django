from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from .forms import UpdateUserForm, UpdateProfileForm, PostForm, FriendForm, receiverform
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.views.generic import TemplateView
from .models import Post, User, FriendList, FriendRequest
from django.shortcuts import render, get_object_or_404

# Create your views here.


def start_menu(request):
    return render(request, 'main/start_menu.html')


def login(request):
    return render(request, 'main/login.html')


def registration(request):
    return render(request, 'main/registration.html')


def friends(request):
    return render(request, 'main/Friends.html')


def add_post(request):
    return render(request, 'main/Add_post.html')


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class profile_page(TemplateView):
    template_name = 'main/profile.html'

    def get(self, request, username):

        # получаем пользователя по username если он существует
        user = get_object_or_404(User, username=username)
        # передаем его в шаблон как profile
        return render(request, self.template_name, {'usernow': user, 'posts': Post.objects.all()})


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'main/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


class HomeView(TemplateView):
    template_name = "main/news.html"
    timeline_template_name = "main/timeline.html"

    def dispatch(self, request, *args, **kwargs):
        try:
            friend_list = FriendList.objects.get(user=request.user)
        except:
            FriendList.objects.create(user=request.user)
            friend_list = FriendList.objects.get(user=request.user)
        context = {
            'posts': Post.objects.all(),
            'friendlists': friend_list
        }
        return render(request, self.timeline_template_name, context)


class CreatePost(TemplateView):
    template_name = "main/add_post.html"
    timeline_template_name = "main/add_post.html"

    def dispatch(self, request, *args, **kwargs):

        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.author = request.user
                form.save()
                return redirect(reverse("news"))
        context = {
            'posts': Post.objects.all()
        }
        return render(request, self.timeline_template_name, context)


class FriendsView(TemplateView):
    template_name = "main/Friends.html"
    timeline_template_name = "main/Friends.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            # friend_form = FriendForm(request.POST)
            receiver_name = request.POST.get('receiver_name')
            accept_form = request.POST.get('accept')
            decline_form = request.POST.get('decline')
            cancel_form = request.POST.get('cancel')
            delete_form = request.POST.get('delete')
            if accept_form:
                friend_reqs = FriendRequest.objects.filter(sender=User.objects.get(username=accept_form), receiver=request.user, is_active=True)
                for friend_req in friend_reqs:
                    friend_req.cancel()
                try:
                    friend_list = FriendList.objects.get(user=request.user)
                except:
                    FriendList.objects.create(user=request.user)
                    friend_list = FriendList.objects.get(user=request.user)
                friend_list.add_friend(account=User.objects.get(username=accept_form))

                friend_list2 = FriendList.objects.get(user=User.objects.get(username=accept_form))
                friend_list2.add_friend(account=request.user)

                return redirect(reverse("friends"))
            elif decline_form:
                friend_reqs = FriendRequest.objects.filter(sender=User.objects.get(username=decline_form),
                                                           receiver=request.user, is_active=True)
                for friend_req in friend_reqs:
                    friend_req.decline()
                return redirect(reverse("friends"))
            elif cancel_form:
                friend_reqs = FriendRequest.objects.filter(sender=request.user,
                                                           receiver=User.objects.get(username=cancel_form), is_active=True)
                for friend_req in friend_reqs:
                    friend_req.cancel()
                return redirect(reverse("friends"))
            elif delete_form:
                friend_list = FriendList.objects.get(user=request.user)
                friend_list.remove_friend(account=User.objects.get(username=delete_form))
                friend_list2 = FriendList.objects.get(user=User.objects.get(username=delete_form))
                friend_list2.remove_friend(account=request.user)
                return redirect(reverse("friends"))
            else:
                # receiver_user = get_object_or_404(User, username=username)
                try:
                    try:
                        friend_list = FriendList.objects.get(user=request.user)
                    except:
                        FriendList.objects.create(user=request.user)
                        friend_list = FriendList.objects.get(user=request.user)
                    print(friend_list.friends.all, 666)
                    print(User.objects.get(username=receiver_name))
                    print()
                    if receiver_name != request.user.username and \
                            not(friend_list.is_mutual_friend(User.objects.get(username=receiver_name))):
                        FriendRequest.objects.create(sender=request.user, receiver=User.objects.get(username=receiver_name), is_active=True)

                except:
                    pass
                """friend_form = FriendForm(request.POST)
                friend_form.instance.sender = request.user
                friend_form.instance.is_active = True
                user = get_object_or_404(User, username=request.user)
                friend_form.instance.receiver = user
                friend_form.save()"""
                # print(friend_form.receiver_username, 87989789798)

                #friend_form.instance.receiver = user
                #friend_form.save()
                return redirect(reverse("friends"))
        try:
            friend_list = FriendList.objects.get(user=request.user)
        except:
            FriendList.objects.create(user=request.user)
            friend_list = FriendList.objects.get(user=request.user)
        friendreq = FriendRequest.objects.filter(receiver=request.user, is_active=True)
        your_friendreq = FriendRequest.objects.filter(sender=request.user, is_active=True)

        context = {
            'friendlists': friend_list,
            'friendrequests': friendreq,
            'your_friendrequests': your_friendreq
        }
        #  friend_list.add_friend(account=User.objects.get(username="IRONMAN"))
        #  print(friend_list.friends.all(), 555)
        return render(request, self.timeline_template_name, context)
