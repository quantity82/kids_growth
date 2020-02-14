from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import PhysData
from users.models import KidsProfile
from .forms import PhysDataForm, PhysDataEditForm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np
import pandas as pd
import io


# 身長体重データを昇順で返却
@login_required
def phys_data_list(request, **kwargs):
    user_name = request.user

    try:
        if len(kwargs) > 0:
            kidsProfileId = kwargs["kidsProfileId"]
        else:
            kidsProfileId = KidsProfile.objects.filter(user=user_name).first().id

        kids_profiles = KidsProfile.objects.filter(user=user_name)
        data_posts = PhysData.objects.filter(user=user_name, kidsProfile=kidsProfileId).order_by('date')

    except AttributeError:
        data_posts = None
        kids_profiles = None

    params = {
        'data_posts': data_posts,
        'kidsProfiles': kids_profiles,
    }

    return render(request, 'phys/phys_data_list.html', params)


# 身長体重データを新規登録する
@login_required
def phys_data_add(request):
    user_name = request.user
    if request.method == 'POST':
        form = PhysDataForm(request.POST, user=user_name)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user_name
            data.save()
            return redirect('phys:phys_data_list')
    else:
        form = PhysDataForm(user=user_name)
    return render(request, 'phys/phys_data_add.html', {'form': form})


# 身長体重データを編集する
@login_required
def phys_data_edit(request, dataPostId):
    physData = PhysData.objects.get(pk=dataPostId)
    if request.method == 'POST':
        form = PhysDataEditForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.kidsProfile = physData.kidsProfile
            data.id = physData.id
            data.save()
            return redirect('phys:phys_data_list')
    else:
        form = PhysDataEditForm(
            {
                'weight': physData.weight,
                'height': physData.height,
                'date': physData.date
            },
            user=request.user
        )
    return render(request, 'phys/phys_data_edit.html', {'form': form})


# 身長体重データを削除する
@login_required
def phys_data_delete(request):
    delete_ids = request.POST.getlist('delete_ids')
    PhysData.objects.filter(pk__in=delete_ids).delete()
    return redirect('phys:phys_data_list')

#グラフ画像を表示するページ
@login_required
def graph_page_display(request, **kwargs):
    user_name = request.user
    try:
        if len(kwargs) > 0:
            kidsProfileId = kwargs["kidsProfileId"]
        else:
            kidsProfileId = KidsProfile.objects.filter(user=user_name).first().id

        kids_profiles = KidsProfile.objects.filter(user=user_name)
        kids_name = KidsProfile.objects.get(id=kidsProfileId).name

    except AttributeError:
        kids_profiles = None
        kidsProfileId = None
        kids_name = "子供情報を登録してください"

    params = {
        'kidsProfiles' : kids_profiles,
        'kidsProfileId' : kidsProfileId,
        'kidsName' : kids_name,
    }
    return render(request, 'phys/phys_graph_display.html', params)

# グラフの画像生成
@login_required
def graph_image_display(request, **kwargs):
    # 初期設定
    fig = plt.figure(figsize=(8, 5))
    ax_h = fig.add_subplot(1, 1, 1)
    ax_w = ax_h.twinx()
    ax_hs = ax_h.twinx()
    ax_ws = ax_h.twinx()

    # グラフ自体の設定
    # タイトル
    ax_h.set_xlabel(u'age')
    ax_h.set_ylabel(u'cm')
    ax_w.set_ylabel(u'kg')

    # 固定線の描画
    border_color_h = 'skyblue' #身長の固定線色
    border_color_w = 'lightgreen' #体重の固定線色
    border_lw_mid = 2 #中央の固定線太さ
    border_lw_other = 1 #中央以外の固定線太さ

    # 固定値（身長）
    # 3%
    data_man_height_03 = pd.read_csv('static/physData/man_height_03.csv', names=['num1', 'num2'])
    ax_h.plot(data_man_height_03['num1'], data_man_height_03['num2'], color=border_color_h, lw=border_lw_other)
    # 10%
    data_man_height_10 = pd.read_csv('static/physData/man_height_10.csv', names=['num1', 'num2'])
    ax_h.plot(data_man_height_10['num1'], data_man_height_10['num2'], color=border_color_h, lw=border_lw_other)
    # 25%
    data_man_height_25 = pd.read_csv('static/physData/man_height_25.csv', names=['num1', 'num2'])
    ax_h.plot(data_man_height_25['num1'], data_man_height_25['num2'], color=border_color_h, lw=border_lw_other)
    # 50%
    data_man_height_50 = pd.read_csv('static/physData/man_height_50.csv', names=['num1', 'num2'])
    ax_h.plot(data_man_height_50['num1'], data_man_height_50['num2'], color=border_color_h, lw=border_lw_mid)
    # 75%
    data_man_height_75 = pd.read_csv('static/physData/man_height_75.csv', names=['num1', 'num2'])
    ax_h.plot(data_man_height_75['num1'], data_man_height_75['num2'], color=border_color_h, lw=border_lw_other)
    # 90%
    data_man_height_90 = pd.read_csv('static/physData/man_height_90.csv', names=['num1', 'num2'])
    ax_h.plot(data_man_height_90['num1'], data_man_height_90['num2'], color=border_color_h, lw=border_lw_other)
    # 97%
    data_man_height_97 = pd.read_csv('static/physData/man_height_97.csv', names=['num1', 'num2'])
    ax_h.plot(data_man_height_97['num1'], data_man_height_97['num2'], color=border_color_h, lw=border_lw_other)

    # 固定値（体重）
    # 3%
    data_man_weight_03 = pd.read_csv('static/physData/man_weight_03.csv', names=['num1', 'num2'])
    ax_w.plot(data_man_weight_03['num1'], data_man_weight_03['num2'], color=border_color_w, lw=1)
    # 10%
    data_man_weight_10 = pd.read_csv('static/physData/man_weight_10.csv', names=['num1', 'num2'])
    ax_w.plot(data_man_weight_10['num1'], data_man_weight_10['num2'], color=border_color_w, lw=1)
    # 25%
    data_man_weight_25 = pd.read_csv('static/physData/man_weight_25.csv', names=['num1', 'num2'])
    ax_w.plot(data_man_weight_25['num1'], data_man_weight_25['num2'], color=border_color_w, lw=1)
    # 50%
    data_man_weight_50 = pd.read_csv('static/physData/man_weight_50.csv', names=['num1', 'num2'])
    ax_w.plot(data_man_weight_50['num1'], data_man_weight_50['num2'], color=border_color_w, lw=1.5)
    # 75%
    data_man_weight_75 = pd.read_csv('static/physData/man_weight_75.csv', names=['num1', 'num2'])
    ax_w.plot(data_man_weight_75['num1'], data_man_weight_75['num2'], color=border_color_w, lw=1)
    # 90%
    data_man_weight_90 = pd.read_csv('static/physData/man_weight_90.csv', names=['num1', 'num2'])
    ax_w.plot(data_man_weight_90['num1'], data_man_weight_90['num2'], color=border_color_w, lw=1)
    # 97%
    data_man_weight_97 = pd.read_csv('static/physData/man_weight_97.csv', names=['num1', 'num2'])
    ax_w.plot(data_man_weight_97['num1'], data_man_weight_97['num2'], color=border_color_w, lw=1)

    # 子供データ取得
    user_name = request.user

    if len(kwargs) > 0:
        kidsProfileId = kwargs["kidsProfileId"]
    else:
        kidsProfileId = KidsProfile.objects.filter(user=user_name).order_by('id')[0].id

    kids_profile = KidsProfile.objects.filter(user=user_name, id=kidsProfileId)
    phys_data = PhysData.objects.filter(user=user_name, kidsProfile=kidsProfileId)

    # グラフデータ作成
    graph_height = []
    graph_weight = []
    graph_date = []

    for i in range(len(phys_data)):
        graph_height.append(phys_data[i].height)
        graph_weight.append(phys_data[i].weight)

        # 誕生日計算（小数点計算）
        dStr1 = phys_data[i].date.strftime('%Y%m%d')
        dStr2 = kids_profile[0].birthday.strftime('%Y%m%d')

        if kids_profile[0].birthday.year == phys_data[i].date.year:
            dStr3 = (int(dStr1) - int(dStr2)) / 1000 # 0才のときの月齢を出す
        else:
            dStr3 = (int(dStr1) - int(dStr2)) / 10000 # 一般的な誕生日計算
        graph_date.append(dStr3)

    # グラフプロット（分散図）
    ax_hs.scatter(graph_date, graph_height, marker='x', color='blue')
    ax_ws.scatter(graph_date, graph_weight, marker='x', color='green')

    # グリッド設定
    ax_h.grid(which='both', color='gray', linestyle='solid')
    ax_w.grid(which='both', color='gray', linestyle='solid')

    # Y軸最大値設定
    ax_h.set_ylim([0, 140])
    ax_w.set_ylim([0, 35])
    ax_hs.set_ylim([0, 140])
    ax_ws.set_ylim([0, 35])

    # Y軸メモリ
    ax_h.set_yticks(np.linspace(0, 140, 15))
    ax_w.set_yticks(np.linspace(0, 35, 15))
    ax_hs.set_yticks([])
    ax_ws.set_yticks([])

    # X軸メモリ
    ax_h.set_xticks(np.linspace(0, 7, 8))
    ax_w.set_xticks(np.linspace(0, 7, 8))
    ax_hs.set_xticks(np.linspace(0, 7, 8))
    ax_ws.set_xticks(np.linspace(0, 7, 8))

    # 描画
    canvas = FigureCanvasAgg(fig)
    buf = io.BytesIO()
    canvas.print_png(buf)

    response = HttpResponse(buf.getvalue(), content_type='image/png')

    fig.clear()

    response['Content-Length'] = str(len(response.content))

    return response
