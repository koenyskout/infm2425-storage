import paho.mqtt.client as mqtt
import json
import time
import random

# MQTT Broker Configuration
MQTT_BROKER = "mosquitto"
MQTT_PORT = 1883


# MQTT Client
class MQTTClient:
    def __init__(self, broker, port):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.connect(broker, port, 60)

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT broker with code {rc}")

    def publish(self, topic, payload):
        self.client.publish(topic, json.dumps(payload))

    def loop(self):
        self.client.loop_start()


# Water Level Sensor
class WaterLevelSensor:
    def __init__(self, sensor_id, initial_level=50.0):
        self.sensor_id = sensor_id
        self.water_level = initial_level

    def measure(self):
        noise = random.uniform(-0.5, 0.5)
        return max(0.0, min(100.0, self.water_level + noise))

    def update_level(self, delta):
        self.water_level = max(0.0, min(100.0, self.water_level + delta))


# Water Temperature Sensor
class WaterTemperatureSensor:
    def __init__(self, sensor_id, initial_temp=25.0):
        self.sensor_id = sensor_id
        self.temperature = initial_temp

    def measure(self):
        noise = random.uniform(-0.5, 0.5)
        return max(0.0, min(100.0, self.temperature + noise))

    def update_temperature(self, delta):
        self.temperature = max(0.0, min(100.0, self.temperature + delta))

    def get_id(self):
        return self.sensor_id


# Heater Actuator
class HeaterActuator:
    def __init__(self, actuator_id, initial_state="off"):
        self.actuator_id = actuator_id
        self.state = initial_state  # "on" or "off"

    def turn_on(self):
        self.state = "on"

    def turn_off(self):
        self.state = "off"


# Valve Actuator
class ValveActuator:
    def __init__(self, actuator_id, initial_state="closed"):
        self.actuator_id = actuator_id
        self.state = initial_state  # "open" or "closed"

    def open(self):
        self.state = "open"

    def close(self):
        self.state = "closed"


# PLC Logic to Manage Tank
class PLCLogic:
    def __init__(self, water_sensor, temp_sensor, inlet_valve, outlet_valve, heater, min_level, max_level, target_temp):
        self.water_sensor = water_sensor
        self.temp_sensor = temp_sensor
        self.inlet_valve = inlet_valve
        self.outlet_valve = outlet_valve
        self.heater = heater
        self.min_level = min_level
        self.max_level = max_level
        self.target_temp = target_temp

    def process(self):
        # Inlet valve control
        current_level = self.water_sensor.measure()
        if current_level <= self.min_level:
            self.inlet_valve.open()
        elif current_level >= self.max_level:
            self.inlet_valve.close()

        # Temperature Control
        current_temp = self.temp_sensor.measure()
        if current_temp < self.target_temp and \
            self.inlet_valve.state == 'closed' and \
            self.outlet_valve.state == 'closed':
            # heat when below target temperature and both valves are closed
            self.heater.turn_on()
        else:
            self.heater.turn_off()

        # Outlet valve control
        if current_temp >= self.target_temp:
            self.outlet_valve.open()
        else:
            self.outlet_valve.close()

        self.__simulate_physics_step()
    

    def __simulate_physics_step(self):
        if self.inlet_valve.state == "open":
            delta_level = random.uniform(2.0, 3.0)
            self.water_sensor.update_level(delta_level)  # inlet valve increases water level
            
            delta_temperature = -random.uniform(1.0, 5.0)
            self.temp_sensor.update_temperature(delta_temperature) # inlet valve adds cool water

        if self.outlet_valve.state == "open":
            self.water_sensor.update_level(-random.uniform(2.0, 3.0))  # outlet valve drains water
        
        if self.heater.state == "on":
            delta_temperature = random.uniform(3.0, 3.5)
            self.temp_sensor.update_temperature(delta_temperature)  # Heater warms water
        else:
            delta_temperature = -random.uniform(1.0, 2.0)
            self.temp_sensor.update_temperature(delta_temperature)  # Water slowly cools if not heated


# Main Simulation Loop
def simulation_loop():
    # Initialize components
    water_sensor = WaterLevelSensor(sensor_id="water_level_sensor_01", initial_level=0.0)
    temp_sensor = WaterTemperatureSensor(sensor_id="water_temp_sensor_01", initial_temp=25.0)
    inlet_valve = ValveActuator(actuator_id="inlet_valve_01", initial_state="closed")
    outlet_valve = ValveActuator(actuator_id="outlet_valve_01", initial_state="closed")
    heater = HeaterActuator(actuator_id="heater_actuator_01", initial_state="off")

    plc = PLCLogic(
        water_sensor,
        temp_sensor,
        inlet_valve,
        outlet_valve,
        heater,
        min_level=30.0,
        max_level=70.0,
        target_temp=80.0,
    )
    mqtt_client = MQTTClient(MQTT_BROKER, MQTT_PORT)
    mqtt_client.loop()

    # Simulation loop
    while True:
        site = "site1"

        # Update PLC logic
        plc.process()

        # Publish sensor data
        mqtt_client.publish(f"factory/{site}/sensor/{water_sensor.sensor_id}/water_level", {
            "value": water_sensor.measure(),
            "unit": "cm",
        })
        mqtt_client.publish(f"factory/{site}/sensor/{temp_sensor.sensor_id}/temperature", {
            "value": temp_sensor.measure(),
            "unit": "°C",
        })

        # Publish actuator statuses
        mqtt_client.publish(f"factory/{site}/actuator/{inlet_valve.actuator_id}/status", {
            "state": inlet_valve.state,
        })
        mqtt_client.publish(f"factory/{site}/actuator/{outlet_valve.actuator_id}/status", {
            "state": outlet_valve.state,
        })
        mqtt_client.publish(f"factory/{site}/actuator/{heater.actuator_id}/status", {
            "state": heater.state,
        })

        # Wait 1 second
        time.sleep(1)

if __name__ == "__main__":
    simulation_loop()
