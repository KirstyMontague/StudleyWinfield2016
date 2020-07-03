#ifndef CBLACKBOARD_H
#define CBLACKBOARD_H


class CBlackBoard
{
	public:
		CBlackBoard(int numRobots) : 
			m_motors(0), 
			m_detectedFood(false), 
			m_carryingFood(false),
			m_numRobots(numRobots)
		{}
		
		int getMotors() {return m_motors;}
		void setMotors(int motors) {m_motors = motors;}
		
		bool getCarryingFood() {return m_carryingFood;}
		void setCarryingFood(bool carryingFood) {m_carryingFood = carryingFood;}
		
		bool getDetectedFood() {return m_detectedFood;}
		void setDetectedFood(bool detected);
				
		float getDensity() {return m_density;}
		float getDensityChange() {return m_densityChange;}
		void setDensity(float density);	
		
		float getDistNest() {return m_distNest;}
		float getNestChange() {return m_distNestChange;}
		void setDistNest(float distance);
		
		float getFoodChange() {return m_distFoodChange;}
		float getDistFood() {return m_distFood;}
		void setDistFood(float distance);
		
	private:
	
		int m_motors;
		
		bool m_detectedFood;
		bool m_carryingFood;
		
		float m_density;
		float m_densityChange;
		
		float m_distNest;
		float m_distNestChange;
		
		float m_distFood;
		float m_distFoodChange;
		
		int m_numRobots;
		
};

#endif
