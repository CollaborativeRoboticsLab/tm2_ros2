# TM ROS 2

ROS 2 Humble packages for Techman robots, including the core driver, message definitions, robot descriptions, MoveIt configurations, Gazebo launches, image transport utilities, and a small inspection GUI.

This repository is the TM ROS 2 workspace for:

- connecting to a real TM robot through TMflow
- launching MoveIt for supported robot models
- running Gazebo simulation
- receiving TM vision images
- using the lightweight inspection GUI

For the detailed vendor walkthroughs, screenshots, and TMflow-specific setup notes, see the documents in [doc](./doc).

## Packages

- `tm_driver`: core robot driver
- `tm_msgs`: ROS interfaces used by the driver
- `tm_description`: URDF/Xacro robot models
- `tm_moveit`: MoveIt configurations for supported TM robots
- `tm_gazebo`: Gazebo simulation launches
- `tm_image`: TM vision image publisher support
- `image_sub`: simple image subscriber example
- `tm_inspect`: GUI for connection and message inspection
- `demo`: example client programs

## Supported robot variants

The MoveIt and Gazebo packages include launch files for:

- `tm5s`, `tm6s`, `tm7s`, `tm12s`, `tm14s`, `tm20s`, `tm25s`, `tm30s`
- `tm5sx`, `tm6sx`, `tm7sx`, `tm12sx`, `tm14sx`, `tm20sx`, `tm25sx`, `tm30sx`

In the examples below, replace `<tm_robot_type>` with one of those names.

## Prerequisites

- Ubuntu with ROS 2 Humble installed
- TMflow configured on the robot controller
- Robot and PC on the same network
- A TMflow Listen node project running before starting the ROS driver

For a real robot connection, make sure:

1. The robot has a static IP address.
2. Your PC is on the same subnet and can ping the robot.
3. TMflow `Ethernet Slave` is configured and enabled.
4. A TMflow `Listen` task is running.

The full TMflow setup walkthrough is in [tm_humble.md](./doc/tm_humble.md).

## Build

Create or enter a ROS 2 workspace, clone this repository into `src`, install dependencies, and build:

```bash
source /opt/ros/humble/setup.bash
mkdir -p ~/tm2_ws/src
cd ~/tm2_ws/src
git clone -b humble https://github.com/TechmanRobotInc/tm2_ros2.git
cd ..
rosdep install --from-paths src --ignore-src -r -y
colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release
source install/setup.bash
```

If you add packages later or want a clean rebuild:

```bash
cd ~/tm2_ws
rm -rf build install log
source /opt/ros/humble/setup.bash
colcon build --cmake-args -DCMAKE_BUILD_TYPE=Release
source install/setup.bash
```

## Launch instructions

Source the workspace in every new terminal before running any command:

```bash
source /opt/ros/humble/setup.bash
cd ~/tm2_ws
source install/setup.bash
```

### Bring up the driver

Use this for a direct connection to a real robot through TMflow:

```bash
ros2 launch tm_driver tm_bringup.launch.py robot_ip:=192.168.10.2
```

The equivalent direct executable is:

```bash
ros2 run tm_driver tm_driver robot_ip:=192.168.10.2
```

### Launch MoveIt with a real robot

The MoveIt launch already starts the TM driver, so do not run a second driver in another terminal for the same robot IP.

```bash
ros2 launch <tm_robot_type>_moveit_config <tm_robot_type>_run_move_group.launch.py robot_ip:=192.168.10.2
```

Example:

```bash
ros2 launch tm12s_moveit_config tm12s_run_move_group.launch.py robot_ip:=192.168.10.2
```

### Launch MoveIt in simulation

```bash
ros2 launch <tm_robot_type>_moveit_config <tm_robot_type>_run_move_group.launch.py
```

Example:

```bash
ros2 launch tm12s_moveit_config tm12s_run_move_group.launch.py
```

### Launch Gazebo

```bash
ros2 launch tm_gazebo <tm_robot_type>_gazebo.launch.py
```

Example:

```bash
ros2 launch tm_gazebo tm12s_gazebo.launch.py
```

### Launch MoveIt with Gazebo

Simulation:

```bash
ros2 launch <tm_robot_type>_moveit_config <tm_robot_type>_run_move_group_gz.launch.py
```

Real robot with the Gazebo-integrated launch path:

```bash
ros2 launch <tm_robot_type>_moveit_config <tm_robot_type>_run_move_group_gz.launch.py robot_ip:=192.168.10.2 sim:=False
```

### Run the inspection GUI

```bash
ros2 launch tm_inspect tm_gui.launch.py
```

### Run TM vision image publisher and subscriber

Start the image bridge node:

```bash
ros2 run tm_image image_talker
```

In another terminal, view the received image stream:

```bash
ros2 run image_sub sub_img
```

TM vision setup on the robot side is documented in [tm_humble.md](./doc/tm_humble.md).

### Run demo programs

Examples in the `demo` package exercise services and motion commands exposed by the driver:

```bash
ros2 run demo demo_send_script
ros2 run demo demo_set_io
ros2 run demo demo_set_positions
```

See [tm_humble_demo.md](./doc/tm_humble_demo.md) for the full demo descriptions.

## Recommended workflow for a real robot

1. Configure networking and TMflow `Ethernet Slave` / `Listen` on the robot.
2. Verify connectivity with `ping <robot_ip>` from the ROS PC.
3. Start the driver with `tm_bringup.launch.py` or start the relevant MoveIt launch.
4. Use RViz, services, actions, or the demo nodes from a second terminal.

## Notes

- Running two TM drivers against the same robot IP is not supported.
- MoveIt real-robot launches can move the robot immediately. Use appropriate safety procedures.
- For Gazebo and MoveIt dependency details, see [tm_humble_extension.md](./doc/tm_humble_extension.md).
- For TM-specific kinematic parameter generation, see [tm_humble_description.md](./doc/tm_humble_description.md).
- For the inspection GUI, see [tm_humble_gui.md](./doc/tm_humble_gui.md).

## Documentation

- [tm_humble.md](./doc/tm_humble.md): TMflow setup, networking, listen node, and vision setup
- [tm_humble_demo.md](./doc/tm_humble_demo.md): demo programs
- [tm_humble_extension.md](./doc/tm_humble_extension.md): MoveIt and Gazebo usage
- [tm_humble_description.md](./doc/tm_humble_description.md): robot-specific description generation
- [tm_humble_gui.md](./doc/tm_humble_gui.md): inspection GUI
