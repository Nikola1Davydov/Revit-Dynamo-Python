__author__ = "Nikolai Davydov"
__title__ = "Copy Ebene"

from rpw import revit, db

import clr
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import UIDocument, Selection
from Autodesk.Revit.UI.Selection import ISelectionFilter, ObjectType

uiapp = __revit__
uidoc = uiapp.ActiveUIDocument
app = uiapp.Application
doc = uidoc.Document

Dialogmessage = ""

def GetParameterValue(param):
    if "Double" in str(param.StorageType):
        return param.AsValueString()
    elif "Integer" in str(param.StorageType):
        return param.AsValueString()
    elif "String" in str(param.StorageType):
        return param.AsValueString()
    elif "None" in str(param.StorageType):
        return param.AsValueString()
    elif "ElementId" in str(param.StorageType):
        return param.AsElementId().IntegerValue.ToString()

class CustomISelectionFilter(ISelectionFilter):
    def __init__(self, category_id):
        self.category_id = category_id
    def AllowElement(self, e):
        if e.Category.Id.IntegerValue == -2000011:
            return True
        else:
            return False
    def AllowReference(self, ref, point):
        return False



with db.Transaction("Copy Ebene"):
    try:
        pickedref = uidoc.Selection.PickObject(ObjectType.Element, CustomISelectionFilter(-2000011), "Please select a wall")
        refSet = uidoc.Selection.PickObjects(ObjectType.Element, CustomISelectionFilter(-2000011), "Please select a walls")
        firstElement = pickedref.ElementId

        firstElement = uidoc.Document.GetElement(pickedref)
        firstElement_parameter_BaseOffset = firstElement.get_Parameter(BuiltInParameter.WALL_BASE_OFFSET)
        firstElement_parameter_TopOffset = firstElement.get_Parameter(BuiltInParameter.WALL_TOP_OFFSET)
        firstElement_parameter_LevelBaseOffset = firstElement.get_Parameter(BuiltInParameter.WALL_BASE_CONSTRAINT)
        firstElement_parameter_LevelTopOffset = firstElement.get_Parameter(BuiltInParameter.WALL_HEIGHT_TYPE)
        firstElement_parameter_ManuellOffset = firstElement.get_Parameter(BuiltInParameter.WALL_USER_HEIGHT_PARAM)
        for r in refSet:
            targetElement = uidoc.Document.GetElement(r)
            targetElement_parameter_BaseOffset = targetElement.get_Parameter(BuiltInParameter.WALL_BASE_OFFSET)
            targetElement_parameter_TopOffset = targetElement.get_Parameter(BuiltInParameter.WALL_TOP_OFFSET)
            targetElement_parameter_LevelBaseOffset = targetElement.get_Parameter(BuiltInParameter.WALL_BASE_CONSTRAINT)
            targetElement_parameter_LevelTopOffset = targetElement.get_Parameter(BuiltInParameter.WALL_HEIGHT_TYPE)
            targetElement_parameter_ManuellOffset = targetElement.get_Parameter(BuiltInParameter.WALL_USER_HEIGHT_PARAM)


            targetElement_parameter_BaseOffset.SetValueString(GetParameterValue(firstElement_parameter_BaseOffset))
            targetElement_parameter_LevelBaseOffset.Set(firstElement_parameter_LevelBaseOffset.AsElementId())
            targetElement_parameter_LevelTopOffset.Set(firstElement_parameter_LevelTopOffset.AsElementId())
            if (targetElement_parameter_ManuellOffset.UserModifiable == False):
                targetElement_parameter_ManuellOffset.SetValueString(GetParameterValue(firstElement_parameter_ManuellOffset))
            else:
                targetElement_parameter_TopOffset.SetValueString(GetParameterValue(firstElement_parameter_TopOffset))
    except:
        pass