#include <Arduino.h>

// ===== PINS =====
#define VOLTAGE_PIN 33
#define CT_PIN 32

// ===== SETTINGS =====
#define NUM_SAMPLES 500
#define VOLTAGE_SCALING 93.56   // Voltage calibration
#define CURRENT_SCALING 0.525     // Current calibration

void setup()
{
  Serial.begin(115200);

  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);
}

void loop()
{
  float sumSq_voltage = 0;

  // ===== Voltage RMS Calculation =====
  for (int i = 0; i < NUM_SAMPLES; i++)
  {
    int raw_voltage = analogRead(VOLTAGE_PIN);

    float voltage = (raw_voltage / 4095.0) * 3.3;

    sumSq_voltage += voltage * voltage;

    delayMicroseconds(5000);  // 200 Hz sampling
  }

  float Vrms_pin = sqrt(sumSq_voltage / NUM_SAMPLES);
  float Vrms_mains = Vrms_pin * VOLTAGE_SCALING;

  // ===== Current Calculation =====
  int current_adc = analogRead(CT_PIN);
  float current_voltage = (3.3 / 4095.0) * current_adc;
  float current_actual = current_voltage * CURRENT_SCALING;

  // ===== Rounding to 1 Decimal Place =====
  float current_rounded = round(current_actual * 10) / 10.0;

  // ===== Output =====
  Serial.print("Mains Voltage: ");
  Serial.print(Vrms_mains, 1);
  Serial.print(" V | Current: ");
  Serial.print(current_rounded, 1);
  Serial.println(" A");

  delay(1000);
}
