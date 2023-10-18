#===============================================================================
#
# Setting and getting Cadwork attributes
#
#===============================================================================

import App, Base, Core, Geom, Part

doc = App.castToDocument(App.GetApplication().getActiveDocument())

# Creating a sample element.
box = Part.createBox(doc)
elem = App.createElement(doc)
elem.setGeometry(box)
doc.recompute()

# Get the Cadwork attributes associated with the element. Create them if not available.
prop = elem.getPropertyByName("cdwkAttributes")
link = Core.castToPropertyLinkBase(prop)
obj = link.getValue()
if obj is None:
	obj = doc.createObjectFromTypeName("App::CdwkAttributes")
	res = elem.setProperty("cdwkAttributes", obj)

# Setting the values to Cadwork attributes.
obj.setProperty("buildingGroup", "My Group 1")          # <== Set your value here!
obj.setProperty("buildingSubGroup", "My SUB Group 1")   # <== Set your value here!
doc.recompute()

# Get the Cadwork attributes associated with the element.
prop = elem.getPropertyByName("cdwkAttributes")
link = Core.castToPropertyLinkBase(prop)
obj = link.getValue()
if obj is not None:
    group = obj.getPropertyByName("buildingGroup").getVariant().getAsString()
    subGroup = obj.getPropertyByName("buildingSubGroup").getVariant().getAsString()

    print(Base.StringTool.toStlString(group))
    print(Base.StringTool.toStlString(subGroup))
