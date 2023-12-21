import os
import asyncio
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import MethodResponse


async def main():
    # Fetch the connection string from an environment variable
    conn_str = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")

    # Create instance of the device client using the authentication provider
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

    try:
        # Connect the device client.
        await device_client.connect()
        print("Successfuly connected to IoT Hub.")
    except:
        print("Error connecting to IoT Hub.")

    # Define behavior for handling methods
    async def method_request_handler(method_request):
        if method_request.name == "startSimulation":
            status = 200  # set return status code
            print(f"executed {method_request.name} with payload {method_request.payload}")
        elif method_request.name == "stopSimulation":
            status = 200  # set return status code
            print(f"executed {method_request.name} with payload {method_request.payload}")
        else:
            payload = {"result": False, "data": "unknown method"}  # set response payload
            status = 400  # set return status code
            print("executed unknown method: " + method_request.name)

        # Send the response
        method_response = MethodResponse.create_from_method_request(method_request, status)
        await device_client.send_method_response(method_response)

    # Set the method request handler on the client
    device_client.on_method_request_received = method_request_handler

if __name__ == "__main__":
    asyncio.run(main())