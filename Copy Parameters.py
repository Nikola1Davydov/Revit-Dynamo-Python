__author__ = "Nikolai Davydov"
__title__ = "Copy \\nParameters"

import sys
import rpw
from rpw import revit, db, ui
from rpw.utils.dotnet import List
from rpw.base import BaseObjectWrapper, BaseObject
from rpw.exceptions import RpwTypeError, RevitExceptions
from rpw.utils.logger import logger
from rpw.utils.coerce import to_element_ids, to_elements, to_iterable
from rpw.db.collection import ElementSet
from rpw.db.reference import Reference
from rpw.db.xyz import XYZ
from rpw.db.element import Element
from rpw.ui.forms import Alert


# def GetParameterValue(param):
#     if "Double" in str(param.StorageType):
#         return param.AsValueString()
#     elif "Integer" in str(param.StorageType):
#         return param.AsValueString()
#     elif "String" in str(param.StorageType):
#         return param.AsValueString()
#     elif "None" in str(param.StorageType):
#         return param.AsValueString()
#     elif "ElementId" in str(param.StorageType):
#         return param.AsElementId().IntegerValue.ToString()


pickedref = ui.Pick.pick_element(
    msg="Please select an element", multiple=False)
refSet = ui.Pick.pick_element(msg="Please select an element", multiple=True)

Dialogmessage = ""

firstElement = pickedref.get_element()
paramSet_firstElement = firstElement.GetOrderedParameters()

with db.Transaction("Copy Parameters"):
    for firstElement_param in paramSet_firstElement:
        name = firstElement_param.Definition.Name
        if name.startswith("sop_"):
            param_id = firstElement_param.Id.IntegerValue
            firstElement_value = firstElement.parameters[name].value
            try:
                for r in refSet:
                    elements_selection = r.get_element()
                    elements_selection.parameters[name] = firstElement_value
                Dialogmessage += name + "\n"
            except:
                pass
    Alert(Dialogmessage, title = "Copy Parameters", header = "folgende Parameter haben neue Werte")
