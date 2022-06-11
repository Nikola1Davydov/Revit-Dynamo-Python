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
parNameList = UnwrapElement(IN[1])

allDocs, allElements, allElementsType = [], [], []
name, value, pType, elemType = [], [], [], []

# Code
allDocs.append(doc)

#Get Elements and Elements Type bei Category
for cat in cats:
	for a in allDocs:
		elems = FilteredElementCollector(a).OfCategoryId(cat.Id)
		allElements.append(elems)
		
#Flatten
elem = [item for sublist in allElements for item in sublist]

#Get Parameters
for e in elem:
    for parName in parNameList:
        p = e.LookupParameter(parName)

        
        if p != None:
            name.append(p.Definition.Name)
            value.append(p.HasValue)

# Output
OUT = elem, name, value