
from mysqlworkbenchexporter.exporter.doctrine2 import TYPES_TABLE_CONVERSION
from mysqlworkbenchexporter.exporter import ExporterOutput, Exporter
import os

        
        

class Doctrine2AnnotationExporter(Exporter):
    def export(self):
        for table in self.data:
            output = ExporterOutput(os.path.join(self.output, table.name.capitalize() + ".php"))
            table_exporter = TableExporter(table, output)
            table_exporter.export()
            output.close()
    

class TableExporter(Exporter):
    def export(self):
        self.output.write_line('<?php')
        self.output.write_blank_line()
        
        self.output.write_line('/**')
        self.output.write_line(' * @Entity')
        self.output.write(' * @Table(name="' + self.data.name.lower() + '"')
        
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
        
        self.output.write_line('class ' + self.data.name.capitalize())
        self.output.write_line('{')
        
        for column in self.data.columns:
            ColumnExporter(column, self.output).export()
            
        for column in self.data.columns:
            ColumnExporter(column, self.output).export_getters_setters()
        
        self.output.write_line('}')
        self.output.write_line('?>')
        
        

class ColumnExporter(Exporter):
    def export(self):
        self.output.write_line('/**', 1)
        type = TYPES_TABLE_CONVERSION[self.data.type]
        if self.data.is_primary:
            self.output.write_line(' * @Id', 1)
        self.output.write(' * @Column(type="%s"'%type, 1)
        if type == 'string':
            self.output.write(', length=%s'%self.data.length)
        elif type == 'decimal' or type == 'double':
            self.output.write(', scale=%s, precision=%s'%(self.data.scale, self.data.precision))
        
        self.output.write(', nullable=%s'% str(not self.data.is_not_null).lower())
        self.output.write(')\n')
        if self.data.auto_increment:
            self.output.write_line(' * @generatedValue(strategy="IDENTITY")', 1)
        self.output.write_line(' */', 1)
        self.output.write_line('private $%s;'%self.data.name.lower(), 1)
        self.output.write_blank_line()
    
    def export_getters_setters(self):
        self.output.write_line('public function get%s()'%self.data.name.capitalize(), 1)
        self.output.write_line('{', 1)
        self.output.write_line('return $this->%s;'%self.data.name.lower(), 2)
        self.output.write_line('}', 1)
        self.output.write_blank_line()
        self.output.write_line('public function set%s($%s)'%(self.data.name.capitalize(), self.data.name.lower()), 1)
        self.output.write_line('{', 1)
        self.output.write_line('$this->%s = $%s;'%(self.data.name.lower(), self.data.name.lower()), 2)
        self.output.write_line('}', 1)
        self.output.write_blank_line()
        
