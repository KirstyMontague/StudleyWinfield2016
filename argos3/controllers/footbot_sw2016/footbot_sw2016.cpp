#include "footbot_sw2016.h"
#include <argos3/core/utility/configuration/argos_configuration.h>
#include <argos3/core/utility/math/vector2.h>

#include <iostream>
#include <algorithm>

CFootBotSW2016::CFootBotSW2016() :
   m_pcWheels(NULL),
   m_pcLEDs(NULL),
   m_pcProximity(NULL),
   m_pcPosition(NULL),
   m_pcRABA(NULL),
   m_pcRABS(NULL),
   m_fWheelVelocity(5.0f),
   m_trackingID(0) {
	m_count = 0;			   
}

CFootBotSW2016::~CFootBotSW2016()
{
	// print the amount of food gathered
	std::cout << "food " << GetId() << " " << std::to_string(m_food) << std::endl;
}

void CFootBotSW2016::Init(TConfigurationNode& t_node) 
{	
	m_pcWheels    = GetActuator<CCI_DifferentialSteeringActuator>("differential_steering");
	m_pcProximity = GetSensor  <CCI_FootBotProximitySensor      >("footbot_proximity"    );
	m_pcPosition  = GetSensor	<CCI_PositioningSensor    			>("positioning"       	 );
	m_pcRABA      = GetActuator<CCI_RangeAndBearingActuator     >("range_and_bearing"    );
	m_pcRABS      = GetSensor  <CCI_RangeAndBearingSensor       >("range_and_bearing"    );
	m_pcLEDs      = GetActuator<CCI_LEDsActuator                >("leds"                 );

	GetNodeAttributeOrDefault(t_node, "velocity", m_fWheelVelocity, m_fWheelVelocity);	
	GetNodeAttributeOrDefault(t_node, "trackingID", m_trackingID, m_trackingID);
	m_food = 0;
}

void CFootBotSW2016::buildTree(std::vector<std::string> tokens)
{
	m_rootNode = new CNode(tokens);	
}

void CFootBotSW2016::createBlackBoard(int numRobots)
{
	m_blackBoard = new CBlackBoard(numRobots);
}

void CFootBotSW2016::sensing() 
{
	// read sensor data
	const CCI_PositioningSensor::SReading& pos = m_pcPosition->GetReading();
	const CCI_RangeAndBearingSensor::TReadings& tPackets = m_pcRABS->GetReadings();	
	Real x = pos.Position.GetX();
	Real y = pos.Position.GetY();
	
	// defaults for density of robots and distance to food or nest
	std::vector<int> IDs;	
	short int nestHops = 9;
	short int foodHops = 9;
	
	// distance from the centre of the arena
	double r = sqrt((x * x) + (y * y));
	
	// check if the robot is in the food region and update blackboard	
	if (r >= 1)
	{
		foodHops = -1;
		m_blackBoard->setDetectedFood(r);
		m_pcLEDs->SetAllColors(CColor::GREEN);
	}
	
	// check if the robot is in the nest region and update blackboard
	if (r < .5)
	{
		nestHops = -1;
		
		if (m_blackBoard->getCarryingFood())
		{		
			m_food++;
			m_blackBoard->setCarryingFood(false);
			m_pcLEDs->SetAllColors(CColor::BLACK);
		}
	}
	if (std::stoi(GetId()) == m_trackingID)  std::cout << std::to_string(nestHops) <<  " ";
		
	// for each range and bearing signal received 
	for(size_t i = 0; i < tPackets.size(); ++i) {
		
		auto data = tPackets[i].Data;
		
		// if we haven't already received a signal from this robot in the current timestep	
		if (std::find(IDs.begin(), IDs.end(), tPackets[i].Data[3]) == IDs.end()) {
			
			// if the other robot is within range
			if (tPackets[i].Range < 25) {
				
				// save nest hops value if lower than the one currently stored
				if (data[5] < nestHops) {
					nestHops = data[5];
				}
				
				// save food hops value if lower than the one currently stored
				if (data[7] < foodHops) {
					foodHops = data[7];
				}
		
				// save this robot's ID
				IDs.push_back(tPackets[i].Data[3]);
			}
		}
	}
	
	// increment nest and food hops
	nestHops++;
	foodHops++;
	
	// save density and distance values
	m_blackBoard->setDensity(IDs.size());
	m_blackBoard->setDistNest(nestHops);
	m_blackBoard->setDistFood(foodHops);
}

void CFootBotSW2016::actuation() 
{
	// write robot ID, distance to nest and distance to food to buffer,
	// plus an arbitrary value to use remaining bytes
	CByteArray cBuf;	
	cBuf << std::stoi(GetId());
	cBuf << (short int) (m_blackBoard->getDistNest() * 10);
	cBuf << (short int) (m_blackBoard->getDistFood() * 10);
	cBuf << (short int) (0);
	
	// send range and bearing signal
	m_pcRABA->ClearData();
	m_pcRABA->SetData(cBuf);
	
	// send motor commands
	int motors = m_blackBoard->getMotors();	
	(motors == 0 ) ? stop() : (motors == 1) ? turnLeft() : (motors == 2) ? turnRight() : goStraight();	
}

void CFootBotSW2016::ControlStep() 
{
	m_count++;
	
	if (m_count == 1)
	{
		// send an initial range and bearing signal so the
		// distances don't get thrown off by empty values
		
		// fill buffer
		CByteArray cBuf;
		cBuf << std::stoi(GetId());
		cBuf << (short int) 11;
		cBuf << (short int) 11;
		cBuf << (short int) 0;
		
		// send signal
		m_pcRABA->ClearData();
		m_pcRABA->SetData(cBuf);
		
		// sometimes it's handy to be able toighlight a particular robot
		if (std::stoi(GetId()) == m_trackingID) m_pcLEDs->SetAllColors(CColor::YELLOW);
	}
	
	if (m_count % 5 == 0)
	{
		sensing();
		
		m_blackBoard->setMotors(0);
		std::string output;
		std::string result = m_rootNode->evaluate(m_blackBoard, output);
		
		// uncomment to print all nodes traversed on each tick
		// if (std::stoi(GetId()) == m_trackingID) std::cout << output << std::endl;
		
		actuation();
	}
}

REGISTER_CONTROLLER(CFootBotSW2016, "footbot_sw2016_controller")
