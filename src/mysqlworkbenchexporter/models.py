



class Index(object):
    def __init__(self, name):
        self.name = name
        self.columns = []


class Table(object):
    def __init__(self, name):
        self.name = name
        self.columns = []
        self.indexes = []
    
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
        self.scale = scale
        self.precision = precision
        
    def __repr__(self):
        return '<Column "%s">'%self.name
    


