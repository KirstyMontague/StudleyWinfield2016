#include "CNode.h"

#include <sstream>
#include <bits/stdc++.h> 
#include <stdlib.h> 



CNode::CNode(std::string word)
{
	m_data = std::stof(word);
}

CNode::CNode(std::vector<std::string>& chromosome) : m_ptr(0)
{
	if (chromosome.size() > 0)
	{
		std::string word = chromosome.at(0);
		//std::cout << word << std::endl;
		
		int token;		
		{		
			if (word == "seqm2") token = 0;
			if (word == "seqm3") token = 1;
			if (word == "seqm4") token = 2;
			if (word == "selm2") token = 3;
			if (word == "selm3") token = 4;
			if (word == "selm4") token = 5;
			if (word == "probm2") token = 6;
			if (word == "probm3") token = 7;
			if (word == "probm4") token = 8;
			if (word == "repeat") token = 9;
			if (word == "successd") token = 10;
			if (word == "failured") token = 11;
			if (word == "mf") token = 12;
			if (word == "ml") token = 13;
			if (word == "mr") token = 14;
			if (word == "ifltvar") token = 15;
			if (word == "ifgevar") token = 16;
			if (word == "ifltcon") token = 17;
			if (word == "ifgecon") token = 18;
			if (word == "set") token = 19;
			if (word == "successl") token = 20;
			if (word == "failurel") token = 21;
		}
		
		chromosome.erase(chromosome.begin());
		
		switch (token)
		{
			case 0: {
				m_type = nodetype::seqm2;
				m_children.push_back(new CNode(chromosome));
				m_children.push_back(new CNode(chromosome));
				break;
			}
			case 1: {
				m_type = nodetype::seqm3;
				m_children.push_back(new CNode(chromosome));
				m_children.push_back(new CNode(chromosome));
				m_children.push_back(new CNode(chromosome));
				break;
			}
			case 2: {
				m_type = nodetype::seqm4;
				m_children.push_back(new CNode(chromosome));
				m_children.push_back(new CNode(chromosome));
				m_children.push_back(new CNode(chromosome));
				m_children.push_back(new CNode(chromosome));
				break;
			}
			case 3: {
				m_type = nodetype::selm2;
				m_children.push_back(new CNode(chromosome));
				m_children.push_back(new CNode(chromosome));
				break;
			}
			case 4: {
				m_type = nodetype::selm3;
				m_children.push_back(new CNode(chromosome));
				m_children.push_back(new CNode(chromosome));
				m_children.push_back(new CNode(chromosome));
				break;
			}
			case 5: {
				m_type = nodetype::selm4;
				m_children.push_back(new CNode(chromosome));
				m_children.push_back(new CNode(chromosome));
				m_children.push_back(new CNode(chromosome));
				m_children.push_back(new CNode(chromosome));
				break;
			}
			case 6: {
				m_type = nodetype::probm2;
				m_children.push_back(new CNode(chromosome));
				m_children.push_back(new CNode(chromosome));
				m_ptr = std::rand() % m_children.size();
				break;
			}
			case 7: {
				m_type = nodetype::probm3;
				m_children.push_back(new CNode(chromosome));
				m_children.push_back(new CNode(chromosome));
				m_children.push_back(new CNode(chromosome));
				m_ptr = std::rand() % m_children.size();
				break;
			}
			case 8: {
				m_type = nodetype::probm4;
				m_children.push_back(new CNode(chromosome));
				m_children.push_back(new CNode(chromosome));
				m_children.push_back(new CNode(chromosome));
				m_children.push_back(new CNode(chromosome));
				m_ptr = std::rand() % m_children.size();
				break;
			}
			case 9: {
				
				m_type = nodetype::repeat;
				
				m_children.push_back(new CNode(chromosome.at(0)));
				chromosome.erase(chromosome.begin());
				
				m_children.push_back(new CNode(chromosome));
				
				break;
				
				m_type = nodetype::repeat;
				m_children.push_back(new CNode(chromosome));
				break;
			}
			case 10: {
				m_type = nodetype::successd;
				m_children.push_back(new CNode(chromosome));
				break;
			}
			case 11: {
				m_type = nodetype::failured;
				m_children.push_back(new CNode(chromosome));
				break;
			}
			case 12: {
				m_type = nodetype::mf;
				break;
			}
			case 13: {
				m_type = nodetype::ml;
				break;
			}
			case 14: {
				m_type = nodetype::mr;
				break;
			}
			case 15: {
				
				m_type = nodetype::ifltvar;		
				
				m_children.push_back(new CNode(chromosome.at(0)));
				chromosome.erase(chromosome.begin());
			
				m_children.push_back(new CNode(chromosome.at(0)));
				chromosome.erase(chromosome.begin());
			
				break;
			}
			case 16: {
				
				m_type = nodetype::ifgevar;		
				
				m_children.push_back(new CNode(chromosome.at(0)));
				chromosome.erase(chromosome.begin());
			
				m_children.push_back(new CNode(chromosome.at(0)));
				chromosome.erase(chromosome.begin());
			
				break;
			}
			case 17: {
				
				m_type = nodetype::ifltcon;
									
				m_children.push_back(new CNode(chromosome.at(0)));
				chromosome.erase(chromosome.begin());
			
				m_children.push_back(new CNode(chromosome.at(0)));
				chromosome.erase(chromosome.begin());
			
				break;
			}
			case 18: {
				
				m_type = nodetype::ifgecon;	
				
				m_children.push_back(new CNode(chromosome.at(0)));
				chromosome.erase(chromosome.begin());
			
				m_children.push_back(new CNode(chromosome.at(0)));
				chromosome.erase(chromosome.begin());
			
				break;
			}
			case 19: {
				
				m_type = nodetype::set;
				
				m_children.push_back(new CNode(chromosome.at(0)));
				chromosome.erase(chromosome.begin());
			
				m_children.push_back(new CNode(chromosome.at(0)));
				chromosome.erase(chromosome.begin());
			
				break;
			}
			case 20: {
				m_type = nodetype::successl;
				break;
			}
			case 21: {
				m_type = nodetype::failurel;
				break;
			}
			case 22: {
				m_data = std::stoi(word); // constant
				break;
			}
			case 23: {
				m_data = std::stoi(word); // blackboard index
				break;
			}
			case 24: {
				m_data = std::stoi(word); // repetitions
				break;
			}
			default: {
				std::cout << "node error" << std::endl;
			}
		}
	}
}

std::string CNode::evaluate(CBlackBoard* blackBoard, std::string& output)
{	
	switch (m_type)
	{
		case CNode::nodetype::seqm2:
		case CNode::nodetype::seqm3:
		case CNode::nodetype::seqm4:
		{
			output += "seqm" + std::to_string(m_children.size()) + "(" + std::to_string(m_ptr) + ") ";
		
			while (m_ptr < m_children.size())
			{
				std::string result = m_children[m_ptr]->evaluate(blackBoard, output);
			
				if (result == "failure")
				{
					m_ptr = 0;
					return "failure";
				}
				
				else if (result == "running")
				{
					return "running";
				}
				
				else
				{
					m_ptr++;
				}
			}
			m_ptr = 0;
			return "success";
		}
		
		case CNode::nodetype::selm2:
		case CNode::nodetype::selm3:
		case CNode::nodetype::selm4:
		{
			output += "selm" + std::to_string(m_children.size()) + "(" + std::to_string(m_ptr) + ") ";
			
			while (m_ptr < m_children.size())
			{
				std::string result = m_children[m_ptr]->evaluate(blackBoard, output);
			
				if (result == "success")
				{
					m_ptr = 0;
					return "success";
				}
				
				else if (result == "running")
				{
					return "running";
				}
				
				else
				{
					m_ptr++;
				}
			}
			
			m_ptr = 0;
			return "failure";
		}
		
		case CNode::nodetype::probm2:
		case CNode::nodetype::probm3:
		case CNode::nodetype::probm4:
		{
			output += "probm" + std::to_string(m_children.size()) + "(" + std::to_string(m_ptr) + ") ";
			
			std::string result = m_children[m_ptr]->evaluate (blackBoard, output);
			
			if (result != "running")
			{
				m_ptr = std::rand() % m_children.size();
			}
			
			return result;
		}
		
		case CNode::nodetype::repeat:
		{
			output += "repeat" + std::to_string(m_children[0]->getData()) + " ";
			
			float iterations = m_children[0]->getData();
			int count = 0;
			
			while (count < iterations)
			{
				count++;
				std::string result = m_children[1]->evaluate(blackBoard, output);
				if (result != "success")
				{
					return result;
				}
			}
			
			return "success";
		}
		
		case CNode::nodetype::successd:
		{
			output += "successd ";
			std::string result = m_children[0]->evaluate (blackBoard, output);
			return (result == "failure") ? "success" : result;
		}
		
		case CNode::nodetype::failured:
		{
			output += "failured ";
			std::string result = m_children[0]->evaluate (blackBoard, output);
			return (result == "success") ? "failure" : result;
		}
		
		case CNode::nodetype::mf:
		{
			output += "mf("+ std::to_string(m_ptr) + ") ";
			
			if (m_ptr == 0)
			{
				blackBoard->setMotors(3);
				m_ptr++;
				return "running";
			}
			
			else
			{
				blackBoard->setMotors(3);
				m_ptr--;
				return "success";
			}
		}
		
		case CNode::nodetype::ml:
		{
			output += "ml("+ std::to_string(m_ptr) + ") ";
			
			if (m_ptr == 0)
			{
				blackBoard->setMotors(1);
				m_ptr++;
				return "running";
			}
			
			else
			{
				blackBoard->setMotors(1);
				m_ptr--;
				return "success";
			}
		}
		
		case CNode::nodetype::mr:
		{
			output += "mr("+ std::to_string(m_ptr) + ") ";
			
			if (m_ptr == 0)
			{
				blackBoard->setMotors(2);
				m_ptr++;
				return "running";
			}
			
			else
			{
				blackBoard->setMotors(2);
				m_ptr--;
				return "success";
			}
		}
				
		case CNode::nodetype::set:
		{
			if (m_children[0]->getData() == 1)
			{
				output += "set scratchpad = " + std::to_string(m_children[1]->getData()) + " ";
				blackBoard->setScratchpad(m_children[1]->getData());
			}
			
			if (m_children[0]->getData() == 2)
			{
				output += "set signal = " + std::to_string(m_children[1]->getData()) + " ";
				blackBoard->setSendSignal(m_children[1]->getData());
			}
			
			return "success";
		}
		
		case CNode::nodetype::ifltvar:
		{
			float value1 = normaliseBlackBoardValue(blackBoard, m_children[0]->getData());
			float value2 = normaliseBlackBoardValue(blackBoard, m_children[1]->getData());
			
			std::string result = (value1 < value2) ? "success" : "failure";
			output += std::to_string(value1) + " lt " + std::to_string(value2) + " " + result + " ";
			return result;			
		}
		
		case CNode::nodetype::ifgevar:
		{
			float value1 = normaliseBlackBoardValue(blackBoard, m_children[0]->getData());
			float value2 = normaliseBlackBoardValue(blackBoard, m_children[1]->getData());
			
			std::string result = (value1 >= value2) ? "success" : "failure";
			output += std::to_string(value1) + " gte " + std::to_string(value2) + " " + result + " ";
			return result;			
		}
		
		case CNode::nodetype::ifltcon:
		{
			float value = normaliseBlackBoardValue(blackBoard, m_children[0]->getData());
			float data = m_children[1]->getData();
			
			std::string result = (value < data) ? "success" : "failure";
			output += std::to_string(value) + " lt " + std::to_string(data) + " " + result + " ";
			return result;
		}
		
		case CNode::nodetype::ifgecon:
		{
			float value = normaliseBlackBoardValue(blackBoard, m_children[0]->getData());
			float data = m_children[1]->getData();
			
			std::string result = (value >= data) ? "success" : "failure";
			output += std::to_string(value) + " gte " + std::to_string(data) + " " + result + " ";
			return result;			
		}

		case CNode::nodetype::successl:
		{
			output += "successl ";
			return "success";
		}
		
		case CNode::nodetype::failurel:
		{
			output += "failurel ";
			return "failure";
		}
		
		default: 
			std::cout << "evaluation error" << std::endl;
	}

	return 0;
}

float CNode::normaliseBlackBoardValue(CBlackBoard* blackBoard, int index)
{
	if (index == 1) { // values between -100 and 100
		return blackBoard->getScratchpad() / 100;
	}
	
	if (index == 2) { // values between -100 and 100
		return blackBoard->getSendSignal() / 100;
	}
	
	if (index == 3) { // boolean
		return (!blackBoard->getReceivedSignal()) ? -1 : 1;
	}
	
	if (index == 4) { // boolean
		return (!blackBoard->getDetectedFood()) ? -1 : 1;
	}
	
	if (index == 5) { // boolean
		return (!blackBoard->getCarryingFood()) ? -1 : 1;
	}
	
	if (index == 6) { // values between 0 and 1
		return (blackBoard->getDensity() * 2 - 1);
	}
	
	if (index == 7) { // values between -4/7 and 4/7
		return (blackBoard->getDensityChange() / 4) * 7;
	}
	
	if (index == 8) { // values between -4/7 and 4/7
		return (blackBoard->getNestChange() / 4) * 7;
	}
	
	if (index == 9) { // values between -4/7 and 4/7
		return (blackBoard->getFoodChange() / 4) * 7;
	}	
}
