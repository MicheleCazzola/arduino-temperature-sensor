int count;
int num_measurements = 2000;
int measurements_per_group = 100;
double resistance_F = 978;           // ohm, DMM
double source_voltage = 4.85;           // V, usb 3.0
double somma;
double sommaD;
int PIN = A5;
int levels = 1024;
// Resistance parameters
double resistance_offset = 100.0;       // ohm (0°C value)
double linear_param = 3.9083E-3;        // (°C)^(-1)
double quadratic_param = -5.775E-7;     // (°C)^(-2)
// Measurements
int voltage_value;                      // V
double temperature;                     // °C


void printValues(int Dout, double t){

  Serial.print(Dout);
  Serial.print(',');
  Serial.print(t);
  Serial.print('\n');
 
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  analogReference(DEFAULT);
  count = 0;
  somma = 0.0;
  sommaD = 0.0;
}

void loop() {
  // put your main code here, to run repeatedly:
  if(count < num_measurements){
    voltage_value = analogRead(PIN);
    temperature = - (0.5 * linear_param / quadratic_param) -
      sqrt( 0.25 * linear_param * linear_param / (quadratic_param * quadratic_param) - (1.0 / (resistance_offset * quadratic_param)) * (resistance_offset + resistance_F - resistance_F * ((double)levels / ((double)voltage_value))));
  //printValues(voltage_value, temperature);
  
    somma += temperature;
    sommaD += (double)voltage_value;
    if((count+1) % measurements_per_group == 0){
      double t = somma / measurements_per_group;
      double d = sommaD / measurements_per_group;
      printValues(d, t);
      somma = 0.0;
      sommaD = 0.0;
    }    
    
    ++count;
    delay(1);
  }
  /*
  else{
    exit(0);  
  }*/
}
