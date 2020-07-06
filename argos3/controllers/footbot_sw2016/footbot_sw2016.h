#ifndef FOOTBOT_SW2016_H
#define FOOTBOT_SW2016_H

#include <argos3/core/control_interface/ci_controller.h>
#include <argos3/plugins/robots/generic/control_interface/ci_differential_steering_actuator.h>
#include <argos3/plugins/robots/foot-bot/control_interface/ci_footbot_proximity_sensor.h>
#include <argos3/plugins/robots/generic/control_interface/ci_range_and_bearing_actuator.h>
#include <argos3/plugins/robots/generic/control_interface/ci_range_and_bearing_sensor.h>
#include <argos3/plugins/robots/generic/control_interface/ci_leds_actuator.h>
#include <argos3/plugins/robots/generic/control_interface/ci_positioning_sensor.h>

#include "CNode.h"


using namespace argos;

class CFootBotSW2016 : public CCI_Controller {

public:

   CFootBotSW2016();
   virtual ~CFootBotSW2016();

   virtual void Init(TConfigurationNode& t_node);
   virtual void ControlStep();
   virtual void Reset() {}
   virtual void Destroy() {}
   
   void buildTree(std::vector<std::string> tokens);
   void createBlackBoard(int numRobots);
   
   
private:

	void stop() {m_pcWheels->SetLinearVelocity(0.0f, 0.0f);}
	void goStraight() {m_pcWheels->SetLinearVelocity(m_fWheelVelocity, m_fWheelVelocity);}
	void turnLeft() {m_pcWheels->SetLinearVelocity(0.0f, m_fWheelVelocity);}
	void turnRight() {m_pcWheels->SetLinearVelocity(m_fWheelVelocity, 0.0f);}

	void sensing();
	void actuation();
		
	CNode* m_rootNode;
	CBlackBoard* m_blackBoard;
	int m_count;
	int m_food;
	int m_trackingID;
	std::vector<int> m_trackingIDs;
   Real m_fWheelVelocity;
   
   bool tracked();
   
   // sensors / actuators
   
   CCI_DifferentialSteeringActuator* m_pcWheels;	/* Pointer to the differential steering actuator */
   CCI_FootBotProximitySensor* m_pcProximity;		/* Pointer to the foot-bot proximity sensor */
   CCI_PositioningSensor* m_pcPosition;				/* Pointer to the foot-bot position sensor */
   CCI_RangeAndBearingActuator*  m_pcRABA;			/* Pointer to the range and bearing actuator */
   CCI_RangeAndBearingSensor* m_pcRABS;				/* Pointer to the range and bearing sensor */
   CCI_LEDsActuator* m_pcLEDs;							/* Pointer to the leds actuator */
   
};

#endif
