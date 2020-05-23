"""

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18Ko8j_G5rLUf_b0s_6z7ah5WOEhPAv18
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms

# Set hyperparameters as described in question 2
train_batch_size = 128
test_batch_size = 1000
learning_rate = 0.005
epochs = 30
device = torch.device("cuda")

# Read dataset via Pytorch and apply normalization to accelerate training
transform = transforms.Compose([transforms.ToTensor()])

dataset = datasets.FashionMNIST('../data', train=True, download=True, transform=transform)

# Split dataset into train and validation 
train_set, valid_set = torch.utils.data.random_split(dataset, [int(len(dataset)*0.8), int(len(dataset)*0.2)])

train_loader = torch.utils.data.DataLoader(train_set, batch_size=train_batch_size, shuffle=True)

valid_loader = torch.utils.data.DataLoader(valid_set, batch_size=test_batch_size, shuffle=True)

test_loader = torch.utils.data.DataLoader(
        datasets.FashionMNIST('../data', train=False, transform=transform),
                              batch_size=test_batch_size, shuffle=True)

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        # Input Channel=1, output channel=32
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3)

        # Set kernel_size=2 and stride=2 such that output images are 12*12
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # Add dropout operation
        self.drop_out1 = nn.Dropout(0.2)

        # Input Channel=32, output channel=16
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3)

        # Set kernel_size=2 and stride=2 such that output images are 8*8
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        # Add dropout operation
        self.drop_out2 = nn.Dropout(0.5)

        self.fc1 = nn.Linear(64 * 5 * 5, 512)
        self.fc2 = nn.Linear(512, 128)
        self.output_layer = nn.Linear(128, 10)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool1(x)
        x = self.drop_out1(x)
        x = F.relu(self.conv2(x))
        x = self.pool2(x)
        x = self.drop_out2(x)
        x = x.view(-1, 64 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        logits = self.output_layer(x)
        output = F.log_softmax(logits, dim=1)
        return output

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        # Input Channel=1, output channel=32
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3)

        # Set kernel_size=2 and stride=2 such that output images are 12*12
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # Add dropout operation
        self.drop_out1 = nn.Dropout(0.2)

        # Input Channel=32, output channel=16
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3)

        # Set kernel_size=2 and stride=2 such that output images are 8*8
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)

        # Add dropout operation
        self.drop_out2 = nn.Dropout(0.5)

        self.fc1 = nn.Linear(64 * 5 * 5, 512)
        self.fc2 = nn.Linear(512, 128)
        self.output_layer = nn.Linear(128, 10)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool1(x)
        x = self.drop_out1(x)
        x = F.relu(self.conv2(x))
        x = self.pool2(x)
        x = self.drop_out2(x)
        x = x.view(-1, 64 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        logits = self.output_layer(x)
        output = F.log_softmax(logits, dim=1)
        return output

# Initialize the MLP model
CNN_model = CNN()

# Copy trainable variables to the spefied device (if using GPU)
CNN_model = CNN_model.to(device)

# Define a stochastic gradient optimizer with learning rate=0.005
'''
Since Vanilla SGD is sensitive to learning rate, I changed it to 
another SGD algorithm 'Adam' in order to make model converged within 30 epochs.
'''
optimizer = optim.Adam(CNN_model.parameters(), lr=learning_rate)

def train(model, device, train_loader, optimizer):
    model.train()
    for batch_idx, (images, labels) in enumerate(train_loader):
        images, labels = images.to(device), labels.to(device)
        
        # Initialize gradients to zero
        optimizer.zero_grad()

        # Forward propagate images to compute loss
        output = model(images)
        loss = F.nll_loss(output, labels)

        # Backpropagate errors to compute gradients
        loss.backward()

        # Apply gradients to parameters
        optimizer.step()

        # Log
        if batch_idx % 100 == 0:
            print('{}/{}\tLoss: {:.6f}'.format(
                batch_idx * len(images), len(train_loader.dataset), 
                loss.item()))
            
def test(model, device, test_loader, if_print=True):
    model.eval()
    test_loss = 0
    correct_predictions = 0
    # No backpropagation in the evaluation phase
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(device), labels.to(device)

            # Forward test images to compute their predictions
            output = model(images)
            test_loss += F.nll_loss(output, labels, reduction='sum')
            predictions = torch.argmax(output, dim=1)

            # Calculate the number of correct predictions
            correct_predictions += torch.sum(torch.eq(predictions, labels))

    # Compute the average loss on each test sample
    test_loss = test_loss / len(test_loader.dataset)

    # Calculate the overall accuracy
    accuracy = 100. * correct_predictions / len(test_loader.dataset)

    # Log
    if if_print:
         print('\nValidation set: loss: {:.4f}, Accuracy: ({:.2f}%)\n'.format(
           test_loss.item(), accuracy.item()))
    return accuracy.item(), test_loss.item()

best_model_idx = 1
best_valid_loss = 100
test_accuracies = []

for epoch in range(1, epochs + 1):
    print('Epoch {}, training.....'.format(epoch))
    train(CNN_model, device, train_loader, optimizer)

    # evaluate model on validation dataset
    _, current_loss = test(CNN_model, device, valid_loader)

    # evaluate model on test dataset
    test_accuracies.append(test(CNN_model, device, test_loader, if_print=False)[0])

    # Record which model is obtained with the lowest loss on validation set
    if current_loss < best_valid_loss:
        best_model_idx = epoch
        best_valid_loss = current_loss
    print('Current best model is in epoch {}'.format(best_model_idx))
    print('################################')

print('Best model obtained via validation dataset at epoch {}'.format(best_model_idx))
print('Test accuracy on this model is {:.2f}%'.format(test_accuracies[best_model_idx-1]))


