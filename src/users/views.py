from django.contrib.auth import login as dj_login
from .forms import SignUpForm, LoginForm, KidsProfileForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .models import KidsProfile

# サインアップ画面
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            dj_login(request, user)
            return redirect(to='/')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

#ログインページ
class login_mypage(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

#ログアウトページ
class logout(LogoutView):
    template_name = 'users/login.html'

#マイページページ
@login_required
def mypage(request):

    user_name = request.user
    kidsProfiles = KidsProfile.objects.filter(user=user_name)

    params = {
        'user' : user_name,
        'kidsProfiles' : kidsProfiles,
    }
    return render(request, 'users/mypage.html',params)


#子供情報追加
@login_required
def kids_profile_add(request):
    user_name = request.user
    if request.method == 'POST':
      form = KidsProfileForm(request.POST, user = user_name)
      if form.is_valid():
        data = form.save(commit=False)
        data.user = user_name
        data.save()
        return redirect('users:mypage')
    else:
      form = KidsProfileForm(user = user_name)
    return render(request, 'users/kids_profile_add.html', {'form': form})

#子供情報編集
@login_required
def kids_profile_edit(request, kidsProfileId):
    kidsProfileData = KidsProfile.objects.get(pk=kidsProfileId)
    if request.method == 'POST':
      form = KidsProfileForm(request.POST)
      if form.is_valid():
        data = form.save(commit=False)
        data.id = kidsProfileData.id
        data.user = request.user
        data.save()
        return redirect('users:mypage')
    else:
      form = KidsProfileForm(
        {
          'name' : kidsProfileData.name ,
          'gender' : kidsProfileData.gender ,
          'birthday' : kidsProfileData.birthday
        },
      )
    return render(request, 'users/kids_profile_edit.html', {'form': form})

#子供情報削除
@login_required
def kids_profile_delete(request, kidsProfileId):
    KidsProfile.objects.get(pk=kidsProfileId).delete()
    return redirect('users:mypage')