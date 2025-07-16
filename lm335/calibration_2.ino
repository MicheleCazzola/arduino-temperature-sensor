char REQUEST_MEASURE_CHAR = 'M';    /* carattere input per fornire misura */
float FULL_RANGE_VOLTAGE = 1.1;     /* tensione interna ADC (V) = V_FR */
int NUM_DIGITAL_VALUES = 1024.0;      /* numero di possibili valori digitali (ADC a 10 bit) = 2^N_bit */
float SENSITIVITY = 0.01;           /* sensibilità nominale sensore (V/K) = S */
float R2 = 27000.0, R3 = 10000.0;         /* resistori partitore */
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
      int voltageValue = analogRead(A5);
      float temperature = ((float)voltageValue * FULL_RANGE_VOLTAGE * (1.0 + R2/R3)) / (NUM_DIGITAL_VALUES * SENSITIVITY); /* funzione di taratura 2 */
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
