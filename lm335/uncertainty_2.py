V_int = {
    "nominal": 1.1,     # volt: valore nominale
    "value": 1.088,      # volt: MISURARE CON DMM tra pin AREF(+) e GND(-) della scheda Arduino
    "error": None       # volt: CALCOLATO A PARTIRE DA SPECIFICHE DMM
}  # internal
S = 0.01                # V/K: sensibilità nominale
VALUES = 1024           # LSB: possibili valori numerici
R2 = {
    "nominal": 27000,   # ohm: valore nominale
    "value": 26500,      # ohm: MISURARE CON DMM
    "error": None       # ohm: CALCOLATO A PARTIRE DA SPECIFICHE DMM
}
R3 = {
    "nominal": 10000,   # ohm: valore nominale
    "value": 9710,      # ohm: MISURARE CON DMM
    "error": None       # ohm: CALCOLATO A PARTIRE DA SPECIFICHE DMM
}
ERROR_SENSOR = 2        # K: errore del sensore

# Valori ricavati dalle specifiche del DMM di laboratorio
V_int["error"] = (0.004 / 100) * V_int["value"] + (0.0007 / 100) * 1
R2["error"] = (0.01 / 100) * R2["value"] + (0.001 / 100) * 100E3
R3["error"] = (0.01 / 100) * R3["value"] + (0.001 / 100) * 10E3

fr = open('data.csv', "r")
fw = open('results.csv', "w")

# Input
D_out = list()
T = list()
for line in fr:
    linea = line[:-1].split(",")
    d_out = {
        "value": int(linea[0]),     # LSB: LETTURA
        "error": 2.5                # LSB: errore dell'ADC
    }
    D_out.append(d_out)
    T.append(float(linea[1]))

# Calcolo e output
error_T = list()
for i in range(len(D_out)):
    d_out = D_out[i]

    # Coefficienti di errore per propagazione incertezza
    coeff = {
        "D_out": V_int["value"] * (1.0 + R2["value"] / R3["value"]) / (VALUES * S),
        "V_int": d_out["value"] * (1.0 + R2["value"] / R3["value"]) / (VALUES * S),
        "R2": d_out["value"] * V_int["value"] / (VALUES * S * R3["value"]),
        "R3": d_out["value"] * V_int["value"] * R2["value"] / (VALUES * S * R3["value"] * R3["value"])
    }

    error_T.append(
        coeff["D_out"] * d_out["error"] + coeff["V_int"] * V_int["error"] + coeff["R2"] * R2["error"] + coeff["R3"] *
        R3["error"] + ERROR_SENSOR)
    fw.write(str(d_out["value"]) + ',' + str(T[i]) + ',' + str(error_T[-1]) + '\n')

fr.close()
fw.close()
