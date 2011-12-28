
from mworkbenchexporter.exporter.doctrine2 import TYPES_TABLE_CONVERSION
from mworkbenchexporter.exporter.common import ExporterOutput, Exporter
from mworkbenchexporter.utils import lower_camel_case, camel_case, pluralize
import os, sys



class Doctrine2AnnotationExporter(Exporter):
    def export(self):
        for table in self.data:
            output_file_name = camel_case(table.name) + ".php"
            if self.verbose:
                sys.stdout.write('build %s ... '%output_file_name)
            output = ExporterOutput(os.path.join(self.output, output_file_name))
            table_exporter = TableExporter(table, output)
            table_exporter.export()
            output.close()
            if self.verbose:
                sys.stdout.write('OK\n')
    

class TableExporter(Exporter):
    def export(self):
        self.output.write_line('<?php')
        self.output.write_blank_line()
        self.output.write_line('use Doctrine\ORM\EntityRepository;')
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
            
        for many_to_many in self.data.many_to_many_connections:
            ManyToManyExporter(many_to_many, self.output).export()
            
        ConstructorExporter(self.data, self.output).export()
            
        for column in self.data.columns:
            ColumnExporter(column, self.output).export_getters_setters()
            
        for foreign_key in self.data.foreign_keys:
            ForeignKeyExporter(foreign_key, self.output).export_methods()
            
        for foreign_key_target in self.data.foreign_key_targets:
            ForeignKeyTargetExporter(foreign_key_target, self.output).export_methods()
            
        for many_to_many in self.data.many_to_many_connections:
            ManyToManyExporter(many_to_many, self.output).export_methods()
        
        self.output.write_line('}')
        self.output.write_line('?>')


class ConstructorExporter(Exporter):
    def export(self):
        self.output.write_line('public function __construct()', 1)
        self.output.write_line('{', 1)
        for foreign_key_target in self.data.foreign_key_targets:
            self.output.write_line('$%s = new \Doctrine\Common\Collections\ArrayCollection();'%pluralize(lower_camel_case(foreign_key_target.table.name)), 2)
        for many_to_many in self.data.many_to_many_connections:
            self.output.write_line('$%s = new \Doctrine\Common\Collections\ArrayCollection();'%pluralize(lower_camel_case(many_to_many.target_table.name)), 2)
        self.output.write_line('}', 1)
        self.output.write_blank_line()
        

class ColumnExporter(Exporter):
    def export(self):
        self.output.write_line('/**', 1)
        column_type = TYPES_TABLE_CONVERSION[self.data.type]
        if self.data.is_primary:
            self.output.write_line(' * @Id', 1)
        self.output.write(' * @Column(name="%s", type="%s"'%(self.data.name, column_type), 1)
        if column_type == 'string':
            self.output.write(', length=%s'%self.data.length)
        elif column_type == 'decimal':
            self.output.write(', scale=%s, precision=%s'%(self.data.scale, self.data.precision))
        
        if self.data.unique:
            self.output.write(', unique=%s'% str(self.data.unique).lower())
        if self.data.is_not_null:
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
        self.output.write_line('return $this;', 2)
        self.output.write_line('}', 1)
        self.output.write_blank_line()
        

class ForeignKeyExporter(Exporter):
    def export(self):
        if self.data.is_one_to_one:
            self.output.write_line('/**', 1)
            self.output.write_line(' * @OneToOne(targetEntiy="%s", invertedBy="%s")'%(camel_case(self.data.referenced_column.table.name), lower_camel_case(self.data.table.name)), 1)
            self.output.write_line(' * @JoinColumn(name="%s", referencedColumnName="%s")'%(self.data.name, self.data.referenced_column.name), 1)
            self.output.write_line(' */', 1)
            self.output.write_line('private $%s;'%lower_camel_case(self.data.referenced_column.table.name), 1)
            self.output.write_blank_line()
        else:
            self.output.write_line('/**', 1)
            self.output.write_line(' * @ManyToOne(targetEntiy="%s", inversedBy="%s")'%(self.data.referenced_column.table.name, pluralize(lower_camel_case(self.data.table.name))), 1)
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
        self.output.write_line('return $this;', 2)
        self.output.write_line('}', 1)
        self.output.write_blank_line()


class ForeignKeyTargetExporter(Exporter):
    def export(self):
        if self.data.is_one_to_one:
            self.output.write_line('/**', 1)
            self.output.write_line(' * @OneToOne(targetEntiy="%s", mappedBy="%s")'%(camel_case(self.data.table.name), lower_camel_case(self.data.referenced_column.table.name)), 1)
            self.output.write_line(' */', 1)
            self.output.write_line('private $%s;'%lower_camel_case(self.data.table.name), 1)
            self.output.write_blank_line()
        else:
            self.output.write_line('/**', 1)
            self.output.write_line(' * @OneToMany(targetEntiy="%s", mappedBy="%s")'%(camel_case(self.data.table.name), lower_camel_case(self.data.name)), 1)
            self.output.write_line(' */', 1)
            self.output.write_line('private $%s;'%pluralize(lower_camel_case(self.data.table.name)), 1)
            self.output.write_blank_line()
        
    def export_methods(self):
        if self.data.is_one_to_one:
            self.output.write_line('public function get%s()'%camel_case(self.data.table.name), 1)
            self.output.write_line('{', 1)
            self.output.write_line('return $this->%s;'%lower_camel_case(self.data.table.name), 2)
            self.output.write_line('}', 1)
            self.output.write_blank_line()
            self.output.write_line('public function set%s($%s)'%(camel_case(self.data.table.name), lower_camel_case(self.data.table.name)), 1)
            self.output.write_line('{', 1)
            self.output.write_line('$this->%s = $%s;'%(lower_camel_case(self.data.table.name), lower_camel_case(self.data.table.name)), 2)
            self.output.write_line('return $this;', 2)
            self.output.write_line('}', 1)
            self.output.write_blank_line()
        else:
            self.output.write_line('public function get%s()'%pluralize(camel_case(self.data.table.name)), 1)
            self.output.write_line('{', 1)
            self.output.write_line('return $this->%s;'%pluralize(lower_camel_case(self.data.table.name)), 2)
            self.output.write_line('}', 1)
            self.output.write_blank_line()
            self.output.write_line('public function add%s($%s)'%(camel_case(self.data.table.name), lower_camel_case(self.data.table.name)), 1)
            self.output.write_line('{', 1)
            self.output.write_line('$this->%s->add($%s);'%(pluralize(lower_camel_case(self.data.table.name)), lower_camel_case(self.data.table.name)), 2)
            self.output.write_line('return $this;', 2)
            self.output.write_line('}', 1)
            self.output.write_blank_line()
            self.output.write_line('public function remove%s($%s)'%(camel_case(self.data.table.name), lower_camel_case(self.data.table.name)), 1)
            self.output.write_line('{', 1)
            self.output.write_line('$this->%s->remove($%s);'%(pluralize(lower_camel_case(self.data.table.name)), lower_camel_case(self.data.table.name)), 2)
            self.output.write_line('return $this;', 2)
            self.output.write_line('}', 1)
            self.output.write_blank_line()
            self.output.write_line('public function removeAll%s()'%pluralize(camel_case(self.data.table.name)), 1)
            self.output.write_line('{', 1)
            self.output.write_line('$this->%s->clear();'%pluralize(lower_camel_case(self.data.table.name)), 2)
            self.output.write_line('return $this;', 2)
            self.output.write_line('}', 1)
            self.output.write_blank_line()
        
        
class ManyToManyExporter(Exporter):
    def export(self):
        self.output.write_line('/**', 1)
        if self.data.is_mapped:
            term = 'mappedBy'
        else:
            term = 'inversedBy'
        self.output.write_line(' * @ManyToMany(targetEntiy="%s", %s="%s")'%(camel_case(self.data.target_table.name), term,pluralize(lower_camel_case(self.data.owner_table.name))), 1)
        self.output.write_line(' * @JoinTable(name="%s",'%self.data.join_table.name, 1)
        self.output.write_line(' *    joinColumns={@JoinColumn(name="%s", referencedColumnName="%s")},'%(self.data.join_column.name, self.data.owner_column.name), 1)
        self.output.write_line(' *    inverseJoinColumns={@JoinColumn(name="%s", referencedColumnName="%s")}'%(self.data.target_many_to_many.join_column.name, self.data.target_many_to_many.owner_column.name), 1)
        self.output.write_line(' */', 1)
        self.output.write_line('private $%s;'%pluralize(lower_camel_case(self.data.target_table.name)), 1)
        self.output.write_blank_line()
        
    def export_methods(self):
        self.output.write_line('public function get%s()'%pluralize(camel_case(self.data.target_table.name)), 1)
        self.output.write_line('{', 1)
        self.output.write_line('return $this->%s;'%pluralize(lower_camel_case(self.data.target_table.name)), 2)
        self.output.write_line('}', 1)
        self.output.write_blank_line()
        self.output.write_line('public function add%s($%s)'%(camel_case(self.data.target_table.name), lower_camel_case(self.data.target_table.name)), 1)
        self.output.write_line('{', 1)
        self.output.write_line('$this->%s->add($%s);'%(pluralize(lower_camel_case(self.data.target_table.name)), lower_camel_case(self.data.target_table.name)), 2)
        self.output.write_line('return $this;', 2)
        self.output.write_line('}', 1)
        self.output.write_blank_line()
        self.output.write_line('public function remove%s($%s)'%(camel_case(self.data.target_table.name), lower_camel_case(self.data.target_table.name)), 1)
        self.output.write_line('{', 1)
        self.output.write_line('$this->%s->remove($%s);'%(pluralize(lower_camel_case(self.data.target_table.name)), lower_camel_case(self.data.target_table.name)), 2)
        self.output.write_line('return $this;', 2)
        self.output.write_line('}', 1)
        self.output.write_blank_line()
        self.output.write_line('public function removeAll%s()'%pluralize(camel_case(self.data.target_table.name)), 1)
        self.output.write_line('{', 1)
        self.output.write_line('$this->%s->clear();'%pluralize(lower_camel_case(self.data.target_table.name)), 2)
        self.output.write_line('return $this;', 2)
        self.output.write_line('}', 1)
        self.output.write_blank_line()
        