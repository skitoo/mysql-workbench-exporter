



class Index(object):
    def __init__(self, name):
        self.name = name
        self.columns = []


class Table(object):
    def __init__(self, id_table, name):
        self.id = id_table
        self.name = name
        self.columns = []
        self.indexes = []
        self.foreign_keys = []
        self.foreign_key_targets = []
        self.many_to_many_connections = []
    
    def __repr__(self):
        return '<Table "%s">'%self.name


class Column(object):
    def __init__(self, id_column, name, data_type, length, auto_increment, is_not_null, scale, precision):
        self.id = id_column
        self.is_primary = False
        self.name = name
        self.type = data_type
        self.length = length
        self.auto_increment = auto_increment
        self.is_not_null = is_not_null
        self.unique = False
        self.scale = scale
        self.precision = precision
        self.is_foreign_key = False
        self.table = None
        
    def define_as_foreignkey(self, referenced_column, is_one_to_one=False):
        self.is_foreign_key = True
        self.is_one_to_one = is_one_to_one
        self.table.foreign_keys.append(self)
        self.table.columns.remove(self)
        self.referenced_column = referenced_column
        self.referenced_column.table.foreign_key_targets.append(self)
        
    def __repr__(self):
        return '<Column "%s">'%self.name
    


class ManyToManyConnection(object):
    def __init__(self, join_table, owner_table, target_table, join_column, owner_column, mapped):
        self.join_table = join_table
        self.owner_table = owner_table
        self.target_table = target_table
        self.join_column = join_column
        self.owner_column = owner_column
        self.target_many_to_many = None
        self.is_mapped = mapped
        
        
        