'''
多头注意力的简单实现参考
'''
import torch
import math
from torch import nn

class MultiHeadAttention(nn.Moudle): # 这里继承了 PyTorch 的 nn.Module，表示它是一个可训练的神经网络模块
    def __init__(self, d_model, num_heads):
        '''
        d_model: 每个词向量的总维度
        num_heads: 注意力头的数量
        '''
        super(MultiHeadAttention, self).__init__()
        assert d_model % num_heads == 0  # "d_model" 必须能够被 num_heads 整除（因为每个头通常使用的是相同的维度）

        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads # 每个注意力头内部的特征维度（代码中默认d_q​=d_k​=d_v, 即每个头中 Query、Key、Value 的维度相同​）

        # 定义 Q, K, V 和输出的线性变换层
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)

    def scaled_dot_product_attention(self, Q, K, V, mask=None):
        # 1. 计算注意力得分
        attn_scores = torch.matmul(Q, K.transpose(-2, -1))/math.sqrt(self.d_k)

        # 2. 应用掩码(mask中，1表示允许关注，0表示禁止关注)
        if mask is not None:
            # 将掩码中为 0 的位置设置为一个非常小的负数，这样softmax后会接近0
            attn_scores = attn_scores.masked_fill(mask == 0, -1e9)

        # 3. 计算注意力权重(Softmax)
        attn_probs = torch.softmax(attn_scores, dim = -1)

        # 4. 加权求和（权重*V）
        output = torch.matmul(attn_probs, V)
        return output

    def split_heads(self, x):
        # 将输入 x 的形状 (batch_size, seq_length, d_model)
        # 变化为（batch_size, nume_heads, d_k）
        batch_size, seq_length, d_model = x.size()
        return x.view(batch_size, seq_length, self.num_heads, self.d_k).transpose(1,2)

    def combine_heads(self, x):
        # 将输入 x 的形状从 （batch_size, num_heads, seq_length, d_k)
        # 变回（batch_size, seq_length, d_model）
        batch_size, num_heads, seq_length, d_k = x.size()
        return x.transpose(1,2).contiguous().view(batch_size, seq_length, self.d_model)

    def forward(self, Q, K, V, mask=None):
        # 1. 对 Q, K, V 进行线性变化
        Q = self.split_heads(self.W_q(Q))
        K = self.split_heads(self.W_k(K))
        V = self.split_heads(self.W_v(V))

        # 2. 计算缩放点积注意力
        attn_output = self.scaled_dot_product_attention(Q, K, V, mask)

        # 3. 合并多头输出并进行最终的线性变换
        output = self.W_o(self.combine_heads(attn_output))
        return output
