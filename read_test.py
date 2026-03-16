
import numpy as np
from sklearn.preprocessing import StandardScaler
import pdb
flag="TRAIN"

labels = np.load("./DE_12k_4/TRAIN_labels.npy")
print("TRAIN_labels: {}".format(len(np.unique(labels))))

# for name in ["inputs", "labels", "ids"]:
for name in ["inputs"]:
    res = np.load("./DE_12k_4/{}_{}.npy".format(flag, name))
    # print(res[9000])
    sample = res[9000]
    sample = sample.squeeze()
    # print(sample)
    print(sample.shape)
    np.save('ng_sample', sample)
    print("{}_{} shape: {}".format(flag, name, res.shape))