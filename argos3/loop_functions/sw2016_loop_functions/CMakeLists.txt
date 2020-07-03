link_directories(${CMAKE_BINARY_DIR}/controllers/footbot_sw2016)

set(sw2016_loop_functions_SOURCES sw2016_loop_functions.h sw2016_loop_functions.cpp)

add_library(sw2016_loop_functions MODULE  ${sw2016_loop_functions_SOURCES})

target_link_libraries(sw2016_loop_functions
                       footbot_sw2016
							  argos3core_simulator
							  argos3plugin_simulator_entities
							  argos3plugin_simulator_footbot)

