
from zipfile import ZipFile
from xml.etree.ElementTree import XML
from mysqlworkbenchexporter.models import Column, Index, Table


class MWBFileParser(object):
    def __init__(self, path):
        self.path = path
        
    def parse(self):
        f = ZipFile(self.path, "r")
        data_xml = f.read('document.mwb.xml')
        tree = XML(data_xml)
        catalog = tree.find(".//value[@key='catalog']")
        tables = catalog.find(".//value[@key='tables']")
        
        result = []
        cols = {}
        for table in tables.getchildren():
            name = table.find("./value[@key='name']")
            t = Table(name.text)
            columns = table.find("./value[@key='columns']")
            
            for column in columns.getchildren():
                name = column.find("./value[@key='name']")
                length = column.find("./value[@key='length']")
                simple_type = column.find("./link[@key='simpleType']")
                auto_increment = column.find("./value[@key='autoIncrement']")
                is_not_null = column.find("./value[@key='isNotNull']")
                scale = column.find("./value[@key='scale']")
                precision = column.find("./value[@key='precision']")
                c = Column(column.get("id"), name.text, simple_type.text, int(length.text), bool(int(auto_increment.text)), bool(int(is_not_null.text)), int(scale.text), int(precision.text))
                t.columns.append(c)
                cols[c.id] = c
            result.append(t)
            
            indexes = table.find("./value[@key='indices']")
            for index in indexes:
                i = Index(index.find("./value[@key='name']").text)
                t.indexes.append(i)
                columns = index.find("./value[@key='columns']")
                is_primary = bool(int(index.find("./value[@key='isPrimary']").text))
                for column in columns:
                    col = cols[column.find("./link[@key='referencedColumn']").text]
                    col.is_primary = is_primary
                    i.columns.append(col)
        return result

