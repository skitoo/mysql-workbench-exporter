


class ExporterOutput(object):
    def __init__(self, filename, indentation_lenght=4):
        self.output = open(filename, "w")
        self.indentation_lenght = indentation_lenght
        
    def write_line(self, data, indentation=0):
        self.output.write(" " * self.indentation_lenght * indentation + data + "\n")
        
    def write_blank_line(self):
        self.write_line("")
        
    def write(self, data, indentation=0):
        self.output.write(" " * self.indentation_lenght * indentation + data)
        
    def close(self):
        self.output.close()
        
        
        
class Exporter(object):
    def __init__(self, data, output, verbose=False):
        self.data = data
        self.output = output
        self.verbose = verbose
        
    def export(self):
        pass