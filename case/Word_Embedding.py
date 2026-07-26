import numpy as np

# 假设这些是已经通过神经网络学习到的简化了的二维词向量
embeddings = {
    'king': np.array([0.9, 0.8]),
    'queen': np.array([0.9,0.2]),
    'man': np.array([0.7,0.9]),
    'woman':np.array([0.7,0.3])
}

def consine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)  # 计算两个向量的点积
    norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2) # np.linalg.norm() 用于计算向量的 L2 范数（也就是几何意义上的向量长度）。
    return dot_product/norm_product

# king-man+woman
result_vec = embeddings["king"] - embeddings['man'] + embeddings['woman']

# 计算结果向量与 queen 的相似度
sim = consine_similarity(result_vec, embeddings['queen'])

print(f"king - man + woman 的结果向量: {result_vec}")
print(f"该结果与 'queen' 的相似度: {sim:.4f}")