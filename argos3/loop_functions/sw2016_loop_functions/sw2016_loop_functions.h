
#include <argos3/core/simulator/loop_functions.h>

using namespace argos;

class CSW2016LoopFunctions : public CLoopFunctions {

public:

   CSW2016LoopFunctions();
   virtual ~CSW2016LoopFunctions();

   virtual void Init(TConfigurationNode& t_tree);
   
   virtual CColor GetFloorColor(const CVector2& c_position_on_plane);

private:

   CFloorEntity* m_pcFloor;
};

