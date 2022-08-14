import clr
clr.AddReference('ProtoGeometry')
clr.AddReference('RevitAPI')
clr.AddReference('RevitServices')
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)
from Autodesk.DesignScript.Geometry import *
from Autodesk.Revit.DB import *
from RevitServices.Persistence import DocumentManager

# Variables
doc = DocumentManager.Instance.CurrentDBDocument

cats = UnwrapElement(IN[0])
Prefix = UnwrapElement(IN[1])

allDocs, allElements, test = [], [], []
name, value, pType, elemType = [], [], [], []

# Code
allDocs.append(doc)

#Get Elements and Elements Type bei Category
for cat in cats:
    for a in allDocs:
        elems = FilteredElementCollector(a).OfCategoryId(cat.Id).WhereElementIsNotElementType().ToElements()
        allElements.append(elems)


#Flatten
elem = [item for sublist in allElements for item in sublist]
TTE = []
#Get Parameters
for e in elem:
    parNameList = e.GetOrderedParameters()
    for parName in parNameList:
        pName = parName.Definition.Name
        TTE.append(pName)
        if pName.startswith(Prefix):
	        name.append(pName)
	        value.append(parName.HasValue)
	        pName = parName.Definition.Name


# Output
#OUT = elem, name, value
OUT = elem, name, value