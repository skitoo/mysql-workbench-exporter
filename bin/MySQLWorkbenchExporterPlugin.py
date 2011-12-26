
from mworkbenchexporter.exporter import get_exporter, DOCTRINE2_ANNOTATION
from mworkbenchexporter.parser.mwbdata import MWBDataParser
import mworkbenchexporter

from wb import *
import grt
from mforms import FileChooser, OpenDirectory


ModuleInfo = DefineModule(name= "MySQLWorkbenchExporter", author= mworkbenchexporter.__author__, version=mworkbenchexporter.__version__)


@ModuleInfo.plugin("mysqlworkbenchexporter.export_to_doctrine2_annotation", caption= "Export to Doctrine 2 Annotation", input= [wbinputs.currentCatalog()], pluginMenu= "Catalog")
@ModuleInfo.export(grt.INT, grt.classes.db_Catalog)
def export_to_doctrine2_annotation(catalog):
    file_chooser = FileChooser(OpenDirectory)
    if file_chooser.run_modal():
        output_path = file_chooser.get_path()
        parser = MWBDataParser(catalog)
        data = parser.parse()
        Exporter = get_exporter(DOCTRINE2_ANNOTATION)
        Exporter(data, output_path).export()
    return 0

