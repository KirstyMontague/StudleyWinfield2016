#include "CBlackBoard.h"

void CBlackBoard::setDetectedFood(bool detected)
{
	if (!detected)
	{
		m_detectedFood = false;
	}
	else
	{
		m_detectedFood = true;
		
		if (!m_carryingFood)
		{
			m_carryingFood = true;
		}
	}		
}

void CBlackBoard::updateDensityVector(float density)
{
	// 1107 is the maximum density value that can be contributed by a single
	// robot and 6 is the number of robots that can fit around a single robot
	density = density / (1107 * 6);
	
	if (m_densityVector.size() > 6)
	{
		m_densityVector.erase(m_densityVector.begin());
	}
	
	m_densityVector.push_back(density);	
}

void CBlackBoard::setDensity(bool first, int robotID)
{
	if (robotID != -1) std::cout << "density ";
	
	float density = 0;
	for (auto d : m_densityVector)
	{
		density += d;
		if (robotID != -1) std::cout << d << " ";
	}
	density /= m_densityVector.size();
	if (robotID != -1) std::cout << " | " << density;
	
	if (!first)	m_densityChange = density - m_density;	
	if (robotID != -1) std::cout << " | " << m_densityChange << std::endl;
	
	m_density = density;
}

void CBlackBoard::updateDistNestVector(float distance)
{
	distance = distance / 500;
	
	if (m_distNestVector.size() > 6)
	{
		m_distNestVector.erase(m_distNestVector.begin());
	}
	
	m_distNestVector.push_back(distance);	
}

void CBlackBoard::setDistNest(bool first, int robotID)
{
	if (robotID != -1) std::cout << "nest ";
	
	float distance = 0;
	for (auto d : m_distNestVector)
	{
		distance += d;
		if (robotID != -1) std::cout << d << " ";
	}
	distance /= m_distNestVector.size();
	if (robotID != -1) std::cout << " | " << distance;
	
	if (!first)	m_distNestChange = distance - m_distNest;	
	if (robotID != -1) std::cout << " | " << m_distNestChange << std::endl;
	
	m_distNest = distance;
}


void CBlackBoard::updateDistFoodVector(float distance)
{
	distance = distance / 500;
	
	if (m_distFoodVector.size() > 6)
	{
		m_distFoodVector.erase(m_distFoodVector.begin());
	}
	
	m_distFoodVector.push_back(distance);	
}

void CBlackBoard::setDistFood(bool first, int robotID)
{
	if (robotID != -1) std::cout << "food ";
	
	float distance = 0;
	for (auto d : m_distFoodVector)
	{
		distance += d;
		if (robotID != -1) std::cout << d << " ";
	}
	distance /= m_distFoodVector.size();
	if (robotID != -1) std::cout << " | " << distance;
	
	if (!first)	m_distFoodChange = distance - m_distFood;
	if (robotID != -1) std::cout << " | " << m_distFoodChange << std::endl;
	
	m_distFood = distance;
}
