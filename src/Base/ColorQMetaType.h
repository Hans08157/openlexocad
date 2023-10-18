#pragma once
#include <Base/Color.h>
#include <QMetaType>  // needed for Q_DECLARE_METATYPE

Q_DECLARE_METATYPE(Base::Color)  // register type for use with QVariant, needed by PropertyView
