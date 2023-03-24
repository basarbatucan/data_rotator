import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys

# functions
def rotate_matrix(theta_deg):
    theta = np.radians(theta_deg)
    c, s = np.cos(theta), np.sin(theta)
    R = np.array(((c, -s), (s, c)))
    return R

if len(sys.argv)==1:
    file_name="banana.csv"
else:
    file_name = sys.argv[1]

# TODO add check here
input_data = pd.read_csv("./" + file_name)

means = [[0,-5], [5,0], [0,5]]
row_n = 1
col_n = 1

# create new domain set with different means
d=0
output_data_01 = pd.DataFrame()
f,ax = plt.subplots(row_n, col_n, figsize=(15,8))
for mu in means:
    data_tmp = input_data.copy()
    data_tmp['domain'] = d
    data_tmp["X1"] = data_tmp["X1"] + mu[1]
    data_tmp["X2"] = data_tmp["X2"] + mu[0]
    # concat
    output_data_01 = pd.concat([output_data_01, data_tmp], ignore_index=True)
    # increase domain index
    d=d+1
# plot
sns.scatterplot(data=output_data_01, x="X1", y="X2", hue="Y",
                    s=10, palette="deep", linewidth=0, alpha=0.7, ax=ax)
ax.grid()
plt.savefig("{}_with_different_means.png".format(file_name))
output_data_01.to_csv('./{}_with_different_means.csv'.format(file_name), index=False)


# create new domain set with different rotations
rotations = [0, 15, 30, 45, 60, 75, 90]
row_n = 2
col_n = 4
f,ax = plt.subplots(row_n, col_n, figsize=(40,20))
output_data_02 = pd.DataFrame()
k=0
for i in range(0, row_n):
    for j in range(0, col_n):
        if k==len(rotations):
            break
        rot_deg = rotations[k]
        k=k+1
        data_tmp = input_data.copy()
        data_tmp['rotation_degrees'] = rot_deg
        data_tmp[["X1", "X2"]] = np.matmul(data_tmp[["X1","X2"]].values, rotate_matrix(rot_deg))
        # plot
        sns.scatterplot(data=data_tmp, x="X1", y="X2", hue="Y",
                    s=10, palette="deep", linewidth=0, alpha=0.7, ax=ax[i,j])
        ax[i,j].grid()
        ax[i,j].set_xlim([-4,4])
        ax[i,j].set_ylim([-4,4])
        ax[i,j].set_title("Rotation degrees: {}".format(rot_deg))
        # concat
        output_data_02 = pd.concat([output_data_02, data_tmp], ignore_index=True)

plt.savefig("{}_with_different_rotations.png".format(file_name))
output_data_02.to_csv('./{}_with_different_rotations.csv'.format(file_name), index=False)