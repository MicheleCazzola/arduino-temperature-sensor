from math import sqrt

R_F = {
    "nominal": 1000.0,
    "measured": 978,  # misurazione con DMM
    "error": None  # calcolo
}
D_out = {
    "value": None,  # input da file
    "error": 2.5  # da specifiche
}

sensorError = {
    "fixed": 0.3,
    "linear": 0.005,
    "value": None  # calcolo
}
sensorParameters = {
    "offset": 100,
    "linear": 3.9083E-3,
    "quadratic": -5.775E-7,
    "value": None
}
temperature = {
    "value": None,  # calcolo
    "error": None  # calcolo
}
LEVELS = 1024
THERMAL_RES = 100  # °C/W
SOURCE_VOLTAGE = 4.85  # V

R_F["error"] = (0.01 / 100) * R_F["measured"] + (0.001 / 100) * R_F["nominal"]

print(R_F["error"])

fr = open("input_single.csv", "r")
fw = open("output_single.csv", "w")

for line in fr:
    line = line.strip().split(",")
    D_out["value"], temperature["value"] = int(line[0]), float(line[1])

    R_F_used = R_F["measured"]

    sqr = (sensorParameters["linear"] ** 2) / (
            4 * (sensorParameters["quadratic"] ** 2)) \
          - (1 / (sensorParameters["offset"] * sensorParameters["quadratic"])) * (
                  sensorParameters["offset"] + R_F_used
                  - LEVELS * R_F_used / D_out["value"])
    c_Dout = abs(
        ((LEVELS / 2) * R_F_used) / (
                sensorParameters["offset"] * sensorParameters["quadratic"] * (D_out["value"] ** 2) * sqrt(sqr)))
    c_RF = abs((D_out["value"] - LEVELS) / (
            2 * sensorParameters["offset"] * sensorParameters["quadratic"] * D_out["value"] * sqrt(sqr)))
    sensorError["value"] = sensorError["fixed"] + sensorError["linear"] * abs(temperature["value"])

    temperature["error"] = c_Dout * D_out["error"] + c_RF * R_F["error"] + sensorError["value"]
    sensorParameters["value"] = sensorParameters["offset"] * (1 + sensorParameters["linear"] * temperature["value"] +
                                                              sensorParameters["quadratic"] * (
                                                                      temperature["value"] ** 2))
    self_heating = THERMAL_RES * (
            (SOURCE_VOLTAGE * sensorParameters["value"] / (sensorParameters["value"] + R_F_used)) ** 2) / \
                   sensorParameters["value"]

    # print(c_Dout, c_RF, sensorError["value"])
    fw.write(str(D_out['value']) + "," + str(temperature["value"]) + "," + str(temperature["error"]) + "," + str(
        self_heating) + "\n")

fr.close()
fw.close()
