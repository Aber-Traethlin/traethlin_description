cmake_minimum_required(VERSION 3.5)
project(traethlin_description)

find_package(ament_cmake)

install(DIRECTORY
  urdf
  rviz
  launch
  meshes
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
