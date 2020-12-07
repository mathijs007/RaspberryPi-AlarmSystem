# Project 11

> An alarmsytem that checks the temperature, the motion and has a badge scanner while connected 
> with Azure

## Installation

Install the dependencies on the raspberry.

```sh
sudo pip3 install azure-iot-device  
sudo pip3 install azure-iot-hub  
sudo pip3 install azure-iothub-service-client  
sudo pip3 install azure-iothub-device-client 
```

## Usage

On the azure cloud shell:
```sh
az extension add --name azure-cli-iot-ext
az iot hub monitor-events --hub-name IoTAlarm --device-id IotDevice
```