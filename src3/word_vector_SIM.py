import os
import numpy as np
from gensim.models import KeyedVectors
import pkuseg

EMBEDDING_DIM = 128
cur = '/'.join(os.path.abspath(__file__).split('/')[:-1])
train_path = os.path.join(cur, 'weizhongtrain.txt')  # 数据集存储路径
vocab_path = os.path.join(cur, 'T1_T2_SIM.txt')  #相似度表存储路径


'''
cur = '/'.join(os.path.abspath(__file__).split('/')[:-1])
embedding_file = os.path.join(cur, 'token_vec_300.bin')  # 字向量文件存储路径
vocabs = []
embedding_vector = []
with open(embedding_file, 'r', encoding='UTF-8')as f:
    for line in f:
        values = line.strip().split(' ')
        if len(values) < 300:  # 词向量维数小于300抛弃
            continue
        word = values[0]  # 字符
        vocabs.append(word)
        coefs = np.asarray(values[1:], dtype='float32')  # 数字码
        embedding_vector.append(coefs)
print('Found %s word vectors.' % len(vocabs))  # 发现有多少个字向量
'''


word2vec_model_path = 'baike_26g_news_13g_novel_229g.bin'    #词向量存储路径
print("Loading word2vec model(it may takes 2-3 mins) ...")
word2vec_model = KeyedVectors.load_word2vec_format(word2vec_model_path, binary=True)
word2vec_dict = {}
for word, vector in zip(word2vec_model.vocab, word2vec_model.vectors):
    if '.bin' not in word2vec_model_path:
        word2vec_dict[word] = vector
    else:
        word2vec_dict[word] = vector /np.linalg.norm(vector)


def word_vector_SIM(t1_leaves_list,t2_leaves_list):
    j = 0
    for word in t1_leaves_list:
        for each in word2vec_dict:
            if word == each:
                j = j + 1
                continue
    word1_vector_matrix = np.zeros((j,EMBEDDING_DIM))
    j = 0
    for word in t1_leaves_list:
        for each in word2vec_dict:
            if word == each:
                word1_vector_matrix[j] = word2vec_dict[each]
                j = j+1
                continue
    #print('word1_vector_matrix:', word1_vector_matrix)

    i = 0
    for word in t2_leaves_list:
        for each in word2vec_dict:
            if word == each:
                i = i + 1
                continue
    word2_vector_matrix = np.zeros((i, EMBEDDING_DIM))
    i = 0
    for word in t2_leaves_list:
        for each in word2vec_dict:
            if word == each:
                word2_vector_matrix[i] = word2vec_dict[each]
                i = i+1
                continue
    #print('word2_vector_matrix:',word2_vector_matrix)
    cosine_dis = cosine_distance(word1_vector_matrix,word2_vector_matrix)
    sum_sim = 0
    for i in range(len(cosine_dis)):
        for j in range(len(cosine_dis[i])):
            sum_sim = cosine_dis[i,j] + sum_sim
    #print('sum_sim:',sum_sim)
    return sum_sim

'向量矩阵余弦距离计算'
def cosine_distance(matrix1, matrix2):
    matrix1_matrix2 = np.dot(matrix1, matrix2.transpose())
    matrix1_norm = np.sqrt(np.multiply(matrix1, matrix1).sum(axis=1))
    matrix1_norm = matrix1_norm[:, np.newaxis]
    matrix2_norm = np.sqrt(np.multiply(matrix2, matrix2).sum(axis=1))
    matrix2_norm = matrix2_norm[:, np.newaxis]
    cosine_distance = np.divide(matrix1_matrix2, np.dot(matrix1_norm, matrix2_norm.transpose()))
    return cosine_distance


def text_save(filename, data):#filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(filename,'a')
    for i in range(len(data)):
        s = str(data[i])
        s = s +'\n'   #去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()
    print("保存文件成功")


'读取数据集，左右句子切分'
sum_sim_list = []
i = 1
for line in open(train_path, encoding='UTF-8-sig'):
    line = line.rstrip().split('\t')  # 先删除句尾再按‘\t’切割句子
    if not line:
        continue
    sent_left = line[0]  # 左边一句
    sent_right = line[1]  # 右边一句
    label = line[2]  # 标签
    print('左句：',sent_left)
    print('右句：', sent_right)
    lexicon = ['微信', '微粒贷','贷款','换了','还款','额度','逾期','开通','还了','花了','还清',
               '提额','扫一扫','打电话','综合','未通过','不通过','扣钱','借款','邀请','审批','提现']
    seg = pkuseg.pkuseg(user_dict=lexicon)
    Leaves_List1 = seg.cut(sent_left)
    Leaves_List2 = seg.cut(sent_right)
    sum_sim = word_vector_SIM(Leaves_List1, Leaves_List2)
    print(i)
    print('两个句子的词语间的语义相似度为:',sum_sim)
    sum_sim_list.append(sum_sim)
    if i == 1000:
        text_save(vocab_path,sum_sim_list)
        break
    i = i + 1