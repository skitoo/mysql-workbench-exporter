
from mworkbenchexporter.exporter.doctrine2 import TYPES_TABLE_CONVERSION
from mworkbenchexporter.exporter import ExporterOutput, Exporter
from mworkbenchexporter.utils import lower_camel_case, camel_case, pluralize
import os


        

class Doctrine2AnnotationExporter(Exporter):
    def export(self):
        for table in self.data:
            output = ExporterOutput(os.path.join(self.output, camel_case(table.name) + ".php"))
            table_exporter = TableExporter(table, output)
            table_exporter.export()
            output.close()
    

class TableExporter(Exporter):
    def export(self):
        self.output.write_line('<?php')
        self.output.write_blank_line()
        
        self.output.write_line('/**')
        self.output.write_line(' * @Entity')
        self.output.write(' * @Table(name="' + self.data.name + '"')
        
        if len(self.data.indexes) > 0:
            self.output.write_line(',')
            self.output.write(' *        indexes={')
            indexes_display = ''
            for index in self.data.indexes:
                indexes_display += '@Index(name="' + index.name + '", columns={'
                for col in index.columns:
                    indexes_display += '"' + col.name + '", '
                indexes_display = indexes_display.strip(', ')
                indexes_display += '}), '
            self.output.write(indexes_display.strip(', '))
            self.output.write('}')
            
        self.output.write(')\n')
        
        self.output.write_line(' */')
        
        self.output.write_line('class ' + camel_case(self.data.name))
        self.output.write_line('{')
        
        for column in self.data.columns:
            ColumnExporter(column, self.output).export()
            
        for foreign_key in self.data.foreign_keys:
            ForeignKeyExporter(foreign_key, self.output).export()
            
        for foreign_key_target in self.data.foreign_key_targets:
            ForeignKeyTargetExporter(foreign_key_target, self.output).export()
            
        ConstructorExporter(self.data, self.output).export()
            
        for column in self.data.columns:
            ColumnExporter(column, self.output).export_getters_setters()
            
        for foreign_key in self.data.foreign_keys:
            ForeignKeyExporter(foreign_key, self.output).export_methods()
        
        self.output.write_line('}')
        self.output.write_line('?>')

class ConstructorExporter(Exporter):
    def export(self):
        self.output.write_line('/**', 1)        
        self.output.write_line(' *', 1)        
        self.output.write_line(' */', 1)
        self.output.write_line('public function __construct()', 1)
        self.output.write_line('{', 1)
        self.output.write_line('}', 1)
        self.output.write_blank_line()
        

class ColumnExporter(Exporter):
    def export(self):
        self.output.write_line('/**', 1)
        type = TYPES_TABLE_CONVERSION[self.data.type]
        if self.data.is_primary:
            self.output.write_line(' * @Id', 1)
        self.output.write(' * @Column(name="%s", type="%s"'%(self.data.name, type), 1)
        if type == 'string':
            self.output.write(', length=%s'%self.data.length)
        elif type == 'decimal':
            self.output.write(', scale=%s, precision=%s'%(self.data.scale, self.data.precision))
        
        #self.output.write(', unique=%s'% str(self.data.unique).lower())
        self.output.write(', nullable=%s'% str(not self.data.is_not_null).lower())
        self.output.write(')\n')
        if self.data.auto_increment:
            self.output.write_line(' * @GeneratedValue(strategy="AUTO")', 1)
        self.output.write_line(' */', 1)
        self.output.write_line('private $%s;'%lower_camel_case(self.data.name), 1)
        self.output.write_blank_line()
    
    def export_getters_setters(self):
        self.output.write_line('public function get%s()'%camel_case(self.data.name), 1)
        self.output.write_line('{', 1)
        self.output.write_line('return $this->%s;'%lower_camel_case(self.data.name), 2)
        self.output.write_line('}', 1)
        self.output.write_blank_line()
        self.output.write_line('public function set%s($%s)'%(camel_case(self.data.name), lower_camel_case(self.data.name)), 1)
        self.output.write_line('{', 1)
        self.output.write_line('$this->%s = $%s;'%(lower_camel_case(self.data.name), lower_camel_case(self.data.name)), 2)
        self.output.write_line('}', 1)
        self.output.write_blank_line()
        

class ForeignKeyExporter(Exporter):
    def export(self):
        self.output.write_line('/**', 1)
        self.output.write_line(' * @ManyToOne(targetEntiy="%s")'%self.data.referenced_column.table.name, 1)
        self.output.write_line(' * @JoinColumn(name="%s", referencedColumnName="%s")'%(self.data.name, self.data.referenced_column.name), 1)
        self.output.write_line(' */', 1)
        self.output.write_line('private $%s;'%lower_camel_case(self.data.referenced_column.table.name), 1)
        self.output.write_blank_line()
    
    def export_methods(self):
        self.output.write_line('public function get%s()'%camel_case(self.data.referenced_column.table.name), 1)
        self.output.write_line('{', 1)
        self.output.write_line('return $this->%s;'%lower_camel_case(self.data.referenced_column.table.name), 2)
        self.output.write_line('}', 1)
        self.output.write_blank_line()
        self.output.write_line('public function set%s($%s)'%(camel_case(self.data.referenced_column.table.name), lower_camel_case(self.data.referenced_column.table.name)), 1)
        self.output.write_line('{', 1)
        self.output.write_line('$this->%s = $%s;'%(lower_camel_case(self.data.referenced_column.table.name), lower_camel_case(self.data.referenced_column.table.name)), 2)
        self.output.write_line('}', 1)
        self.output.write_blank_line()
        
class ForeignKeyTargetExporter(Exporter):
    def export(self):
        self.output.write_line('/**', 1)
        self.output.write_line(' * @OneToMany(targetEntiy="%s", mappedBy="%s")'%(camel_case(self.data.table.name), lower_camel_case(self.data.name)), 1)
        self.output.write_line(' */', 1)
        self.output.write_line('private $%s;'%pluralize(lower_camel_case(self.data.table.name)), 1)
        self.output.write_blank_line()
        
        