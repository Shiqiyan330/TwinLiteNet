import re
import matplotlib.pyplot as plt

# 读取nohup.out
with open('nohup.out', 'r') as f:
    lines = f.readlines()

epochs = []
miou = []
acc = []
iou = []

for line in lines:
    # 匹配进度行，提取epoch
    match = re.match(r'(\d+)%\|.*\[(\d+):(\d+)<.*\]', line)
    if match:
        # 这里假设每个进度条都代表一个epoch
        epoch = int(match.group(2))  # 取分钟数作为epoch编号
        epochs.append(epoch)
    # 匹配 Driving Area Segment: mIOU
    if 'Driving Area Segment: mIOU' in line:
        m = re.search(r'mIOU\(([\d.]+)\)', line)
        if m:
            miou.append(float(m.group(1)))
    # 匹配 Lane Line Segment: Acc IOU
    if 'Lane Line Segment:' in line:
        m1 = re.search(r'Acc\(([\d.]+)\)', line)
        m2 = re.search(r'IOU\(([\d.]+)\)', line)
        if m1:
            acc.append(float(m1.group(1)))
        if m2:
            iou.append(float(m2.group(1)))

# 画图
plt.figure()
# 手动设置尺寸使图片清晰
plt.figure(figsize=(10, 6))
plt.plot(miou, label='Driving Area mIOU')
plt.plot(acc, label='Lane Line Acc')
plt.plot(iou, label='Lane Line IOU')
plt.xlabel('Epoch')
plt.ylabel('Metric')
plt.legend()
plt.title('Training Curve')
plt.show()
# 保存
plt.savefig('training_curve.png')