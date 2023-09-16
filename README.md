# Open-Source-Network-Protocol-for-Mobile-IoT
Open Source Network Protocol for IoT

Welcome to the repository for our research project aimed at developing an open-source network protocol for controlling, accessing, and managing robots and a collection of Internet of Things (IoT) devices deployed on a mobile platform. This protocol not only facilitates communication between a robot equipped with various IoT sensors and a controller but also allows multiple users anywhere on the Internet to access the onboard camera. With the availability of this open-source protocol, individuals and hobbyists will have the means to construct, deploy, and control robots equipped with sensors and tools, akin to those used in law enforcement, firefighting, and military applications, for tasks that are too dangerous for humans.

## Table of Contents
- [About](#about)
- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Materials](#materials)
- [Example Code](#example-code)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## About

Our research project addresses the development of an open-source network protocol to empower the control, access, and management of mobile IoT devices and robots. We aim to provide a solution that facilitates remote operation, access to sensory data, and real-time camera streaming. This project was undertaken as an effort to democratize the deployment of robots and IoT devices for various applications, including scenarios where human involvement is too risky.

## Project Overview

Our research project centers around the following objectives:
- **Protocol Development**: We have developed a custom network protocol tailored for mobile IoT devices and robot communication.
- **Remote Control**: Our protocol allows users to remotely control the robot, access sensor data, and operate onboard tools.
- **Camera Streaming**: Users from anywhere on the Internet can view the robot's onboard camera in real-time.
- **Open Source**: The protocol is open source, enabling individuals, hobbyists, and developers to build, customize, and enhance their mobile IoT devices and robots.

## Key Features

- **Custom Network Protocol**: Our protocol is designed specifically for mobile IoT devices, ensuring efficient communication.
- **Remote Control**: Users can send commands to control the robot and access sensor data remotely.
- **Real-Time Camera Streaming**: Multiple users can simultaneously access the robot's camera feed over the Internet.
- **Open Source**: The project is open source, allowing for contributions and customization.

## Materials

To replicate this project, you will need the following materials:

- [Raspberry Pi Car Kit](https://www.amazon.com/SunFounder-Raspberry-Graphical-Programming-Electronic/dp/B06XWSVLL8/ref=sr_1_10?hvadid=557458856046&hvdev=c&hvlocphy=9008533&hvnetw=g&hvqmt=e&hvrand=18160414894892081649&hvtargid=kwd-151905203777&hydadcr=18031_13447380&keywords=raspberry%2Bpi%2Bcar%2Bkit&qid=1694825605&sr=8-10&th=1)

This Raspberry Pi Car Kit will serve as the foundation for your mobile IoT device and robot project. It includes essential components for building and customizing your hardware platform.

## Example Code

You can find example Python source code and resources for the SunFounder PiCar-V in the [SunFounder_PiCar-V GitHub repository](https://github.com/sunfounder/SunFounder_PiCar-V). This repository contains code and documentation to help you get started with your Raspberry Pi car project.

Feel free to explore the repository for code samples, tutorials, and additional resources to enhance your project.


## Architecture

Our architecture employs a publisher-subscriber model, where the robot acts as a publisher of sensor data and camera streams, while the controller and remote users act as subscribers. This architecture ensures real-time communication and access to sensory information.

<img width="1082" alt="image" src="https://github.com/crudy002/Open-Source-Network-Protocol-for-Mobile-IoT/assets/80554884/1a63a585-8c5b-4401-b1b2-6fb8073aa1d1">

## Getting Started

To get started with our open-source network protocol and deploy it on your mobile IoT devices or robots, follow these steps:

1. Clone this repository: `git clone https://github.com/your-username/your-repo.git`
2. Navigate to the project directory: `cd your-repo`

## Usage

Once the protocol is installed and configured, you can begin using it to control your robots and access sensor data. 
<img width="1311" alt="image" src="https://github.com/crudy002/Open-Source-Network-Protocol-for-Mobile-IoT/assets/80554884/395876e3-4b44-4611-af5e-7c8a50c1c6e4">
<img width="486" alt="image" src="https://github.com/crudy002/Open-Source-Network-Protocol-for-Mobile-IoT/assets/80554884/ff916797-a19c-40a1-93f6-55973c9f9b04">


## Contributing

We welcome contributions from the open-source community to enhance and expand this project. To contribute, follow these steps:

1. Fork the repository and create a new branch for your contribution.
2. Make your changes and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

By contributing to this project, you agree to abide by the terms of this license.

We look forward to collaborating with you on this exciting journey of making mobile IoT devices and robot control accessible to all!

Feel free to customize this README to include specific details, links, or images relevant to your project. A comprehensive README will help others understand your project's goals, features, and how to get started.


