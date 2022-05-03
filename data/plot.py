#!/usr/bin/env python3
import pandas as pd
import math
import matplotlib.pyplot as plt
import seaborn as sns
import os

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.options.mode.chained_assignment = None 

df_plaintext = pd.read_csv('plaintext.expanded.csv.gz')
df_plaintext["encrypted"] = 0
df_plaintext = df_plaintext[df_plaintext["extension"] != ".webp"]

df_encrypted = pd.read_csv('expanded.pyencrypted_v1.csv.gz')
df_encrypted["encrypted"] = 1
df_encrypted = df_encrypted[df_encrypted["extension"] != ".webp"]

df_encrypted_base32 = pd.read_csv('expanded.pyencrypted_v1.b32.csv.gz')
df_encrypted_base32["encrypted"] = 1
df_encrypted_base32 = df_encrypted_base32[df_encrypted_base32["extension"] != ".webp"]

print(df_plaintext.columns)

plt.rcParams.update({'font.size': 32, 'figure.figsize': (30, 30)})
fig = plt.figure()
fig.subplots_adjust(left=0, right=.95, bottom=0, top=1)
ax = fig.add_subplot(projection='3d')
#ax.view_init(elev=(-45 / 360.0 * 2 * math.pi), azim=(66 / 360.0 * 2 * math.pi))
ax.view_init(azim=-29.0, elev=-80.0)

def scatter(ax, df, label):
    nrows = df.shape[0]
    df = df.sample(frac=(20000.0/nrows))
    df = df.drop("extension", axis=1)
    df = df.drop("filename", axis=1)
    df = (df - df.min()) / (df.max() - df.min())
    x = df["shannon_entropy"]
    y = df["montecarlo_pi"]
    z = df["autocorrelation"]
    ax.set_xlabel("Shannon's entropy")
    ax.set_ylabel(r"Monte-Carlo simulation of $\pi$")
    ax.set_zlabel("Autocorrelation")
    ax.scatter(x, y, z, marker='s', s=50, label=label)

scatter(ax, df_plaintext, "Plain text")
scatter(ax, df_encrypted, "Encrypted text")
scatter(ax, df_encrypted_base32, "Encrypted base-32 encoded text")

plt.legend()

os.system("rm -f foo.png")
#plt.show()
plt.savefig('foo.png')
os.system("open foo.png")

"""
Index(['Unnamed: 0', 'extension', 'filename', 'shannon_entropy',
       'montecarlo_pi', 'chisquare', 'autocorrelation', 'filesize',
       'encrypted'],
      dtype='object')
"""
