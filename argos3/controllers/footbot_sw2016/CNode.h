#ifndef CNODE_H
#define CNODE_H

#include "CBlackBoard.h"

#include <iostream>
#include <vector>

class CNode
{
	public:
	
		enum nodetype : int
		{
			seqm2 = 0,
			seqm3 = 1,
			seqm4 = 2,
			selm2 = 3,
			selm3 = 4,
			selm4 = 5,
			probm2 = 6,
			probm3 = 7,
			probm4 = 8,
			repeat = 9,
			successd = 10,
			failured = 11,
			mf = 12,
			ml = 13,
			mr = 14,
			ifltvar = 15,
			ifgevar = 16,
			ifltcon = 17,
			ifgecon = 18,
			set = 19,
			successl = 20,
			failurel = 21,
			rand = 22,
			bb = 23
			
		};

		CNode(std::vector<std::string>& chromosome);
		CNode(std::string word);
		std::string evaluate(CBlackBoard* blackBoard, std::string& output);		
		int getData() {return m_data;}
	
	private:
	
		float normalisedBlackBoardValue(CBlackBoard* blackBoard, int index);
	
		std::vector<CNode*> m_children;
		nodetype m_type;
		int m_data;
	
};

#endif
