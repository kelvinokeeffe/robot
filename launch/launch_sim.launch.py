import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

def generate_launch_description():

    #Include the robot_state_publisher launch file, provided by our own package. Force sim time to vbe enabled
    # !! Ensure that the package naem is set correctly !!

    package_name='robot'  #<--Change this to suit the package

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name), 'launch', 'rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    #Inculde the Gazebo Launch File, provided by the gaevo ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py'
                )]),
    )

    # Run the spawner node form the gazebo_ros package. Then entity name doesn't really matter if you only have a single robot
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'mobile_robot'],
                        output='screen')


    #Launch all together
    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity
    ])