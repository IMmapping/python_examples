import os
import sys
import arcpy
import string
import calendar, datetime, traceback
from arcpy import env
'''
WORKSPACE AND ENVIRONMENT SETUP:



    *******NOTE*********
You need to have a databse connection named "COC_LGIM.sde" in ArcMap or ArcCatalog for the script to run!
'''




#THIS WILL DETERMINE WHERE THE OUTPUT LOG IS WRITTEN
backupTime = time.strftime("%Y_%m_%d_%H%M")

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))
file_path = get_script_path()
# REPLACE 'file_path' WITH DESIRED DIRECTORY FOR OUTPUT LOG IF DIFFERENT FROM SCRIPT LOCATION
os.chdir(file_path)
arcpy.env.overwriteOutput = True
GDBpath = "X:\\GIS\\Scripts\\CAFR\\SourceData.gdb\\"
calcGDB = "X:\\GIS\\Scripts\\CAFR\\CAFR_Calculations.gdb\\"
finalOutput = "X:\\GIS\\Scripts\\CAFR\\final_Output.gdb\\"
arcpy.env.scratchWorkspace = GDBpath
arcpy.env.workspace = GDBpath
centennialBoundary = # enter database connection to boundary here
# FINAL PARCEL OUTPUT NAME:
FinalOutputName = "CAFR_Final"
timeLog = time.strftime("%Y_%m_%d_%H%M")
################################################################################
"""
try:
   '''
    LOG START TIME
    '''
    d = datetime.datetime.now()
    os.chdir("X:\\GIS\\Scripts\\CAFR\\")
    log = open("PythonOutputLogFile.txt","a")
    log.write("----------------------------" + "\n")
    log.write("----------------------------" + "\n")
    log.write("Log: " + str(d) + "\n")
    log.write("\n")
    # Start process...
    starttime = datetime.datetime.now()
    log.write("Begin process:\n")
    log.write("     Process started at "+ str(starttime) + "\n")
    log.write("\n")
    print "Started at " + str(d)

print GDBpath
fcs = arcpy.ListFeatureClasses(GDBpath)
print fcs
for fc in fcs:

    print fc
"""
print "start"
# THIS CALCULATES ALL OF THE DATA FOR THE INDIVIDUAL FEATURE CLASSES
fcList = arcpy.ListFeatureClasses("*","","")
for fc in fcList:
    print fc
    arcpy.AddField_management(fc, fc + "_SQ_FT_ALL", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, fc + "_COUNT", "TEXT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(fc, fc + "_SQ_FT_ALL", "!shape.area@SQUAREFEET !", "PYTHON", "")
    arcpy.AddField_management(fc, fc + "_SQ_FT_CLIP", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, fc + "_Percentage", "FLOAT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.Clip_analysis(fc, centennialBoundary, calcGDB + fc, "")
    arcpy.CalculateField_management(calcGDB + fc, fc + "_SQ_FT_CLIP", "!shape.area@squarefeet!", "PYTHON", "")
    arcpy.CalculateField_management(calcGDB + fc, fc + "_Percentage", "!"+fc+"_SQ_FT_CLIP!/ !"+fc+"_SQ_FT_ALL! * 100", "PYTHON", "")
    featureCount = arcpy.GetCount_management(calcGDB + fc)
    arcpy.CalculateField_management(calcGDB + fc, fc + "_COUNT", str(featureCount))
    fields = arcpy.ListFields(fc)
    # ADD FIELD NAMES BELOW THAT YOU WANT TO KEEP IN THE FINAL OUTPUT.  THIS IS A LIST OF NAMES.  THE WEBSITE IS LOCATED HERE: https://gis.stackexchange.com/questions/101885/how-to-invert-deleting-multiple-fields-with-delete-tool-in-arcgis-10-1-sp1
    keepFields = ["OBJECTID", "OBJECTID_1", "NAME", "DIST_NAME", "DISTRICTNA", "DISTRICT_N", "SHAPEAREA", "SHAPE_Leng", "Shape_Length", "Shape_Area","Shape"]
    dropFields = [x.name for x in fields if x.name not in keepFields]
    arcpy.DeleteField_management(fc,dropFields)
    print fields

arcpy.env.scratchWorkspace = calcGDB
arcpy.env.workspace = calcGDB

#arcpy.CreateFeatureclass_management(out_path="X:/GIS/Scripts/CAFR/CAFR_Calculations.gdb", out_name="CAFR", geometry_type="POLYGON", template="", has_m="DISABLED", has_z="DISABLED", spatial_reference="", config_keyword="", spatial_grid_1="0", spatial_grid_2="0", spatial_grid_3="0")

# NEW CAFR FILE CREATED

fcList = arcpy.ListFeatureClasses("")

arcpy.Merge_management(fcList, finalOutput+"CAFR")

arcpy.TableToExcel_conversion(finalOutput+"CAFR", "X:\\GIS\\Scripts\\CAFR\\CAFR_"+ timeLog +"_.xls")

print "merged"

