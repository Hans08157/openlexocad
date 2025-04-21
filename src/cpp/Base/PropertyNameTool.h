#pragma once
#include <string>
#include <map>

/// The PropertyKind enum determines what a modification of
/// this property does to the object it is contained in.
/// The setting of the PropertyKind has direct influence on
/// the recompute of an object:

/// P_MODIFY_DATA    -> triggers NO RECOMPUTE
/// P_MODIFY_PLACEMENT   -> triggers a recompute of the objects placement only
/// P_MODIFY_LINK               -> depricated, don't use
/// P_MODIFY_VISIBLITY   -> triggers a change of the objects visibility
/// P_MODIFY_SHAPE       -> triggers a recompute of the objects shape. This always results in a recompute of the appearance aswell.
/// P_MODIFY_APPEARANCE  -> triggers a recompute of the objects appearance (color, textures, styles)


namespace Base
{
enum PropertyKind
{
    P_MODIFY_DATA = 0,
    P_MODIFY_PLACEMENT = 1 << 0,   // 1
    P_MODIFY_LINK = 1 << 1,               // 2
    P_MODIFY_VISIBLITY = 1 << 3,   // 8
    P_MODIFY_SHAPE = 1 << 4,       // 16
    P_MODIFY_APPEARANCE = 1 << 5,  // 32

};

// Property name
enum PName
{
    m_No_Name = 0,
    m_GlobalId,
    m_OwnerHistory,
    m_Name,
    m_Description,
    m_ObjectType,
    m_ObjectPlacement,
    m_Representation,
    m_Radius,
    m_Position,
    m_Tag,
    m_XLength,
    m_YLength,
    m_ZLength,
    m_Location,
    m_Axis,
    m_RefDirection,
    m_Coordinates,

    // Inverse > 10000
    m_Inverse = 10000,
    m_StyledByItem_inverse,
    m_HasAssignments_inverse,
    m_Nests_inverse,
    m_IsNestedBy_inverse,
    m_HasContext_inverse,
    m_IsDecomposedBy_inverse,
    m_Decomposes_inverse,
    m_HasAssociations_inverse,
    m_IsDeclaredBy_inverse,
    m_Declares_inverse,
    m_IsTypedBy_inverse,
    m_IsDefinedBy_inverse,
    m_ReferencedBy_inverse,
    m_FillsVoids_inverse,
    m_ConnectedTo_inverse,
    m_IsInterferedByElements_inverse,
    m_InterferesElements_inverse,
    m_HasProjections_inverse,
    m_ReferencedInStructures_inverse,
    m_HasOpenings_inverse,
    m_IsConnectionRealization_inverse,
    m_ProvidesBoundaries_inverse,
    m_ConnectedFrom_inverse,
    m_HasCoverings_inverse,
    m_ContainedInStructure_inverse,
    // User > 20000
    m_User = 20000
};

/// This class is used to store all property names and
/// their indices in a central location for fast access
/// and low memory footprint.

class LX_BASE_EXPORT PropertyNameTool
{
public:
    /// Returns the string representation of the property name index
    static std::string getPNameAsString(const Base::PName n);
    /// Returns the index for the property name string
    static Base::PName getPNameFromString(const std::string& n);
    /// ADD ALL NEW PROPERTY NAMES HERE...
    static void init();
    /// Adds a user defined property name by index and name. Index must be greater PName::USER (10000)
    static void addUserProperty(unsigned int index, const std::string& name);
    /// User name count
    static unsigned int userNameCnt;

private:
    static std::map<unsigned, std::string> pnameMap;
    static std::map<std::string, unsigned> pstringMap;
};
}  // namespace Base


#define ADD_PNAME(_pname_) \
    { \
        pnameMap[Base::_pname_] = #_pname_; \
        pstringMap[#_pname_] = Base::_pname_; \
    }