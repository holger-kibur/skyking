import torch.nn as nn
import torch

import base_kernel

def add_params(dest, layer):
    for param in layer.parameters():
        dest.append(param.data)

class DynamicVolumeKernel(base_kernel.BaseKernel):
    def __init__(self, kernel_size, channels):
        super().__init__(kernel_size)
        self.conv = nn.Conv1d(3, 9, 12)
        self.pool = nn.MaxPool1d(2)
        self.hidden = nn.Linear(9 * (self.kernel_size - 12) // 2, 64)
        self.dropout = nn.Dropout(0.2)
        self.out = nn.Linear(64, 5)

    def get(self):
        input_tensor = torch.transpose(torch.FloatTensor([self.buffer]), 1, 2)
        print(input_tensor)
        input_tensor = self.conv(input_tensor)
        input_tensor = self.pool(input_tensor)
        input_tensor = input_tensor.view(input_tensor.size(0), -1)
        print(input_tensor.size())
        input_tensor = nn.functional.relu(self.hidden(input_tensor))
        input_tensor = self.dropout(input_tensor)
        input_tensor = self.out(input_tensor)
        print(input_tensor)
        
    def set_kernel_size(self, kernel_size):
        raise EnvironmentError("Cannot change size of neural network kernel!")

    def get_weights(self):
        param_tensor_list = []
        add_params(tensor_list, self.conv)
        add_params(tensor_list, self.hidden)
        add_params(tensor_list, self.out)
        return param_tensor_list