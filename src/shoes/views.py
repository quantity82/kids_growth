from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ShoesData
from users.models import KidsProfile
from .forms import ShoesDataForm, ShoesDataEditForm


#靴リスト
@login_required
def shoes_data_list(request, **kwargs):
    user_name = request.user
    if len(kwargs) > 0:
        kidsProfileId = kwargs["kidsProfileId"]
    else:
        kidsProfileId = KidsProfile.objects.filter(user=user_name).order_by('id')[0].id

    kids_profiles = KidsProfile.objects.filter(user=user_name) #子供情報選択用
    kids_profile  = KidsProfile.objects.filter(id=kidsProfileId)
    shoes_data_posts = ShoesData.objects.filter(user=user_name, kidsProfile=kidsProfileId).order_by('buy_date')

    params = {
        'shoes_data_posts' : shoes_data_posts,
        'kidsProfiles' : kids_profiles,
        'kidsName' : kids_profile[0].name,
    }
    return render(request, 'shoes/shoes_data_list.html', params)

#靴データを新規追加
@login_required
def shoes_data_add(request):
    user_name = request.user
    if request.method == 'POST':
      form = ShoesDataForm(request.POST, user = user_name)
      if form.is_valid():
        data = form.save(commit=False)
        if request.FILES.get('shoes_image') is None:
            pass
        else:
            data.shoes_image = request.FILES.get('shoes_image')
        data.user = user_name
        data.save()
        return redirect('shoes:shoes_data_list')
    else:
      form = ShoesDataForm(user = user_name)
    return render(request, 'shoes/shoes_data_add.html', {'form': form})

#靴データを編集
@login_required
def shoes_data_edit(request, shoesDataId):
    shoes_data = ShoesData.objects.get(pk=shoesDataId)
    if request.method == 'POST':
      form = ShoesDataEditForm(request.POST)
      if form.is_valid():
        data = form.save(commit=False)
        data.user = request.user
        data.kidsProfile = shoes_data.kidsProfile
        data.shoes_image = request.FILES.get('shoes_image')
        data.save()
        shoes_data.delete()
        return redirect('shoes:shoes_data_list')
    else:
      form = ShoesDataEditForm(
        {
          'buy_date' : shoes_data.buy_date ,
          'shoes_size' : shoes_data.shoes_size ,
          'shoes_memo' : shoes_data.shoes_memo ,
          'shoes_image' : shoes_data.shoes_image
        },
        user = request.user
      )
    return render(request, 'shoes/shoes_data_edit.html', {'form': form})

#靴データを削除
@login_required
def shoes_data_delete(request, shoesDataId):
    ShoesData.objects.get(id=shoesDataId).delete()
    return redirect('shoes:shoes_data_list')