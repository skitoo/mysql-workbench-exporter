#!/usr/bin/env python


from mysqlworkbenchexporter.parser.mwbfile import MWBFileParser
from mysqlworkbenchexporter.exporter.doctrine2.annotation import Doctrine2AnnotationExporter


def main():
    parser = MWBFileParser("../test/test.mwb")
    data = parser.parse()
    exporter = Doctrine2AnnotationExporter(data, "../output/")
    exporter.export()

if __name__ == '__main__':
    main()


