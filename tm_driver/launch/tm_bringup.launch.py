from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    tm_robot_ip = LaunchConfiguration('tm_robot_ip')
    tm_use_simulation = LaunchConfiguration('tm_use_simulation')
    no_logging = LaunchConfiguration('no_logging')

    declare_robot_ip = DeclareLaunchArgument(
        'tm_robot_ip',
        default_value='',
        description='Target robot IP address. Leave empty to run in fake mode unless tm_use_simulation is false and CLI fallback is used.',
    )

    declare_use_simulation = DeclareLaunchArgument(
        'tm_use_simulation',
        default_value='false',
        description='Run tm_driver in simulation/fake mode.',
    )

    declare_no_logging = DeclareLaunchArgument(
        'no_logging',
        default_value='false',
        description='Use the driver\'s direct console print functions instead of ROS logging.',
    )

    return LaunchDescription([
        declare_robot_ip,
        declare_use_simulation,
        declare_no_logging,
        Node(
            package='tm_driver',
            executable='tm_driver',
            output='screen',
            parameters=[{
                'tm_robot_ip': ParameterValue(tm_robot_ip, value_type=str),
                'tm_use_simulation': ParameterValue(tm_use_simulation, value_type=bool),
                'no_logging': ParameterValue(no_logging, value_type=bool),
            }],
        )
    ])