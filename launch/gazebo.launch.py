import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription, conditions
from launch.substitutions import Command, LaunchConfiguration
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch_ros.actions import Node

output_dest = "log"

def generate_launch_description():
  pkg_traethlin_description = get_package_share_directory('traethlin_description')

  traethlin_urdf = Command(['xacro', ' ', os.path.join(pkg_traethlin_description,
                                                      'urdf',
                                                      'traethlin.urdf.xacro')])

  namespace_ = LaunchConfiguration('namespace')

  namespace_launch_arg = DeclareLaunchArgument(
    'namespace',
    default_value='traethlin'
  )

  world_file_name = 'traethlin.world'
  world = os.path.join(pkg_traethlin_description, 'worlds', world_file_name)

  robot_state_publisher = Node(
    package='robot_state_publisher',
    executable='robot_state_publisher',
    name='robot_state_publisher',
    namespace=namespace_,
    parameters=[{
      'robot_description': traethlin_urdf
      }],
    output={"both": output_dest},
    arguments=['--ros-args', '--log-level', 'WARN'],
    respawn=True
    )


  joint_state_publisher = Node(
    package='joint_state_publisher',
    name='joint_state_publisher',
    executable='joint_state_publisher',
    namespace=namespace_,
    output={"both": output_dest},
    arguments=['--ros-args', '--log-level', 'WARN'],
    respawn=True
    )

  return LaunchDescription([
    namespace_launch_arg,

    ExecuteProcess(
            cmd=['gazebo', '--verbose', world, '-s', 'libgazebo_ros_factory.so'],
            output='screen'),

    robot_state_publisher,

    joint_state_publisher,

    Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='urdf_spawner',
        output='screen',
        arguments=["-robot_namespace", namespace_,
                   "-topic", ["/", namespace_, "/robot_description"],
                   "-entity", "traethlin"]
    )
  ])
