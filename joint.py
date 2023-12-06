from PIL import Image
import os

# 画像の間隔
gap = 20

# 画像のリストを作成
images = [Image.open(f"{i}_{j}.png") for i in range(8) for j in range(64)]

# 新しい画像のサイズを計算
total_width = (images[0].width + gap) * 8 - gap
max_height = (max(image.height for image in images) + gap) * 64 - gap

# 新しい画像を作成
new_image = Image.new('RGB', (total_width, max_height))

# 画像を配置
for index, image in enumerate(images):
    x_offset = (image.width + gap) * (index % 8)
    y_offset = (image.height + gap) * (index // 8)
    new_image.paste(image, (x_offset, y_offset))

# 新しい画像を保存
new_image.save("combined_image.png")