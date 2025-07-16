V_FR = {
    "value": 4.85,  # volt
    "error": 0.4    # volt
}  # USB 3.0: valore ed errore dati dallo standard e dalle SPECIFICHE del PC utilizzato
S = 0.01            # V/K: sensibilità nominale
VALUES = 1024       # LSB: possibili valori numerici
ERROR_D_OUT = 2.5   # LSB: errore dell'ADC
ERROR_SENSOR = 2    # K: errore del sensore

fr = open('data.csv', "r")
fw = open('results.csv', "w")

D_out = list()
T = list()
for line in fr:
    linea = line[:-1].split(",")
    D_out.append(int(linea[0]))
    T.append(float(linea[1]))

# Calcolo errori e stampa su file csv
error_T = list()
for i in range(len(D_out)):
    error_T.append(V_FR["value"] * ERROR_D_OUT / (S * VALUES) + D_out[i] * V_FR["error"] / (S * VALUES) + ERROR_SENSOR)
    fw.write(str(D_out[i]) + ',' + str(T[i]) + ',' + str(error_T[-1])+'\n')

fr.close()
fw.close()
