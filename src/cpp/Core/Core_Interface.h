#pragma once

#include <Base/String.h>
#include <Base/GlobalId.h>

namespace Core
{
///////////////////////////////////////////////////////////
//                                                       //
// --------------------- BEGIN API --------------------- //
//                                                       //
// ATTENTION: DO NOT CHANGE ANY SIGNATURES IN THE API !  //
//                                                       //
///////////////////////////////////////////////////////////

/////////////////////////////////////////
/// General
/////////////////////////////////////////

LX_CORE_EXPORT Base::String getLastImportedFilePath();
LX_CORE_EXPORT Base::String getCurrentScriptFilePath();
LX_CORE_EXPORT Base::GlobalId getCurrentScriptId();


///////////////////////////////////////////////////////////
//                                                       //
// ---------------------- END API ---------------------- //
//                                                       //
///////////////////////////////////////////////////////////

}  // namespace Core
