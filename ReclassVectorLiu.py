# URL of ArcGIS for Server service
# http://qilin.geog.uw.edu:6080/arcgis/rest/services/CLIVIAMA/ReclassVectorLiu2/GPServer

import arcpy

# reclassify table
table = []

def readClassTable(fn):
    """
    read the classify table
    """
    rows = arcpy.SearchCursor(fn) 

    # h = []

    for row in rows:
        x = [row.getValue("lowerbound"), row.getValue("upperbound"), row.getValue('value')]
        # h[row.getValue("FIPSCounty")] = row.getValue("CountyName")
        table.append(x)

    return table



def classify(shapeFile, dbf, inFieldName, outFieldName, default):
    """
      classify the rows in shapefile table, store the result in outFieldName
    """

    # create new field
    arcpy.AddField_management(shapeFile, outFieldName, "DOUBLE")

    # read the classify table
    table = readClassTable(dbf)


    expression = "getClass(float(!"+inFieldName+"!))"

    table_exp = 'table = ' + str(table)

    de_exp = 'default = ' + str(default)

    # find the first match in the classify table, return default if none match
    block = """

def getClass(x):

    for r in table:
        if x >= r[0] and x <= r[1]:
            return r[2]

    return default

"""
    block = table_exp + '\n' + de_exp + '\n' + block

    # calculate the new class
    arcpy.CalculateField_management(shapeFile, outFieldName, expression, "PYTHON_9.3", block)




class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [ReclassVectorLiu]


class ReclassVectorLiu(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Reclassify Vector Data - 458 - Liu"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        shapeFile = arcpy.Parameter(
            displayName="Input shapefile",
            name="shapefile",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")

        tableName = arcpy.Parameter(
            displayName="Input Reclassify Table",
            name="ReclassifyTable",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")

        inFieldName = arcpy.Parameter(
            displayName="Input infield",
            name="infield",
            datatype="GPString",
            parameterType="Required",
            direction="Input")


        outFieldName = arcpy.Parameter(
            displayName="Input outfield",
            name="outfield",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        default = arcpy.Parameter(
            displayName="Input default",
            name="default",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")

        params = [shapeFile, tableName, inFieldName, outFieldName, default]

        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # get parameters
        shapeFile = parameters[0].valueAsText
        tableName = parameters[1].valueAsText
        inFieldName = parameters[2].valueAsText
        outFieldName = parameters[3].valueAsText
        default = parameters[4].valueAsText

        # execute task
        classify(shapeFile, tableName, inFieldName, outFieldName, default)

        return


