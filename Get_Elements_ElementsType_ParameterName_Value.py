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

allDocs, allElements, elemTypeId = [], [], []
name, value, Typname, Typvalue = [], [], [], []

# Code
allDocs.append(doc)

#Get Elements bei Category
for cat in cats:
    for a in allDocs:
        elems = FilteredElementCollector(a).OfCategoryId(cat.Id).WhereElementIsNotElementType().ToElements()
        allElements.append(elems)

#Flatten
elem = [item for sublist in allElements for item in sublist]

#Get exemplar Parameters
for e in elem:
    parNameList = e.GetOrderedParameters()
    elemTypeId.append(e.GetTypeId())
    for parName in parNameList:
        pName = parName.Definition.Name
        if pName.startswith(Prefix):
            name.append(pName)
            value.append(parName.HasValue)

#Get ElemType from Elements
elemT = [doc.GetElement(i) for i in elemTypeId]
#filter ElemType
elemTyp = [i for i in elemT if i != None]

#Get Type Parameters
for el in elemTyp:
    parNameList = el.GetOrderedParameters()
    for parName in parNameList:
        pName = parName.Definition.Name
        if pName.startswith(Prefix):
            Typname.append(pName)
            Typvalue.append(parName.HasValue)


name_gesamt = name + Typname
value_gesamt = value + Typvalue

# Output
OUT = elem, name_gesamt, value_gesamt