#include <Arduino.h>

// CURRENT TRANSFORMER OUTPUT PIN
int CT_PIN = 32;

// POTIENTIAL TRANSFORMER OUTPUT PIN
int PT_PIN = 33;

void setup()
{
  // SERIAL MONITOR CONFIGURATION
  Serial.begin(115200);

  analogReadResolution(12);       // Set 12-bit resolution (0–4095)
  analogSetAttenuation(ADC_11db); // USE THE FULL 0.0V - 3.3 V
}

void main()
{

  int current_adc = analogRead(CT_PIN);
  int voltage_adc = analogRead(PT_PIN);

  // Convert to voltage
  float current_voltage = (3.3 / 4095.0) * current_adc + 0.150;
  float voltage_voltage = (3.3 / 4095.0) * voltage_adc;

  Serial.print("CT ADC: ");
  Serial.print(current_adc);
  Serial.print(" | CT Voltage: ");
  Serial.print(current_voltage);

  Serial.print(" || PT ADC: ");
  Serial.print(voltage_adc);
  Serial.print(" | PT Voltage: ");
  Serial.println(voltage_voltage);

  delay(500);
}
