#===============================================================================
#
# QUIT LEXOCAD.
#
# close()      - Prompts the user to save unsaved files before closing.
# close(False) - Same as above.
# close(True)  - No message is shown. Unsaved changes are lost.
#
#===============================================================================

import Gui
Gui.Lexocad().close(True)