import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import json

# 8x64のグリッドを作成
fig, axs = plt.subplots(64, 8, figsize=(20, 120))

# グリッドの各セルに画像を配置
for i in range(64):
    for j in range(8):
        img = mpimg.imread(f'{j}_{i}.png')  # 画像を読み込む
        axs[i, j].imshow(img)
        axs[i, j].axis('off')  # 軸を非表示に

# record.jsonからデータを読み込む
with open('record.json') as f:
    data = json.load(f)

# 矢印を描画
for generation in list(data.keys())[:8]:  # 0から7までのgenerationのみを処理
    for individual in range(len(data[generation])):
        child = int(individual)
        child_coords = (child ,int(generation))

        # par1が存在する場合のみ矢印を描画
        if 'par1' in data[str(generation)][str(individual)]:
            parent1 = int(data[generation][str(individual)]['par1'])
            parent1_coords = (parent1 , int(generation) - 1)  # parent1は前の世代
            axs[parent1_coords].annotate("", xy=child_coords, xytext=parent1_coords, 
                                         xycoords='data', 
                                         arrowprops=dict(arrowstyle="->", color='r'))

        # par2が存在する場合のみ矢印を描画
        if 'par2' in data[str(generation)][str(individual)]:
            parent2 = int(data[generation][str(individual)]['par2'])
            parent2_coords = (parent2 ,int(generation) - 1)  # parent2は前の世代
            axs[parent2_coords].annotate("", xy=child_coords, xytext=parent2_coords, 
                                         xycoords='data', 
                                         arrowprops=dict(arrowstyle="->", color='r'))

# 画像として保存
plt.subplots_adjust(wspace=0.5)  # 画像間のスペースを調整
plt.savefig("grid.png")