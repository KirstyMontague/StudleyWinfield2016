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
   m_rWheelVelocity(5.0f),
   m_lWheelVelocity(5.0f),
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

	Real wheelVelocity;
	Real noise;
	GetNodeAttributeOrDefault(t_node, "velocity", wheelVelocity, wheelVelocity);
	GetNodeAttributeOrDefault(t_node, "trackingID", m_trackingID, m_trackingID);
	GetNodeAttributeOrDefault(t_node, "verbose", m_verbose, m_verbose);
	
	noise = (std::rand() % 20);
	noise = (noise + 90) / 100;
	m_rWheelVelocity = wheelVelocity * noise;
	
	noise = (std::rand() % 20);
	noise = (noise + 90) / 100;
	m_lWheelVelocity = wheelVelocity * noise;
	
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

void CFootBotSW2016::setParams(float gap)
{
	m_params = gap;
}

void CFootBotSW2016::sensing() 
{
	bool tracking = inTrackingIDs() && m_verbose;
	std::string output;
	
	// reset receivedSignal
	m_blackBoard->setReceivedSignal(false);
	
	// read sensor data
	const CCI_PositioningSensor::SReading& pos = m_pcPosition->GetReading();
	const CCI_RangeAndBearingSensor::TReadings& tPackets = m_pcRABS->GetReadings();	
	Real x = pos.Position.GetX();
	Real y = pos.Position.GetY();
	
	// distance from the centre of the arena
	double r = sqrt((x * x) + (y * y));
	
	// update the blackboard to reflect whether the robot is in the food region
	m_blackBoard->setDetectedFood(r >= .5 + m_params);
	
	// update the blackboard to reflect whether the robot is in the nest region
	if (r < .5 && m_blackBoard->getCarryingFood())
	{		
		m_food++;
		m_blackBoard->setCarryingFood(false);
		m_pcLEDs->SetAllColors(CColor::BLACK);
	}
	
	if (r >= .5 + m_params)
	{
		m_pcLEDs->SetAllColors(CColor::GREEN);
	}
	
	// map for density of robots and defaults for distance to food or nest
	std::map<int, double> IDs;
	float nestRange = (r < .5) ? 0 : 500;
	float foodRange = (r < .5 + m_params) ? 500 : 0;
	
	// for each range and bearing signal received 
	for(size_t i = 0; i < tPackets.size(); ++i) {
		
		if (std::rand() % 20 == 0) {
			continue;
		}
		
		if (tPackets[i].Range > 100) {
			continue;
		}
		
		auto data = tPackets[i].Data;
		
		int id;
		short int nest;
		short int food;
		short int signal;
		data >> id;
		data >> nest;
		data >> food;
		data >> signal;
		
		if (signal == 1)
		{
			m_blackBoard->setReceivedSignal(true);
			if (tracking) output += "signal received from #" + std::to_string(id) + "\n";
		}
		
		// if we haven't already received a signal from this robot in the current timestep	
		if (IDs.find(id) == IDs.end())
		{
			// save distance to nest and food if lower than the ones currently stored
			if (nest + tPackets[i].Range < nestRange) nestRange = nest + tPackets[i].Range;
			if (food + tPackets[i].Range < foodRange) foodRange = food + tPackets[i].Range;
			
			// store density value for this robot
			Real range = 1 / (ARGOS_PI * ((tPackets[i].Range / 1000) * (tPackets[i].Range / 1000))); // max = 1107
			IDs.insert(std::pair<int, double>(id, range));
		}
	}
	
	// calculate density
	float density = 0;
	for (auto it = IDs.begin(); it != IDs.end(); ++it)
	{
		density += it->second;
	}
	
	if (tracking) std::cout << output <<std::endl;
	
	// save density and change in density
	m_blackBoard->updateDensityVector(density);
	if (m_count == 2 || m_count % 4 == 0)
	{
		m_blackBoard->setDensity((m_count == 2), (tracking ? std::stoi(GetId()) : -1));
	}
	
	// save distance to nest and change in distance
	m_blackBoard->updateDistNestVector(nestRange);
	if (m_count == 2 || m_count % 4 == 0)
	{
		m_blackBoard->setDistNest((m_count == 2), (tracking ? std::stoi(GetId()) : -1));
	}
	
	// save distance to food and change in distance
	m_blackBoard->updateDistFoodVector(foodRange);
	if (m_count == 2 || m_count % 4 == 0)
	{
		m_blackBoard->setDistFood((m_count == 2), (tracking ? std::stoi(GetId()) : -1));
	}
}

void CFootBotSW2016::actuation() 
{
	short int id = std::stoi(GetId());
	short int distNest = m_blackBoard->getDistNest() * 500;
	short int distFood = m_blackBoard->getDistFood() * 500;
	short int sendSignal = m_blackBoard->getSendSignal() <= 0 ? 0 : 1;
	
	// write robot ID, distance to nest, distance to food and signal to buffer
	CByteArray cBuf;	
	cBuf << std::stoi(GetId());
	cBuf << distNest;
	cBuf << distFood;
	cBuf << sendSignal;
	
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
		
		short int id = std::stoi(GetId());
	
		// fill buffer
		CByteArray cBuf;
		cBuf << std::stoi(GetId());
		cBuf << (short int) 500;
		cBuf << (short int) 500;
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
