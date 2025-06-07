from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration, Command
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    # Package paths
    pkg_serial = get_package_share_directory('serial_driver')
    pkg_drive_model = get_package_share_directory('meamr_drive_model')
    pkg_description = get_package_share_directory('meamr_description')
    pkg_joystick = get_package_share_directory('meamr_joystick')

    # Launch file paths
    launch_serial_path = os.path.join(pkg_serial, 'launch', 'serial_driver_bridge_node.launch.py')
    launch_drive_model_path = os.path.join(pkg_drive_model, 'launch', 'meamr_base.launch.py')
    launch_joystick_path = os.path.join(pkg_joystick, 'launch', 'meamr_joystick.launch.py')

    # Other paths (urdf, config, etc.)
    serial_config_path = os.path.join(pkg_drive_model, 'config', 'serial.yaml')
    urdf_path = os.path.join(pkg_description, 'urdf', 'meamr.urdf.xacro')

    # Nodes
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': Command(['xacro ', urdf_path])}],
        output='log',
        arguments=['--ros-args', '--log-level', 'error']
    )
    
    # Declare arguments
    declare_urdf = DeclareLaunchArgument(
        name='model', 
        default_value=urdf_path,
    )

    # Include launch descriptions
    serial_driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(launch_serial_path),
        launch_arguments={
            'params_file': serial_config_path,
        }.items()
    )

    meamr_drive_model_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(launch_drive_model_path)
    )

    meamr_joystick_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(launch_joystick_path)
    )

    ld = LaunchDescription()
    # Arguments
    ld.add_action(declare_urdf)
    # Nodes and included launch files
    ld.add_action(serial_driver_launch)
    ld.add_action(meamr_drive_model_launch)
    # ld.add_action(meamr_joystick_launch)
    
    ld.add_action(robot_state_publisher_node)


    return ld
