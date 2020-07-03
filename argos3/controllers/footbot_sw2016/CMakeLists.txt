add_library(footbot_sw2016 SHARED footbot_sw2016.h footbot_sw2016.cpp CNode.h CNode.cpp CBlackBoard.h CBlackBoard.cpp)
target_link_libraries(footbot_sw2016
							 argos3core_simulator
							 argos3plugin_simulator_footbot
							 argos3plugin_simulator_genericrobot)
