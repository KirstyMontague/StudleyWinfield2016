#include "footbot_sw2016.h"
#include <argos3/core/utility/configuration/argos_configuration.h>
#include <argos3/core/utility/math/vector2.h>

#include <iostream>
#include <algorithm>
#include <cstring>

CFootBotSW2016::CFootBotSW2016() :
   m_pcWheels(NULL),
   m_pcLEDs(NULL),
   m_pcProximity(NULL),
   m_pcPosition(NULL),
   m_pcRABA(NULL),
   m_pcRABS(NULL),
   m_fWheelVelocity(5.0f),
   m_trackingID(0),
   m_count(0),
   m_food(0) {
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
	GetNodeAttributeOrDefault(t_node, "verbose", m_verbose, m_verbose);
	
	m_trackingIDs.push_back(m_trackingID);
	
	// sometimes it's handy to be able to highlight a particular robot
	if (inTrackingIDs() && m_verbose) m_pcLEDs->SetAllColors(CColor::YELLOW);
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
	bool tracking = inTrackingIDs() && m_verbose;
	std::string output;
	
	// read sensor data
	const CCI_PositioningSensor::SReading& pos = m_pcPosition->GetReading();
	const CCI_RangeAndBearingSensor::TReadings& tPackets = m_pcRABS->GetReadings();	
	Real x = pos.Position.GetX();
	Real y = pos.Position.GetY();
	
	// distance from the centre of the arena
	double r = sqrt((x * x) + (y * y));
	
	// defaults for density of robots and distance to food or nest
	std::vector<int> IDs;	
	int density = 0;
	float nestHops = (r < .5) ? -1000 : 9000;
	float foodHops = (r < 1) ? 9000 : -1000;
	
	// update the blackboard to reflect whether the robot is in the food region
	m_blackBoard->setDetectedFood(r >= 1);
	
	// update the blackboard to reflect whether the robot is in the nest region
	if (r < .5 && m_blackBoard->getCarryingFood())
	{		
		m_food++;
		m_blackBoard->setCarryingFood(false);
		m_pcLEDs->SetAllColors(CColor::BLACK);
	}
	
	if (r >= 1)
	{
		m_pcLEDs->SetAllColors(CColor::GREEN);
	}
		
	// for each range and bearing signal received 
	for(size_t i = 0; i < tPackets.size(); ++i) {
		
		auto data = tPackets[i].Data;
		
		int id;
		short int nest;
		short int food;
		data >> id;
		data >> nest;
		data >> food;
				
		// if we haven't already received a signal from this robot in the current timestep	
		if (std::find(IDs.begin(), IDs.end(), id) == IDs.end()) {
			
			if (tracking) output += std::to_string(id) + " ";
		
			// if the other robot is within range
			if (tPackets[i].Range < 35) {
				
				if (tracking) output += std::to_string(food) + " | ";
				
				// save nest hops value if lower than the one currently stored
				if (nest < nestHops) {
					nestHops = nest;
				}
				
				// save food hops value if lower than the one currently stored
				if (food < foodHops) {
					foodHops = food;
				}
				
				density++;
			}
			else
			{
				if (tracking) output += "x | ";
			}
		
			// save this robot's ID
			IDs.push_back(id);
		}
		else
		{
			if (tracking) output += "d | ";
		}
	}
	
	// increment nest and food hops
	nestHops += 1000;
	foodHops += 1000;
	
	if (tracking) output += std::to_string(foodHops);	
	if (tracking) std::cout << GetId() << " : " << output <<std::endl;
	
	// save density and change in density
	m_blackBoard->updateDensityVector(density);
	if (m_count == 2 || m_count % 4 == 0)
	{
		m_blackBoard->setDensity((m_count == 2), (tracking ? std::stoi(GetId()) : -1));
	}
	
	// save distance to nest and change in distance
	m_blackBoard->updateDistNestVector(nestHops);
	if (m_count == 2 || m_count % 4 == 0)
	{
		m_blackBoard->setDistNest((m_count == 2), (tracking ? std::stoi(GetId()) : -1));
	}
	
	// save distance to food and change in distance
	m_blackBoard->updateDistFoodVector(foodHops);
	if (m_count == 2 || m_count % 4 == 0)
	{
		m_blackBoard->setDistFood((m_count == 2), (tracking ? std::stoi(GetId()) : -1));
	}
}

void CFootBotSW2016::actuation() 
{
	short int distNest = m_blackBoard->getDistNest() * 10000;
	short int distFood = m_blackBoard->getDistFood() * 10000;
	if (inTrackingIDs() && m_verbose) std::cout << GetId() << " RAB signal: " << distFood << std::endl;
	
	// write robot ID, distance to nest and distance to food to buffer,
	// plus an arbitrary value to use remaining bytes
	CByteArray cBuf;	
	cBuf << std::stoi(GetId());
	cBuf << distNest;
	cBuf << distFood;
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
		cBuf << (short int) 10000;
		cBuf << (short int) 10000;
		cBuf << (short int) 0;
		
		// send signal
		m_pcRABA->ClearData();
		m_pcRABA->SetData(cBuf);
	}
	else
	{
		sensing();
	}
	
	if (m_count % 4 == 0)
	{
		m_blackBoard->setMotors(0);
		std::string output;
		std::string result = m_rootNode->evaluate(m_blackBoard, output);
		
		// uncomment to print all nodes traversed on each tick
		if (inTrackingIDs()) std::cout << output << std::endl;
	}
		
	if (m_count > 1)
	{
		actuation();
	}
	
	if (inTrackingIDs() && m_verbose) std::cout << std::endl;
}

bool CFootBotSW2016::inTrackingIDs()
{
	return (std::find(m_trackingIDs.begin(), m_trackingIDs.end(), std::stoi(GetId())) != m_trackingIDs.end());
}

REGISTER_CONTROLLER(CFootBotSW2016, "footbot_sw2016_controller")
