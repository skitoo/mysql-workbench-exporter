
from mworkbenchexporter.exporter.doctrine2 import TYPES_TABLE_CONVERSION
from mworkbenchexporter.exporter.common import ExporterOutput, Exporter
from mworkbenchexporter.utils import lower_camel_case, camel_case, pluralize
import os, sys



class Doctrine2YamlExporter(Exporter):
    def export(self):
        for table in self.data:
            output_file_name = camel_case(table.name) + ".yml"
            if self.verbose:
                sys.stdout.write('build %s ... '%output_file_name)
            output = ExporterOutput(os.path.join(self.output, output_file_name), 2)
            table_exporter = TableExporter(table, output)
            table_exporter.export()
            output.close()
            if self.verbose:
                sys.stdout.write('OK\n')
                

class TableExporter(Exporter):
    def export(self):
        self.output.write_blank_line()
        self.output.write_line('%s:'%camel_case(self.data.name))
        self.output.write_line('type: entity', 1)
        self.output.write_line('table: %s'%self.data.name, 1)
        
        primary_keys = filter(lambda c:c.is_primary, self.data.columns)
        columns = filter(lambda c:not c.is_primary, self.data.columns)
        
        if len(primary_keys) > 0:
            self.output.write_line('id:', 1)
            for pk in primary_keys:
                PrimaryKeyExporter(pk, self.output).export()
        
        if len(columns) > 0:
            self.output.write_line('fields:', 1)
            for column in columns:
                ColumnExporter(column, self.output).export()
            
        if len(self.data.foreign_keys) > 0:
            self.output.write_line('manyToOne:', 1)
            for foreign_key in self.data.foreign_keys:
                ForeignKeyExporter(foreign_key, self.output).export()
                
        if len(self.data.foreign_key_targets) > 0:
            self.output.write_line('oneToMany:', 1)
            for foreign_key_target in self.data.foreign_key_targets:
                ForeignKeyTargetExporter(foreign_key_target, self.output).export()
                
        if len(self.data.many_to_many_connections) > 0:
            self.output.write_line('manyToMany:', 1)
            for many_to_many in self.data.many_to_many_connections:
                ManyToManyExporter(many_to_many, self.output).export()
                
class PrimaryKeyExporter(Exporter):
    def export(self):
        self.output.write_line('%s:'%self.data.name, 2)
        data_type = TYPES_TABLE_CONVERSION[self.data.type]
        self.output.write_line('type: %s'%data_type, 3)
        if data_type == 'string':
            self.output.write_line('length: %s'%self.data.length, 3)
        elif data_type == 'decimal':
            self.output.write_line('scale: %s'%self.data.scale, 3)
            self.output.write_line('precision: %s'%self.data.precision, 3)
        if self.data.auto_increment:
            self.output.write_line('generator:', 3)
            self.output.write_line('strategy: AUTO', 4)

class ColumnExporter(Exporter):
    def export(self):
        self.output.write_line('%s:'%self.data.name, 2)
        data_type = TYPES_TABLE_CONVERSION[self.data.type]
        self.output.write_line('type: %s'%data_type, 3)
        if data_type == 'string':
            self.output.write_line('length: %s'%self.data.length, 3)
        elif data_type == 'decimal':
            self.output.write_line('scale: %s'%self.data.scale, 3)
            self.output.write_line('precision: %s'%self.data.precision, 3)
        if self.data.unique:
            self.output.write_line('unique: true', 3)
        if self.data.is_not_null:
            self.output.write_line('nullable: false', 3)    
        
        
class ForeignKeyExporter(Exporter):
    def export(self):
        self.output.write_line('%s:'%lower_camel_case(self.data.referenced_column.table.name), 2)
        self.output.write_line('targetEntity: %s'%self.data.referenced_column.table.name, 3)
        self.output.write_line('inversedBy: %s'%pluralize(lower_camel_case(self.data.table.name)), 3)
        self.output.write_line('joinColumn:', 3)
        self.output.write_line('name: %s'%self.data.name, 4)
        self.output.write_line('referencedColumnName: %s'%self.data.referenced_column.name, 4)
        
        
class ForeignKeyTargetExporter(Exporter):
    def export(self):
        self.output.write_line('%s:'%pluralize(lower_camel_case(self.data.table.name)), 2)
        self.output.write_line('targetEntity: %s'%camel_case(self.data.table.name), 3)
        self.output.write_line('mappedBy: %s'%lower_camel_case(self.data.name), 3)
        
        
class ManyToManyExporter(Exporter):
    def export(self):
        self.output.write_line('%s:'%pluralize(lower_camel_case(self.data.target_table.name)), 2)
        self.output.write_line('targetEntity: %s'%camel_case(self.data.target_table.name), 3)
        self.output.write_line('joinTable:', 3)
        self.output.write_line('name: %s'%self.data.join_table.name, 4)
        self.output.write_line('joinColumns:', 4)
        self.output.write_line('%s:'%self.data.join_column.name, 5)
        self.output.write_line('referencedColumnName: %s'%self.data.owner_column.name, 6)
        self.output.write_line('inverseJoinColumns:', 4)
        self.output.write_line('%s:'%self.data.target_many_to_many.join_column.name, 5)
        self.output.write_line('referencedColumnName: %s'%self.data.target_many_to_many.owner_column.name, 5)
        