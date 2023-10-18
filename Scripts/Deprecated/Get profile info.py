# ===============================================================================
#
# GETTING INFORMATION ABOUT A METAL PROFILE
#
# ===============================================================================

# -----------------------------
# 1. Import Lexocad libraries.
# -----------------------------
import App, Base, Core, Geom, Gui


# ---------------------------------------------------------------------------
# 2. Function that digs inside the profile geometry and returns its details.
# ---------------------------------------------------------------------------
def getProfile(element):
    if element is not None:
        geo = element.getGeometry()
        if geo is not None:
            prop = geo.getPropertyByName("sweptArea")
            if prop is not None:
                link = Core.castToPropertyLinkBase(prop)
                if link is not None:
                    profile = link.getValue()
                    if profile is not None:
                        dict = {}
                        dict['name'] = Base.StringTool.toStlString(
                            profile.getPropertyByName("profileName").getVariant().toString())
                        dict['h'] = profile.getPropertyByName("overallDepth").getVariant().toDouble()
                        dict['b'] = profile.getPropertyByName("overallWidth").getVariant().toDouble()
                        dict['s'] = profile.getPropertyByName("webThickness").getVariant().toDouble()
                        dict['t'] = profile.getPropertyByName("flangeThickness").getVariant().toDouble()
                        dict['r'] = profile.getPropertyByName("filletRadius").getVariant().toDouble()
                        return dict

# ----------------------------
# 3. Get the active document.
# ----------------------------
doc = App.castToDocument(App.GetApplication().getActiveDocument())

# -----------------------------------------------------------------------------------
# 4. Loop on all selected elements and print the information for each metal profile.
# -----------------------------------------------------------------------------------
elements = Gui.getSelectedElements(doc)
if elements.empty():
    print("Select at least 1 metal profile")

for element in elements:
    profile = getProfile(element)
    if profile is not None:  # Make sure we really have a metal profile
        print(profile['name'], " ", profile['h'], " ", profile['b'], " ", profile['s'], " ", profile['t'], " ",
              profile['r'], "\n")