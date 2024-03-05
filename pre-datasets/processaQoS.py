import os
import pandas as pd
from collections import defaultdict
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("nGat")
parser.add_argument("path")
parser.add_argument("tag")

args = parser.parse_args()
cwd = os.getcwd()
resFolder = "{}/".format(cwd) + args.path

gg = 0
g = int(args.nGat)
arqQosVazio = []
unsupportedDevs = 0
unreachedGateways = 0
numberOfFiles = 0
allDevsAndGat = 0

devMeanMethod = defaultdict(dict)
devPreDef = defaultdict(dict)
for d in range(10, 20, 10):  # devices 10, 20, 30, 40, 50
    devToMean = defaultdict(list)
    for s in range(1, 31):  # seeds 1..30
        # PROCESSA DELAY
        file_pDelay = resFolder + "/transmissionPackets_" + \
                      str(s) + "_" + str(g) + "x" + str(d) + ".dat"
        if os.path.isfile(file_pDelay):
            # REMOVE LINHAS CUJAS TRANSMISSÕES NÃO FORAM CONCLUIDAS
            dataDelay = pd.read_csv(file_pDelay, sep=" ",
                                    names=['device', 'gateway', 't_sent', 't_received', 't_elapsed'])
            dfDelay = pd.DataFrame(dataDelay)  # t.transmissao de todos devices por gateway
            index0 = dfDelay[dfDelay['t_received'] == 0].index
            dfDelay.drop(index0, inplace=True)

            # Verificar Gateways alcançados por algum pacote
            gg = dfDelay['gateway'].nunique()
            dd = dfDelay['device'].nunique()
            sd = ""
            numberOfFiles += 1
            if dd < d:
                sd = file_pDelay
                unsupportedDevs += 1

            if gg == g and dd == d:
                allDevsAndGat += 1

            # Verifica se o numero de gateways planejados não são efetivos
            # # (não são acessados por nenhum device)
            # caso ocorra, o arquivo de QoS não é gravado e este caso é desconsiderado.
            if gg < g:
                unreachedGateways += 1

            # DEFINE UMA LINHA POR DEVICE COM A MÉDIA DAS TRANSMISSÕES DESTE DEVICE
            dfDelay_a = dfDelay.groupby(['device'])['t_elapsed'].agg(['mean'])
            dfDelay_a.rename(columns={'mean': 'delay'}, inplace=True)

            # PROCESSA DATARATE
            file_pParam = resFolder + "/transmissionParameters_" + str(s) + "_" + str(
                g) + "x" + str(d) + ".dat"
            dataParam = pd.read_csv(file_pParam, sep=" ", names=['device', 'sf', 'tp', 'dr'])
            dfParam = pd.DataFrame(dataParam)
            # print(dfParam)
            # listDR = dfParam[['dr']]
            dfDR = pd.DataFrame(dfParam[['device', 'dr']])
            # print(dfQos_b) #DR para QoS

            # CALCULA QOS POR DEVICE
            dfQos = dfDR.join(dfDelay_a, on='device', how='left')
            dfQos.dropna(inplace=True)  # remove devices sem DR ou Delay
            dfQos['qos'] = dfQos['dr'] / 6835.94 + (1 - dfQos['delay'] / (400 / 183.11))

            # SEED, GATEWAYS EFETIVOS, DEVICES EFETIVOS, MÉDIA QOS, MÉDIA DELAY, MÉDIA DATARATE
            devToMean[g].append([s, gg, dd, dfQos['qos'].sum()/d, dfQos['delay'].sum()/d, dfQos['dr'].sum()/d])

            file_pQoS = resFolder + "/qosXdev_" + str(s) + "_" + str(
                g) + "x" + str(d) + "_" + args.tag + ".dat"
            if len(dfQos.index) == 0:
                arqQosVazio.append(file_pQoS)
            # DEVICE DATARATE DELAY QOS
            dfQos.to_csv(file_pQoS, header=False, sep=" ", index=False)
        # print("Gat: ", g)
    devPreDef[d] = devToMean
devMeanMethod['pre'] = devPreDef

# # Grava devices efetivos atendidos por n Gateways
# # Dataframe "Devices atendidos por n gateways" [d]
for mk, ml in devMeanMethod.items():
    for dk, dl in ml.items():
        for gk, gl in dl.items():
            # Agrupados por devices (10,20,30,40,50) e Gateways
            # SEED, GATEWAYS EFETIVOS, DEVICES EFETIVOS, MÉDIA QOS, MÉDIA DELAY, MÉDIA DATARATE
            # fileDM = resFolder + "/transmissionDevMeanHM_" + str(gk) + "x" + str(dk) + ".dat"
            # dfDM = pd.DataFrame(gl)
            # dfDM.to_csv(fileDM, mode='a', header=False, sep=" ", index=False)
            # Agrupados somente pelos gateways
            # SEED, GATEWAYS EFETIVOS, DEVICES EFETIVOS, MÉDIA QOS, MÉDIA DELAY, MÉDIA DATARATE
            fileHM = resFolder + "/qosXgw_" + str(gk) + "_" + args.tag + ".dat"
            dfHM = pd.DataFrame(gl)
            dfHM.to_csv(fileHM, mode='a', header=False, sep=" ", index=False)

print("Number of files: " + str(numberOfFiles))
print(" Unsupported Devices: " + str(unsupportedDevs))
print(" Unreached Gateways: " + str(unreachedGateways))
print(" All Devices & Gateways: " + str(allDevsAndGat))
print("Arquivos vazios: ")
print(arqQosVazio)
