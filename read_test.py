
import numpy as np
from sklearn.preprocessing import StandardScaler
import pdb
flag="TRAIN"

labels = np.load("./DE_12k_4/TEST_labels.npy")
print("TEST_labels: {}".format(len(np.unique(labels))))

for name in ["inputs", "labels", "ids"]:
    res = np.load("./DE_12k_4/{}_{}.npy".format(flag, name))
    pdb.set_trace()
    print("{}_{} shape: {}".format(flag, name, res.shape))