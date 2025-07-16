char REQUEST_MEASURE_CHAR = 'M';    /* carattere input per fornire misura */
float D_OFFSET = 0;                 /* offset del sistema -> DA CARATTERIZZARE (LSB) */
float GAIN = 10;                    /* guadagno del sistema -> DA CATTERIZZARE (LSB/V) */
float SENSITIVITY = 0.01;           /* sensibilità nominale sensore (V/K) = S */
bool dataComplete;                  /* flag calcolo temperatura */


char toUpper(char c){
  return (isLowerCase(c)) ? c - 32 : c;
}

/* Stampa valori */
void printValues(int D_out, float T){
    Serial.print(D_out);
    Serial.print(",");
    Serial.print(T);
    Serial.print("\n");
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  analogReference(INTERNAL);
  dataComplete = false;
}

void loop() {
  // put your main code here, to run repeatedly:
  if(dataComplete){
      int voltageValue = analogRead(A0);
      float temperature = (voltageValue - D_OFFSET) / (GAIN * SENSITIVITY); /* funzione di taratura 2 */
      printValues(voltageValue, temperature);
      dataComplete = false;
  }
}

void serialEvent(){
  while (Serial.available() > 0){
    char inChar = Serial.read();
    if(toUpper(inChar) == REQUEST_MEASURE_CHAR and dataComplete == false){
      dataComplete = true;
    }
  }
}
