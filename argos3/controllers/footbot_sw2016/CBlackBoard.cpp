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
		m_distFood = 0;
		
		if (!m_carryingFood)
		{
			m_carryingFood = true;
		}
	}		
}

void CBlackBoard::setDensity(float density)
{
	density = density / m_numRobots;
	m_densityChange = density - m_density;
	m_density = density;
}

void CBlackBoard::setDistNest(float distance)
{
	distance /= 10;
	m_distNestChange = distance - m_distNest;
	m_distNest = distance;
}

void CBlackBoard::setDistFood(float distance)
{
	distance /= 10;
	m_distFoodChange = distance - m_distFood;
	m_distFood = distance;
}
