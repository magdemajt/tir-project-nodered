# Irrigation System

### Project made by: Mateusz Wejman, Mateusz Mazur, Mikołaj Klimek, Karol Wrona

## Overview

This project was made for IoT classes on UST Cracow. The goal of this project was to create a software that can be used as a tool for monitoring the humidity of plant soil. The project was desinged for small devices like rasberry pi, however due to technical limitations we used Docker to simulate different parts of the system.

The application is composed of three different componnets:
- Dirtmodel - mockup of the soil and deivce with sensors that would measure dirt humidity
- Water Valve - a mockup of device that would control flow of the water, integrated in *Dirtmodel*
- Mqtt broker - in our case we used mosquitto, we use it to communicate between different components
- Node Red - an proggraming tool for wiring together software and hardware

Moreover, we implemneted an Node Red dashboard which will display all necessary information to the user and will alow him to control the Water Valve.

### How To Run Application

We provide an Docker Compose container that contains the entire application. In order to run it make sure that you have Docker Compose installed and type:

```
docker compose up -d
```

To interact with application proceede to https:localhost:1880/ui

### How to control the application

In dashboard user can turn on and off automatization of watering. If automatization works and water level is below water level set by user on slider, system turn on sprinkler. Watering is turned on, until water level exceed expected value. To avoid too frequent turning sprinkler, water level set by user have 5L margin. If automatization is switched off, user can manually switch on and off watering. When sprinkler is turned off, parameteres are updated onece in 8 seconds. After turned on the watering, user can see changes second by second.  

Inside dashboard view you can monitor the current wheater and the humidity inside the soil. Below the gauge you can see chart that will plot the water level for past 15 minutes (for production release the time interval would be bigger but for the sake of testing we decided to use 15 minute time window). In the top right corner, you will see a switch that will allow user to control the water valve.

#### PLZ wrzuccie tu zdjecie tego dashboardu

## Implementation

### DirtModel

DirtModel was implemented in Pyhton. In order to better the performance of our application, we used Python threading library to listen to mqqt msessages on another thread.

Our soil model is very advanced, it has multiple realitime parameters like: humus, looseness, volume and plant water absortion. All of them have the impact on how quickly the water will be evaporating and how much water the plant will absorb. Weather (temperature, air humidity and speed of wind) also can influence on water absorption.


Dirt model communicates with mqqt broker on topic *"brain"*

### Mqqt protocol

To communicate between different components we use Mqqt Protocol. For the mqqt broker we use Mosquitto implemntation.

### Node-Red

The rest of application logic was implemented in Node-Red flow diagram.

#### PLz wrzuccie tu zdjecie

Node red allows user to control the hardware through Node-Red-Dashboard which is plugin to the Node-Red service. The Node-Red server is self hosted and client can interact with it through web application.
