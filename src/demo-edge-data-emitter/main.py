import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import MethodResponse
from aiomqtt import Client, MqttError
import random

MQTTBrokerIP = ""
MQTTPublisherClientName = "vm-lukas-virtual"

# Connect IoTHub Client to Hub and register direct commands
def create_client():
    try:
        # Fetch the connection string from an environment variable
        conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
        
        # Create instance of the device client using the authentication provider
        device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

        # Define behavior for handling methods
        async def method_request_handler(method_request):
            # Method to send a publishing event on the mqttBroker
            if method_request.name == "startSimulation":
                status = 200  # set return status code
                print(f"executed {method_request.name} with payload {method_request.payload}")
            # Method to send a stop event for publishing messages to the mqttBroker
            elif method_request.name == "stopSimulation":
                status = 200  # set return status code
                print(f"executed {method_request.name} with payload {method_request.payload}")
            else:
                status = 400  # set return status code
                print(f"executed unknown method: {method_request.name}")

            # Send the response
            method_response = MethodResponse.create_from_method_request(method_request, status, f"Direct command {method_request.name} executed.")
            await device_client.send_method_response(method_response)

        # Set the method request handler on the client
        device_client.on_method_request_received = method_request_handler
    except:
        print("error creating IoT Hub client.")
    return device_client

# MQTT publisher for simulation of sensor data - sends data for 10 times with random value between 1 and 50 while sleeping 1 sec
async def simulateSensor(payload):
    async with Client(MQTTBrokerIP, client_id=MQTTPublisherClientName) as client:
        while True:
            for plcEntry in payload["devices"]:
                for sensorEntry in payload[plcEntry]["sensors"]:
                    sensorValue = random.uniform(sensorEntry["startValue"], sensorEntry["endValue"])
                    sensorType = sensorEntry["sensor"]
                    await client.publish(f"sensors/{sensorType}", payload=sensorValue)
                    # TODO still some stuff to do here

async def main():
    try:
        # Connect the device client.
        device_client = create_client()
        await device_client.connect()
        print("Successfuly connected to IoT Hub.")
    except:
        print("Error connecting to IoT Hub.")

if __name__ == "__main__":
    asyncio.run(main())