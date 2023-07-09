import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
# 定义网络模型


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, 3, 1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(16, 32, 3, 1)
        self.fc1 = nn.Linear(32 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x = self.pool(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = self.pool(x)
        x = x.view(-1, 32 * 5 * 5)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        return x


def main():
    # 训练模型
    fg, ax = plt.subplots()
    # plt.show()
    
    for epoch in range(5):  # 迭代5次
        # plt.close()
        line, = ax.plot([], [])
        ax.set_xlim(-1, 1000)
        ax.set_ylim(0, 2.5)
        running_loss = 0.0
        running = []
        time_i = []
        for i, data in enumerate(trainloader, 0):
            inputs, labels = data

            optimizer.zero_grad()

            outputs = net(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running.append(loss.item())
            time_i.append(i)
            
            running_loss += loss.item()
            print(i, running_loss, loss.item())
            # line.set_data(timestamps[:i+1], values[:i+1])
            if i % 200 == 199:  # 每200个mini-batches打印一次损失值
                print('[%d, %5d] loss: %.3f' %
                      (epoch + 1, i + 1, running_loss / 200))
                running_loss = 0.0
        for i in range(len(time_i)):

            line.set_data(time_i[:i+1], running[:i+1])
            # line1.set_data(timestamps[:i+1], dy[:i+1])
            plt.draw()
            plt.pause(0.01)
        plt.show()
        
    print('Finished training')

    # 在测试集上评估模型
    correct = 0
    total = 0
    with torch.no_grad():
        for data in testloader:
            images, labels = data
            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print('Accuracy on the test images: %d %%' % (100 * correct / total))


if __name__ == '__main__':
    # 设置随机种子，以便结果可复现

    torch.manual_seed(123)
    print(torch.manual_seed(123))
    # 加载训练数据集和测试数据集
    transform = transforms.Compose(
        [transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])

    trainset = torchvision.datasets.MNIST(
        root='./data', train=True, download=True, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=64,
                                              shuffle=True, num_workers=2)
    print(type(trainloader))

    testset = torchvision.datasets.MNIST(root='./data', train=False,
                                         download=True, transform=transform)
    testloader = torch.utils.data.DataLoader(testset, batch_size=64,
                                             shuffle=False, num_workers=2)

    classes = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')

    # 创建模型实例和优化器
    net = Net()
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
    main()
