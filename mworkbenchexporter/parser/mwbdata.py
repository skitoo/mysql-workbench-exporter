
from mworkbenchexporter.models import Column, Index, Table, ManyToManyConnection
import re

class MWBDataParser(object):
    def __init__(self, catalog):
        self.catalog = catalog
        
    def parse(self):
        result = []
        cols_ref = {}
        tables_ref = {}
        for schema in self.catalog.schemata:
            for table in schema.tables:
                t = Table(table, table.name)
                tables_ref[table] = t
                for column in table.columns:
                    if column.simpleType:
                        column_type = re.match(r"{<db.SimpleDatatype> \((?P<name>.*)\)", column.simpleType.__str__()).group('name')
                    else:
                        column_type = re.match(r"{<db.UserDatatype> \((?P<name>.*)\)", column.userType.__str__()).group('name')
                    c = Column(column, column.name, column_type, column.length, False, column.isNotNull, column.scale, column.precision)
                    t.columns.append(c)
                    c.table = t
                    cols_ref['%s:%s'%(t.name, c.name)] = c
                for indice in table.indices:
                    i = Index(indice.name)
                    t.indexes.append(i)
                    for c in indice.columns:
                        c = cols_ref['%s:%s'%(t.name, c.referencedColumn.name)]
                        c.unique = bool(indice.unique)
                        c.is_primary = bool(indice.isPrimary)
                        i.columns.append(c)
                result.append(t)
            
            for table in schema.tables:
                for fk in table.foreignKeys:
                    owner_column = cols_ref['%s:%s'%(table.name, fk.columns[0].name)]
                    referenced_column = cols_ref['%s:%s'%(fk.referencedTable.name, fk.referencedColumns[0].name)]
                    owner_column.define_as_foreignkey(referenced_column, not fk.many)
                    
        # check many to many
        for table in result:
            if len(table.columns) == 0 and len(table.foreign_keys) == 2:
                fk1 = table.foreign_keys[0]
                fk2 = table.foreign_keys[1]
                fk1.referenced_column.table.foreign_key_targets.remove(fk1)
                fk2.referenced_column.table.foreign_key_targets.remove(fk2)
                fk1_many_to_many = ManyToManyConnection(table, fk1.referenced_column.table, fk2.referenced_column.table, fk1, fk1.referenced_column, True)
                fk2_many_to_many = ManyToManyConnection(table, fk2.referenced_column.table, fk1.referenced_column.table, fk2, fk2.referenced_column, False)
                fk1_many_to_many.target_many_to_many = fk2_many_to_many
                fk2_many_to_many.target_many_to_many = fk1_many_to_many
                fk1.referenced_column.table.many_to_many_connections.append(fk1_many_to_many)
                fk2.referenced_column.table.many_to_many_connections.append(fk2_many_to_many)
                result.remove(table)
        return result