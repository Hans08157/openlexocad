#pragma once
#include <Geom/Precision.h>

namespace Topo
{
class LX_TOPO_EXPORT SimplifyOptions
{
public:

    void set_simplification_tol(double tol);
    void set_max_radius(double radius);
    void set_do_curve_simplification(int val);
    void set_do_surface_simplification(int val);
    void set_do_elliptical_cylinder_simplification(int allow_elliptical_cylinder);
    void set_do_elliptical_cone_simplification(int allow_elliptical_cone);
    void set_do_approximate(int val);
    void set_do_force_simplification(int val);
    void set_do_limit_surfs_to_faces(int val);

    void set_max_gap_tolerance(double mg);
    void set_desired_gap_tightness(double mg);

    void set_mesh_min_colinearity(double v);
    void set_mesh_min_delta_v(double v);
    void set_mesh_min_normal_angle(double v);
    void set_mesh_min_length(double v);


public:
    double m_simplify_pos_tol = Geom::Precision::linear_Resolution();
    double m_max_radius = Geom::Precision::linear_Resolution() / Geom::Precision::angle_Resolution();
    int m_do_curve_simplification = 1;
    int m_do_surface_simplification = 1;
    int m_allow_elliptical_cylinder_simplification = 1;
    int m_allow_elliptical_cone_simplification = 1;
    int m_do_approximate = 0;
    int m_do_force_simplification = 0;
    int m_limit_surfs_to_faces = 0;

    double m_max_gap_tolerance = 1;
    double m_desired_gap_tightness = Geom::Precision::linear_Resolution();

    double m_mesh_min_colinearity = 1e-6;
    double m_mesh_min_delta_v = 1e-6;
    double m_mesh_min_normal_angle = 1e-6;
    double m_mesh_min_length = 1e-6;
};

}  // namespace Topo