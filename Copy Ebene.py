from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager
from Autodesk.Revit.ApplicationServices import *
from Autodesk.Revit.Attributes import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *

doc = DocumentManager.Instance.CurrentDBDocument

Element_selection = SelectElement(doc)
