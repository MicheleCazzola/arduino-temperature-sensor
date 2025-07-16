V_REF = {
    "nominal": 3,       # volt: valore nominale
    "value": None,         # volt: MISURARE CON DMM tra pin AREF(+) e GND(-) della scheda Arduino
    "error": None       # volt: CALCOLATO in seguito
}       # generatore di riferimento
V_REF["error"] = (0.004/100) * V_REF["value"] + (0.0007/100) * V_REF["nominal"]

S = 0.01            # V/K: sensibilità nominale
VALUES = 1024       # LSB: possibili valori numerici
D_OFF = {
    "value": None,      # LSB: MISURATO a vuoto
    "error": 0.5        # LSB
}
D_out_ref = {
    "value": None,      # LSB: LETTO a vista
    "error": 1          # LSB
}
ERROR_SENSOR = 2     # K: errore del sensore

# Guadagno del sistema
GAIN = {
    "value": (D_out_ref["value"] - D_OFF["value"]) / V_REF["value"],    # LSB/V: valore di guadagno
    "error": None                                                       # LSB/V: CALCOLATO in seguito
}
GAIN["error"] = D_out_ref["error"]/V_REF["value"] + D_OFF["error"]/V_REF["value"] + abs(D_OFF["value"] - D_out_ref["value"]) * V_REF["error"] / (GAIN["value"] * GAIN["value"])

# Input
fr = open('data.csv', "r")
fw = open('results.csv', "w")

D_out = list()
T = list()
for line in fr:
    linea = line[:-1].split(",")
    d_out = {
        "value": int(linea[0]),     # LSB
        "error": 1                  # LSB
    }
    D_out.append(d_out)
    T.append(int(linea[1]))

# Calcolo e output
error_T = list()
for i in range(len(D_out)):
    d_out = D_out[i]
    # Coefficienti di errore per propagazione incertezza
    coeff = {
        "D_out": 1.0 / (S * GAIN["value"]),
        "D_OFF": 1.0 / (S * GAIN["value"]),
        "GAIN": abs(D_OFF["value"] - d_out["value"]) / (S * GAIN["value"] * GAIN["value"])
    }

    error_T.append(coeff["D_out"] * d_out["error"] + coeff["D_OFF"] * D_OFF["error"] + coeff["GAIN"] * GAIN["error"] + ERROR_SENSOR)
    fw.write(str(T[i]) + ',' + str(error_T[-1]) + '\n')

fr.close()
fw.close()
