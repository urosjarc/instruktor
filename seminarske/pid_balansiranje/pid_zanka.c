
#include <Servo.h>
#define sensor A0

float meritev_dolzine(){
  float volti = analogRead(sensor)*5.0/1024;  // value from sensor * (5/1024)

  /** pretvorba iz voltov v centimetre preko zmerjene karakteristike senzorja */
  return (13.099*volti*volti - 50.588*volti + 58.77);
}

/**
 * Ta funkcija na podlagi referencne razdalije izracuna povprecno napako tako
 * da v obmocju <cas_merjenja> dobi <stevilo_vzorcev> ki jih povpreci...
 * V funkciji je tudi uporabljen delay ki zagotavlja da zajamemo vzorce v enakomernem casovnem
 * intervalu.
 */
float povprecna_napaka(float referenca, int cas_merjenja, int stevilo_vzorcev) {

    float napaka = 0;
    for(int i = 0;i<stevilo_vzorcev;i++){
        napaka += meritev_dolzine() - referenca;
        delay((int) cas_merjenja/stevilo_vzorcev);
    }
    napaka /= stevilo_vzorcev;

    return napaka;
}

/**
 * Ta funkcija omeji maksimalni zasuk servo motorja...
 * Maks in min meja je bila dolocena ekspirementalno.
 * Na koncu pa se pristeje k popravku se integral napake.
 * !!! Samo integral napake lahko poveca zasuk servo motorja izven omejitev !!!
 */
float omejitve_popravka(float popravek, float integral_napake){
  int maks_popravek = 1;
  int min_popravek = -1;

  if(popravek >= maks_popravek) popravek = maks_popravek;
  else if(popravek <= min_popravek) popravek = min_popravek;
  
  return popravek + integral_napake;
}

void print(float napaka, float i, float d){
  Serial.print(-napaka);
  Serial.print("\t");
  Serial.print("\t");
  Serial.print(i*10);
  Serial.print("\t");
  Serial.println(d*0.1);
}

Servo servo;

float referenca = 12;
float popravek;
float napaka = 0;
float prejsnja_napaka = 0;
float hitrost = 0;
float integral_napake = 0;

int stoparica = 0;
int cas_merjenja = 60; //waiting 20ms
int stevilo_meritev = 20;

// Koeficienti pid
float Kp = 0.5f;
float Ki = 1e-4f;
float Kd = 1e3f;

void setup() {

    Serial.begin(9600); // start the serial port
    servo.attach(9);
    servo.write(90);

    delay(5000);
    Serial.println("Napaka\tIntegral\tHitrost");
}

void loop() {
  /** Meritve clenov v pid zanki */
  napaka = povprecna_napaka(referenca, cas_merjenja, stevilo_meritev); //cas merjenja 60ms, stevilo vzorcev = 20 ...
  hitrost = (napaka - prejsnja_napaka) / cas_merjenja;
  integral_napake += napaka*cas_merjenja;

  /** V primeru da zogica gre preko referencne razdalije se integral napake resetira */
  if(integral_napake > 0 && napaka < 0 || integral_napake < 0 && napaka > 0)
    integral_napake = 0;

  /** Da se znebiva lokalnih minimumov in lokalnih maksimumov povecamo cas pri  */
  if(stoparica % cas_merjenja*3 == 0){
    print(napaka, Ki * integral_napake, Kd * hitrost);
  }

  /** Izracun in omejitve popravka */
  popravek = Kp * napaka + Ki * integral_napake + Kd * hitrost;
  popravek = omejitve_popravka(popravek, Ki * integral_napake);

  /** Uveljavitev rotacije servo motorja */
  servo.write(90 + popravek);

  /** Updajt prejsnje napake, casa */
  prejsnja_napaka = napaka;
  stoparica += cas_merjenja;

  /** Hard reset stoparice */
  if(stoparica > 1e4){
    stoparica = 0;
  }
}
