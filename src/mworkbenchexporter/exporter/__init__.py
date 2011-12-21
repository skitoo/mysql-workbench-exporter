



class ExporterOutput(object):
    def __init__(self, filename):
        self.output = open(filename, "w")
        
    def write_line(self, data, indentation=0):
        self.output.write(" " * 4 * indentation + data + "\n")
        
    def write_blank_line(self):
        self.write_line("")
        
    def write(self, data, indentation=0):
        self.output.write(" " * 4 * indentation + data)
        
    def close(self):
        self.output.close()
        
        
        
class Exporter(object):
    def __init__(self, data, output):
        self.data = data
        self.output = output
        
    def export(self):
        pass