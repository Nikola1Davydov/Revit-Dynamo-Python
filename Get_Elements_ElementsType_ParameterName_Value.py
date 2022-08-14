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

allDocs, allElements, allElementsType = [], [], []
name, value, Typname, Typvalue = [], [], [], []
elemType_lst , eType, elemTypeId = [], [], []
# Code
allDocs.append(doc)

#Get Elements and Elements Type bei Category
for cat in cats:
    for a in allDocs:
        elems = FilteredElementCollector(a).OfCategoryId(cat.Id).WhereElementIsNotElementType().ToElements()
        allElements.append(elems)
        elemType = FilteredElementCollector(a).OfCategoryId(cat.Id).WhereElementIsElementType().ToElements()
        allElementsType.append(elemType)
        elemTypeId.append(elemType.Id)
#elemTypeId = [a.Id for a in allElementsType]
#Flatten
elem = [item for sublist in allElements for item in sublist]
elemTyp = [item for sublist in allElementsType for item in sublist]

#Get exemplar Parameters
for e in elem:
    parNameList = e.GetOrderedParameters()
    for parName in parNameList:
        pName = parName.Definition.Name
        if pName.startswith(Prefix):
            name.append(pName)
            value.append(parName.HasValue)

#Get Type Parameters
for e in elemTyp:
    parNameList = e.GetOrderedParameters()
    elemType_lst.append(e.Id)
    for parName in parNameList:
        pName = parName.Definition.Name
        if pName.startswith(Prefix):
            Typname.append(pName)
            Typvalue.append(parName.HasValue)

for el in elemType_lst:
	if el.Id in type_ids:
		eType.append(e)

# Output
#OUT = elem, name, value
OUT = elem, name, value, Typname, Typvalue, eType