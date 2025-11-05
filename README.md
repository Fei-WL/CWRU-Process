# CWRU-Process
针对CWRU数据集的处理方法

## 文件说明
> col_name.py: 存储了数据文件的名称，以及对应需要提取的列名称，以字典的形式存储。

> process.py: 用于处理CWRU数据的程序。运行时传入参数，可决定是生成四分类数据还是十分类数据。参数说明如下：
> 
>> root_dir: 存放CWRU数据的根目录
>>
>> device: 设备源。FE: Fan End, DE: Driver End
>>
>> freq: 故障数据的采样率，12k, 48k。可用于区分文件目录。
>>
>> nclass: 分类数目，4分类或10分类
>>
>> input_len: 切分数据集时单个样本的切分长度
>>
>> stride: 步长，0-1区间

## 目录说明
数据太大，因此没有上传。有需要的可以从[此处下载](https://pan.baidu.com/s/1AAp14jdKFz7VtFLeImfG5g?pwd=nj9r)。此处给出raw_data目录中的目录结构，便于理解和运行。
```
raw_data
├─ Normal Baseline
│  ├─ normal_0.mat
│  ├─ normal_1.mat
│  ├─ normal_2.mat
│  └─ normal_3.mat
├─ 48k Drive End Bearing Fault Data
│  ├─ Outer Race
│  │  ├─ 0021
│  │  │  ├─ OR021@12_0.mat
│  │  │  ├─ OR021@12_1.mat
│  │  │  ├─ OR021@12_2.mat
│  │  │  ├─ OR021@12_3.mat
│  │  │  ├─ OR021@3_0.mat
│  │  │  ├─ OR021@3_1.mat
│  │  │  ├─ OR021@3_2.mat
│  │  │  ├─ OR021@3_3.mat
│  │  │  ├─ OR021@6_0.mat
│  │  │  ├─ OR021@6_1.mat
│  │  │  ├─ OR021@6_2.mat
│  │  │  └─ OR021@6_3.mat
│  │  ├─ 0014
│  │  │  ├─ OR014@6_0.mat
│  │  │  ├─ OR014@6_1.mat
│  │  │  ├─ OR014@6_2.mat
│  │  │  └─ OR014@6_3.mat
│  │  └─ 0007
│  │     ├─ OR007@12_0.mat
│  │     ├─ OR007@12_1.mat
│  │     ├─ OR007@12_2.mat
│  │     ├─ OR007@12_3.mat
│  │     ├─ OR007@3_0.mat
│  │     ├─ OR007@3_1.mat
│  │     ├─ OR007@3_2.mat
│  │     ├─ OR007@3_3.mat
│  │     ├─ OR007@6_0.mat
│  │     ├─ OR007@6_1.mat
│  │     ├─ OR007@6_2.mat
│  │     └─ OR007@6_3.mat
│  ├─ Inner Race
│  │  ├─ 0021
│  │  │  ├─ IR021_0.mat
│  │  │  ├─ IR021_1.mat
│  │  │  ├─ IR021_2.mat
│  │  │  └─ IR021_3.mat
│  │  ├─ 0014
│  │  │  ├─ IR014_0.mat
│  │  │  ├─ IR014_1.mat
│  │  │  ├─ IR014_2.mat
│  │  │  └─ IR014_3.mat
│  │  └─ 0007
│  │     ├─ IR007_0.mat
│  │     ├─ IR007_1.mat
│  │     ├─ IR007_2.mat
│  │     └─ IR007_3.mat
│  └─ Ball
│     ├─ 0021
│     │  ├─ B021_0.mat
│     │  ├─ B021_1.mat
│     │  ├─ B021_2.mat
│     │  └─ B021_3.mat
│     ├─ 0014
│     │  ├─ B014_0.mat
│     │  ├─ B014_1.mat
│     │  ├─ B014_2.mat
│     │  └─ B014_3.mat
│     └─ 0007
│        ├─ B007_0.mat
│        ├─ B007_1.mat
│        ├─ B007_2.mat
│        └─ B007_3.mat
├─ 12k Fan End Bearing Fault Data
│  ├─ Outer Race
│  │  ├─ 0021
│  │  │  ├─ OR021@3_1.mat
│  │  │  ├─ OR021@3_2.mat
│  │  │  ├─ OR021@3_3.mat
│  │  │  └─ OR021@6_0.mat
│  │  ├─ 0014
│  │  │  ├─ OR014@3_0.mat
│  │  │  ├─ OR014@3_1.mat
│  │  │  ├─ OR014@3_2.mat
│  │  │  ├─ OR014@3_3.mat
│  │  │  └─ OR014@6_0.mat
│  │  └─ 0007
│  │     ├─ OR007@12_0.mat
│  │     ├─ OR007@12_1.mat
│  │     ├─ OR007@12_2.mat
│  │     ├─ OR007@12_3.mat
│  │     ├─ OR007@3_0.mat
│  │     ├─ OR007@3_1.mat
│  │     ├─ OR007@3_2.mat
│  │     ├─ OR007@3_3.mat
│  │     ├─ OR007@6_0.mat
│  │     ├─ OR007@6_1.mat
│  │     ├─ OR007@6_2.mat
│  │     └─ OR007@6_3.mat
│  ├─ Inner Race
│  │  ├─ 0021
│  │  │  ├─ IR021_0.mat
│  │  │  ├─ IR021_1.mat
│  │  │  ├─ IR021_2.mat
│  │  │  └─ IR021_3.mat
│  │  ├─ 0014
│  │  │  ├─ IR014_0.mat
│  │  │  ├─ IR014_1.mat
│  │  │  ├─ IR014_2.mat
│  │  │  └─ IR014_3.mat
│  │  └─ 0007
│  │     ├─ IR007_0.mat
│  │     ├─ IR007_1.mat
│  │     ├─ IR007_2.mat
│  │     └─ IR007_3.mat
│  └─ Ball
│     ├─ 0021
│     │  ├─ B021_0.mat
│     │  ├─ B021_1.mat
│     │  ├─ B021_2.mat
│     │  └─ B021_3.mat
│     ├─ 0014
│     │  ├─ B014_0.mat
│     │  ├─ B014_1.mat
│     │  ├─ B014_2.mat
│     │  └─ B014_3.mat
│     └─ 0007
│        ├─ B007_0.mat
│        ├─ B007_1.mat
│        ├─ B007_2.mat
│        └─ B007_3.mat
└─ 12k Drive End Bearing Fault Data
   ├─ Outer Race
   │  ├─ 0021
   │  │  ├─ OR021@12_0.mat
   │  │  ├─ OR021@12_1.mat
   │  │  ├─ OR021@12_2.mat
   │  │  ├─ OR021@12_3.mat
   │  │  ├─ OR021@3_0.mat
   │  │  ├─ OR021@3_1.mat
   │  │  ├─ OR021@3_2.mat
   │  │  ├─ OR021@3_3.mat
   │  │  ├─ OR021@6_0.mat
   │  │  ├─ OR021@6_1.mat
   │  │  ├─ OR021@6_2.mat
   │  │  └─ OR021@6_3.mat
   │  ├─ 0014
   │  │  ├─ OR014@6_0.mat
   │  │  ├─ OR014@6_1.mat
   │  │  ├─ OR014@6_2.mat
   │  │  └─ OR014@6_3.mat
   │  └─ 0007
   │     ├─ OR007@12_0.mat
   │     ├─ OR007@12_1.mat
   │     ├─ OR007@12_2.mat
   │     ├─ OR007@12_3.mat
   │     ├─ OR007@3_0.mat
   │     ├─ OR007@3_1.mat
   │     ├─ OR007@3_2.mat
   │     ├─ OR007@3_3.mat
   │     ├─ OR007@6_0.mat
   │     ├─ OR007@6_1.mat
   │     ├─ OR007@6_2.mat
   │     └─ OR007@6_3.mat
   ├─ Inner Race
   │  ├─ 0028
   │  │  ├─ IR028_0.mat
   │  │  ├─ IR028_1.mat
   │  │  ├─ IR028_2.mat
   │  │  └─ IR028_3.mat
   │  ├─ 0021
   │  │  ├─ IR021_0.mat
   │  │  ├─ IR021_1.mat
   │  │  ├─ IR021_2.mat
   │  │  └─ IR021_3.mat
   │  ├─ 0014
   │  │  ├─ IR014_0.mat
   │  │  ├─ IR014_1.mat
   │  │  ├─ IR014_2.mat
   │  │  └─ IR014_3.mat
   │  └─ 0007
   │     ├─ IR007_0.mat
   │     ├─ IR007_1.mat
   │     ├─ IR007_2.mat
   │     └─ IR007_3.mat
   └─ Ball
      ├─ 0028
      │  ├─ B028_0.mat
      │  ├─ B028_1.mat
      │  ├─ B028_2.mat
      │  └─ B028_3.mat
      ├─ 0021
      │  ├─ B021_0.mat
      │  ├─ B021_1.mat
      │  ├─ B021_2.mat
      │  └─ B021_3.mat
      ├─ 0014
      │  ├─ B014_0.mat
      │  ├─ B014_1.mat
      │  ├─ B014_2.mat
      │  └─ B014_3.mat
      └─ 0007
         ├─ B007_0.mat
         ├─ B007_1.mat
         ├─ B007_2.mat
         └─ B007_3.mat
```
一级目录根据[CWRU官网](https://engineering.case.edu/bearingdatacenter/download-data-file)中的链接进行划分。

二级目录根据故障类型进行划分，即Ball, Inner Race, Outer Race

三级目录根据直径划分，即0.007, 0.014, 0.021, 0.028

*.mat文件的名称根据官网中的数据进行了命名，更加直观

## 运行说明
```
python process.py --nclass 4 --device FE --input_len 512 --stride 0.5
```

## 额外说明
本数据处理方法是为了使用[BasicTS](https://github.com/GestaltCogTeam/BasicTS)做时序分类，因此增加了description文件，可根据需要删除。