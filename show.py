import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# 画像の読み込み
img = mpimg.imread('sub2-64.png')

# 64x64の画像を作成
fig, axs = plt.subplots(8, 8, figsize=(15, 15))

# 画像をプロット
for i in range(64):
    axs[i // 8, i % 8].imshow(img)
    axs[i // 8, i % 8].axis('off')  # 軸を非表示に

# ある配列に基づいて線分を引く
lines = np.array([[0, 1], [1, 2], [2, 3], [3, 0]])  # これは例です。あなたの配列に置き換えてください。
for line in lines:
    start = line[0]
    end = line[1]
    axs[start // 8, start % 8].plot([start % 8, end % 8], [start // 8, end // 8], color='r')

plt.show()