
from zipfile import ZipFile
from xml.etree.ElementTree import XML
from mworkbenchexporter.models import Column, Index, Table


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
        tables_ref = {}
        ## tables
        for table in tables.getchildren():
            id_table = table.get("id")
            name = table.find("./value[@key='name']")
            
            t = Table(id_table, name.text)
            tables_ref[id_table] = t
            
            ## columns
            columns = table.find("./value[@key='columns']")
            for column in columns.getchildren():
                name = column.find("./value[@key='name']").text
                length = int(column.find("./value[@key='length']").text)
                simple_type = column.find("./link[@key='simpleType']")
                if simple_type is None:
                    simple_type = column.find("./link[@key='userType']") 
                simple_type = simple_type.text
                auto_increment = bool(int(column.find("./value[@key='autoIncrement']").text))
                is_not_null = bool(int(column.find("./value[@key='isNotNull']").text))
                scale = int(column.find("./value[@key='scale']").text)
                precision = int(column.find("./value[@key='precision']").text)
                c = Column(column.get("id"), name, simple_type, length, auto_increment, is_not_null, scale, precision)
                t.columns.append(c)
                c.table = t
                cols[c.id] = c
            result.append(t)
            
            ## indexes
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
        
        
        for table in tables.getchildren():     
            ## relations
            foreign_keys = table.find("./value[@key='foreignKeys']")
            for foreign_key in foreign_keys.getchildren():
                owner_column =  cols[foreign_key.find("./value[@key='columns']").getchildren()[0].text]
                referenced_column = cols[foreign_key.find("./value[@key='referencedColumns']").getchildren()[0].text]
                owner_column.define_as_foreignkey(referenced_column)
            
        # check many to many
        for table in result:
            if len(table.columns) == 0 and len(table.foreign_keys) == 2:
                fk1 = table.foreign_keys[0]
                fk2 = table.foreign_keys[1]
                fk1.referenced_column.table.foreign_key_targets.remove(fk1)
                fk2.referenced_column.table.foreign_key_targets.remove(fk2)
                result.remove(table)
        return result


