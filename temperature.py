import torch
import numpy as np
import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from sklearn import preprocessing

features = pd.read_csv('./temps.csv')

# 标签，要预测的温度的真实值
labels = np.array(features['actual'])

print(labels)
# 在特征中去掉标签
features = features.drop('actual', axis=1)

# 训练集每列名字单独保存，留备用
feature_list = list(features.columns)
print(feature_list)
# 转换成合适的格式
features = np.array(features)
print(features)
input_features = preprocessing.StandardScaler().fit_transform(features)

# 设置网络模型
input_size = input_features.shape[1]
hidden_size = 128
output_size = 1
batch_size = 16
my_nn = torch.nn.Sequential(
    torch.nn.Linear(input_size, hidden_size),
    torch.nn.Sigmoid(),
    torch.nn.Linear(hidden_size, output_size),
)

# 损失函数与优化器
cost = torch.nn.MSELoss(reduction='mean')
optimizer = torch.optim.Adam(my_nn.parameters(), lr=0.001)

# 训练网络模型
losses = []
for i in range(500):
    batch_loss = []
    # MINI-Batch方法来进行训练
    for start in range(0, len(input_features), batch_size):
        end = start + batch_size if start + \
            batch_size < len(input_features) else len(input_features)
        xx = torch.tensor(
            input_features[start:end], dtype=torch.float, requires_grad=True)
        yy = torch.tensor(labels[start:end],
                          dtype=torch.float, requires_grad=True)
        prediction = my_nn(xx)
        loss = cost(prediction, yy)
        optimizer.zero_grad()
        loss.backward(retain_graph=True)
        # 所有optimizer都实现了step()方法，它会更新所有的参数
        optimizer.step()
        batch_loss.append(loss.data.numpy())

    # 打印损失，每100轮打印一次
    if i % 100 == 0:
        losses.append(np.mean(batch_loss))
        print(i, np.mean(batch_loss), batch_loss)

x = torch.tensor(input_features, dtype=torch.float)
predict = my_nn(x).data.numpy()

# 转换日期格式
months = features[:, feature_list.index('month')]
days = features[:, feature_list.index('day')]
years = features[:, feature_list.index('year')]
dates = [str(int(year)) + '-' + str(int(month)) + '-' + str(int(day))
         for year, month, day in zip(years, months, days)]
dates = [datetime.datetime.strptime(date, '%Y-%m-%d') for date in dates]

# 创建一个表格来存日期和其对应的标签数值
true_data = pd.DataFrame(data={'date': dates, 'actual': labels})

# 同理，再创建一个来存日期和其对应的模型预测值
test_dates = [str(int(year)) + '-' + str(int(month)) + '-' + str(int(day))
              for year, month, day in zip(years, months, days)]
test_dates = [datetime.datetime.strptime(
    date, '%Y-%m-%d') for date in test_dates]
predictions_data = pd.DataFrame(
    data={'date': test_dates, 'prediction': predict.reshape(-1)})

# 绘制散点图
# matplotlib添加本地的支持中文的字体库，默认是英文的无法显示中文
matplotlib.rc("font", family='SimHei')
plt.figure(figsize=(12, 7), dpi=160)
# 真实值
plt.plot(true_data['date'], true_data['actual'], 'b+', label='真实值')
# 预测值
plt.plot(predictions_data['date'],
         predictions_data['prediction'], 'r+', label='预测值', marker='o')
plt.xticks(rotation=30, size=15)
plt.ylim(0, 50)
plt.yticks(size=15)

x_major_locator = MultipleLocator(3)
y_major_locator = MultipleLocator(5)
ax = plt.gca()
ax.xaxis.set_major_locator(x_major_locator)
ax.yaxis.set_major_locator(y_major_locator)
plt.legend(fontsize=15)

plt.ylabel('日最高温度', size=15)
plt.show()
