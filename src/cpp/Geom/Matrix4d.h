#pragma once
#include <Geom/Pnt.h>

namespace Geom
{
/**
 * \brief This is a simple implementation of double based matrix
 */
class LX_GEOM_EXPORT Matrix4
{
public:
    Matrix4();
    ;

    void multVecMatrix(const Geom::Pnt& src, Geom::Pnt& dst) const;
    void makeIdentity();
    /**
     * \brief init the matrix to be scale matrix
     * \param value scale value
     */
    void setScale(double value);

    // Matrix4 operator *(const Matrix4 & m1, const Matrix4 & m2);
    Matrix4& operator*=(const Matrix4& m);

    Matrix4& multRight(const Matrix4& m);

    double matrix[4][4]{};
};
}  // namespace Geom
