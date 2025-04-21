#pragma once
#include <algorithm>
#include <numeric>
#include <Base/Type.h>


namespace Base
{
template <class InputIt, class OutputIt, class Pred, class Fct>
void transform_if(InputIt first, InputIt last, OutputIt dest, Pred pred, Fct transform)
{
    while (first != last)
    {
        if (pred(*first))
            *dest++ = transform(*first);
        else
            *dest++ = *first;

        ++first;
    }
}

template <class Cont, class OutputIt, class Pred, class Fct>
void transform_if(Cont container, OutputIt dest, Pred pred, Fct transform)
{
    transform_if(container.cbegin(), container.cend(), dest, pred, transform);
}

template <typename Container, typename OutputIt, typename BinaryFunction>
void transform(Container container, OutputIt out, BinaryFunction function)
{
    std::transform(container.cbegin(), container.cend(), out, function);
}

template <typename Container, typename T, typename BinaryFunction>
T accumulate(Container container, T init, BinaryFunction function)
{
    return std::accumulate(container.cbegin(), container.cend(), init, function);
}


// usage: when we need const std::vector<App::Element*>&, but we have std::vector<App::Wall*> walls, we can use Base::castToBaseContainer<App::Element>(walls);
template <typename To, template <typename...> class Cont, typename FromPtr>
const Cont<To*>& castToBaseContainer(const Cont<FromPtr>& v)
{
    static_assert(std::is_pointer<FromPtr>(), "FromPtr is not a pointer");
    static_assert(std::is_base_of<To, std::remove_pointer_t<FromPtr>>(), "From is not derived from To");

    return *reinterpret_cast<const Cont<To*>*>(&v);
}

template <typename To, template <typename...> class Cont, typename FromPtr>
Cont<To*>& castToBaseContainer(Cont<FromPtr>& v)
{
    static_assert(std::is_pointer<FromPtr>(), "FromPtr is not a pointer");
    static_assert(std::is_base_of<To, std::remove_pointer_t<FromPtr>>(), "From is not derived from To");

    return *reinterpret_cast<Cont<To*>*>(&v);
}


template <typename Val, typename Cont>
bool allSubtype(const Cont& cont)
{
    return all_of(begin(cont), end(cont), [](auto val) { return dynamic_cast<Val>(val) != nullptr; });
}

/**
 * \brief Tests if at least one element of the container is a subclass (dynamic castable) of at least one of the Derivates.
 * E.g. we have a vector<Element*> elems and we want to know if any of the elements is a subclass of either one of those:
 * App::CrossSectionElement, App::CrossPlaneElement, App::ElevationElement.
 * We tests is like this: isAnyDerivedFrom<App::Element,vector,App::CrossSectionElement, App::CrossPlaneElement, App::ElevationElement>(elems).
 * There is a couple of specializations in App/ContainerTool.h for more call convenience.
 *
 * \tparam BaseClass Polymorphic Base.
 * \tparam Cont Simple container type compatible with std::ranges.
 * \tparam Derivates Pack of types to be tested.
 * \param container Conatainer of pointers to BaseClass.
 * \return true if the above holds.
 */
template <typename BaseClass, template <typename...> class Cont, typename... Derivates>
bool isAnyDerivedFrom(const Cont<BaseClass*>& container)
{
    return std::any_of(begin(container),end(container), [](const auto v) { return ((dynamic_cast<Derivates*>(v) != nullptr) || ...); });
}

template <class T>
inline void hash_combine(std::size_t& seed, const T& v)
{
    std::hash<T> hasher;
    seed ^= hasher(v) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
}

struct hash_pair
{
    template <class T1, class T2>
    size_t operator()(const std::pair<T1, T2>& p) const
    {
        std::size_t seed = 0;
        hash_combine(seed, p.first);
        hash_combine(seed, p.second);
        return seed;
    }
};

}