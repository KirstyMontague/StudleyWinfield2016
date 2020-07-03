#include "sw2016_loop_functions.h"

#include <argos3/plugins/simulator/entities/box_entity.h>
#include <argos3/plugins/simulator/entities/cylinder_entity.h>
#include <argos3/plugins/robots/foot-bot/simulator/footbot_entity.h>

#include <controllers/footbot_sw2016/footbot_sw2016.h>

#include <sstream>
#include <list>
#include <algorithm>
#include <string>
#include <math.h>

CSW2016LoopFunctions::CSW2016LoopFunctions() :
   m_pcFloor(NULL) {
}

CSW2016LoopFunctions::~CSW2016LoopFunctions() {}

void CSW2016LoopFunctions::Init(TConfigurationNode& t_tree) 
{
	m_pcFloor = &GetSpace().GetFloorEntity();
                     
	CRandom::CRNG* pcRNG = CRandom::CreateRNG("argos");;
	
	// get random seed from file	
   std::ifstream seedFile("../seed.txt");
	std::string seed;
	while( getline(seedFile, seed) )
	{
		pcRNG->SetSeed(std::stoi(seed));
		pcRNG->Reset();
	}
		
	// get the filename for chromosome (best/chromosome)
	std::string filename;
	TConfigurationNodeIterator itDistr;
	for(itDistr = itDistr.begin(&t_tree); itDistr != itDistr.end(); ++itDistr) 
	{
		TConfigurationNode& tDistr = *itDistr;
		GetNodeAttribute(tDistr, "name", filename);
	}

	// read number of robots and chromosome from fil
   std::ifstream chromosomeFile("../"+filename);   
   
	int sqrtRobots = 0;
	std::string chromosome;	
	std::string line;
   while( getline(chromosomeFile, line) )
	{
		// number of robots
		if (sqrtRobots == 0)
		{
			sqrtRobots = std::stoi(line);
		}
		
		// chromosome
		else
		{
			line.erase(std::remove(line.begin(), line.end(), ','), line.end());
			
			std::replace( line.begin(), line.end(), '(', ' ');
			std::replace( line.begin(), line.end(), ')', ' ');
			
			chromosome = line;
		}
	}
	
	// tokenize chromosome
	std::stringstream ss(chromosome); 
	std::string token;
	std::vector<std::string> tokens;
	while (std::getline(ss, token, ' ')) 
	{
		if (token.length() > 0)
		{
			tokens.push_back(token);
		}
	}   
	
	// add robots
	for (int i = 0; i < sqrtRobots; ++i)
	{
		for (int j = 0; j < sqrtRobots; ++j)
		{
			CFootBotEntity* pcFB = new CFootBotEntity(std::to_string(i*sqrtRobots+j), "fswc");
			AddEntity(*pcFB);
			
			CVector3 cFBPos;
			CQuaternion cFBRot;	
			
			// position
			double x = ((double) i - floor(sqrtRobots / 2)) / 4;
			double y = ((double) j - floor(sqrtRobots / 2)) / 4;
			cFBPos.Set(x, y, 0.0f);	
			
			// rotation
			auto r = pcRNG->Uniform(CRadians::UNSIGNED_RANGE);
			cFBRot.FromAngleAxis(r, CVector3::Z);
			
			// place robot
			MoveEntity(pcFB->GetEmbodiedEntity(), cFBPos, cFBRot);	
		
			// create robot
			CFootBotSW2016& controller = dynamic_cast<CFootBotSW2016&>(pcFB->GetControllableEntity().GetController());
			controller.buildTree(tokens);
			controller.createBlackBoard(sqrtRobots * sqrtRobots);
		}
	}

}

CColor CSW2016LoopFunctions::GetFloorColor(const CVector2& c_position_on_plane)
{
	double x = c_position_on_plane.GetX();
	double y = c_position_on_plane.GetY();
	
	// distance from centre
	double r = sqrt((x * x) + (y * y));
	
	if (fmod(x, 1) == 0 || fmod(y, 1) == 0)
	{
      return CColor::GRAY80; // tile edges
	}	
	else if (r < 0.5f) 
   {
		return CColor::GRAY50; // nest
   }
   else if (r < 1.0f)
   {
		return CColor::WHITE; // gap
	}
	
	return CColor::GRAY50; // food
}

	
REGISTER_LOOP_FUNCTIONS(CSW2016LoopFunctions, "sw2016_loop_functions");
