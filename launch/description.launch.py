import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription, conditions
from launch.substitutions import Command, LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

output_dest = "log"

def generate_launch_description():
  pkg_traethlin_description = get_package_share_directory('traethlin_description')

  traethlin_urdf = Command(['xacro', ' ', os.path.join(pkg_traethlin_description,
                                                      'urdf',
                                                      'traethlin.urdf.xacro')])

  robot_state_publisher = Node(
    package='robot_state_publisher',
    executable='robot_state_publisher',
    name='robot_state_publisher',
    parameters=[{
      'robot_description': traethlin_urdf
      }],
    output={"both": output_dest},
    arguments=['--ros-args', '--log-level', 'DEBUG'],
    respawn=True
    )


  joint_state_publisher = Node(
    package='joint_state_publisher',
    name='joint_state_publisher',
    executable='joint_state_publisher',
    output={"both": output_dest},
    arguments=['--ros-args', '--log-level', 'DEBUG'],
    respawn=True
    )

  return LaunchDescription([
    robot_state_publisher,
    joint_state_publisher,
  ])
