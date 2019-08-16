import math

count = 0   #分数预测准确的句子对数
i = 1

f = open("weizhongtrain.txt",encoding='UTF-8')
T1_T1_kernel_path = open("T1-T1-kernel\\ST-CGRCT.txt",encoding='UTF-8')   # T1、T1句法树相似度值存储路径
T1_T2_kernel_path = open("T1-T2-kernel\\ST-CGRCT.txt",encoding='UTF-8')   # T1、T2句法树相似度值存储路径
T2_T2_kernel_path = open("T2-T2-kernel\\ST-CGRCT.txt",encoding='UTF-8')   # T2、T2句法树相似度值存储路径
T1_T1_SIM_path = open("T1-T1-SIM\\T1_T1_SIM.txt",encoding='UTF-8')    # T1、T1语义相似度值存储路径
T1_T2_SIM_path = open("T1-T2-SIM\\T1_T2_SIM.txt",encoding='UTF-8')  # T1、T2语义相似度值存储路径
T2_T2_SIM_path = open("T2-T2-SIM\\T2_T2_SIM.txt",encoding='UTF-8')   # T2、T2语义相似度值存储路径


'1000个句子对计算相似度'
while i <= 1000:
    line = f.readline()
    line = line.rstrip().split('\t')  # 先删除句尾再按‘\t’切割句子
    print(line)
    label = line[2]  # 标签

    each1 = T1_T1_kernel_path.readline()
    each1 = each1.rstrip().split('\t')  # 先删除句尾再按‘\t’切割句子
    x1 = float(each1[0])  #T1 T1树结构相似度值

    each2 = T1_T2_kernel_path.readline()
    each2 = each2.rstrip().split('\t')  # 先删除句尾再按‘\t’切割句子
    x2 = float(each2[0])  # T1 T2树结构相似度值

    each3 = T2_T2_kernel_path.readline()
    each3 = each3.rstrip().split('\t')  # 先删除句尾再按‘\t’切割句子
    x3 = float(each3[0])  # T2 T2树结构相似度值

    each4 = T1_T1_SIM_path.readline()
    each4 = each4.rstrip().split('\t')  # 先删除句尾再按‘\t’切割句子
    x4 = float(each4[0])  # T1 T1语义相似度值

    each5 = T1_T2_SIM_path.readline()
    each5 = each5.rstrip().split('\t')  # 先删除句尾再按‘\t’切割句子
    x5 = float(each5[0])  # T1 T2语义相似度值

    each6 = T2_T2_SIM_path.readline()
    each6 = each6.rstrip().split('\t')  # 先删除句尾再按‘\t’切割句子
    x6 = float(each6[0])  # T2 T2语义相似度值

    '标准化处理'
    K11 = x1+x4
    K12 = x2+x5
    K22 = x3+x6
    score = K12 / math.sqrt(K11 * K22)
    print('score:',score)

    if score >= 0.4:
        y = '1'
    else:
        y = '0'

    if y == label:
        count = count + 1

    print('ST-CGRCT句子相似度准确率:',(float(count))/(float(i)))
    i = i + 1

