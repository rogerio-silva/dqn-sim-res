import os

import matplotlib.pyplot as plt
import pandas as pd

nRun = 50

fig = plt.figure(figsize=(16, 9))
MAX_DELAY = 50 / 183.11
MIN_DELAY = 50 / 6835.94
QOS_BOUND = 1.3
MIN_TICKS = 2

path = "/home/rogerio/git/sim-res/datafile/"
pCompl = "/results/qos/"
pathFigs = "/home/rogerio/git/sim-res/datafile/figs/"
methods = {'do': 'density-oriented', 'un': 'uniform', 'eq': 'equidistant', 'op': 'optimized-oriented'}

# Achar pontos acima do bound
# {10dev: [xg, xic, xqos], 20dev: [yg, yic, yqos]... }

metohdsAboveQoSBound = {}
for mk, mv in methods.items():
    rowsAboveQoSBound = {10: [0, 0, 0], 20: [0, 0, 0], 30: [0, 0, 0], 40: [0, 0, 0],
                         50: [0, 0, 0], 60: [0, 0, 0], 70: [0, 0, 0], 80: [0, 0, 0],
                         90: [0, 0, 0], 100: [0, 0, 0]}
    metohdsAboveQoSBound[mk] = rowsAboveQoSBound
    for g in range(1, 51):
        if mk == 'op':
            file = path + mv + pCompl + "qos_" + str(g) + ".dat"
        else:
            file = path + "baseline/" + mv + pCompl + "qos_" + str(g) + ".dat"
        if os.path.isfile(file):
            dataQoS = pd.read_csv(file, sep=" ", names=['devices', 'qos', 'icq', 'dr', 'icdr', 'delay', 'icd'])
            dfQoS = pd.DataFrame(dataQoS)
            dfQoSAbUpBound = dfQoS.loc[dfQoS['qos'] > QOS_BOUND]
            for d in range(10, 110, 10):
                dfLinhaD = dfQoSAbUpBound[dfQoSAbUpBound['devices'] == d]
                if not dfLinhaD.empty and dfLinhaD['qos'].values[0] > rowsAboveQoSBound[d][0]:
                    tupla = [dfLinhaD['qos'].values[0], dfLinhaD['icq'].values[0], g]
                    rowsAboveQoSBound[d] = tupla
    metohdsAboveQoSBound[mk] = rowsAboveQoSBound
    # sorted_dfToPlotD[mk] = dict(sorted(dfToPlotD.items(), key=lambda x: x[1], reverse=True))
for mk, mv in methods.items():
    print(metohdsAboveQoSBound[mk])

styles = {'do': 'dashed', 'eq': 'dashdot', 'un': 'dotted', 'op': 'solid'}
for mk, mv in methods.items():
    devices = metohdsAboveQoSBound[mk].keys()
    qos = []
    gw = []
    ic = []
    for d in devices:
        qos.append(metohdsAboveQoSBound[mk][d][0])
        ic.append(metohdsAboveQoSBound[mk][d][1])
        gw.append(metohdsAboveQoSBound[mk][d][2])
    lStyle = styles[mk]
    plt.errorbar(devices, qos, ic, marker='s', ls=lStyle, label = mk,
                     markersize=12, capsize=6, elinewidth=2, lw=3, capthick=2)
# #
plt.legend(bbox_to_anchor=(-0.013, 1.1), ncol=6, loc='upper left', fontsize=20)
plt.xlabel('Number of Devices', fontsize=26)
plt.ylabel('Delay', fontsize=26)
plt.grid(axis='y')
plt.xlim([5, 105])
plt.yticks(fontsize=24)
plt.xticks(fontsize=24)
