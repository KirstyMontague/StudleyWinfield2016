#ifndef CBLACKBOARD_H
#define CBLACKBOARD_H

#include <vector>
#include <iostream>

class CBlackBoard
{
	public:
		CBlackBoard(int numRobots) : 
			m_motors(0),
			m_scratchpad(0),
			m_sendSignal(0),
			m_receivedSignal(0),
			m_detectedFood(false), 
			m_carryingFood(false),
			m_density(0),
			m_densityChange(0),
			m_distNest(0),
			m_distNestChange(0),
			m_distFood(1),
			m_distFoodChange(0),
			m_numRobots(numRobots)
		{}
		
		int getMotors() {return m_motors;}
		void setMotors(int motors) {m_motors = motors;}
		
		int getScratchpad() {return m_scratchpad;}
		void setScratchpad(int scratchpad) {m_scratchpad = scratchpad;}
		
		int getSendSignal() {return m_sendSignal;}
		void setSendSignal(int signal) {m_sendSignal = signal;}
		
		bool getReceivedSignal() {return m_receivedSignal;}
		void setReceivedSignal(bool received) {m_receivedSignal = received;}
		
		bool getCarryingFood() {return m_carryingFood;}
		void setCarryingFood(bool carryingFood) {m_carryingFood = carryingFood;}
		
		bool getDetectedFood() {return m_detectedFood;}
		void setDetectedFood(bool detected);
				
		float getDensity() {return m_density;}
		float getDensityChange() {return m_densityChange;}
		void updateDensityVector(float density);
		void setDensity(bool first = false, int robotID = -1);
		
		float getDistNest() {return m_distNest;}
		float getNestChange() {return m_distNestChange;}
		void updateDistNestVector(float distance);
		void setDistNest(bool first = false, int robotID = -1);
		
		float getDistFood() {return m_distFood;}
		float getFoodChange() {return m_distFoodChange;}
		void updateDistFoodVector(float distance);
		void setDistFood(bool first = false, int robotID = -1);
		
	private:
	
		int m_motors;
		
		int m_scratchpad;
		
		int m_sendSignal;
		
		bool m_receivedSignal;
		
		bool m_detectedFood;
		
		bool m_carryingFood;
		
		float m_density;
		
		float m_densityChange;
		std::vector<float> m_densityVector;
		
		float m_distNest;
		float m_distNestChange;
		std::vector<float> m_distNestVector;
		
		float m_distFood;
		float m_distFoodChange;
		std::vector<float> m_distFoodVector;
		
		int m_numRobots;
		
};

#endif
