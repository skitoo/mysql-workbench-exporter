#!/usr/bin/env python


from mworkbenchexporter.parser.mwbfile import MWBFileParser
from mworkbenchexporter.exporter.doctrine2.annotation import Doctrine2AnnotationExporter


def main():
    parser = MWBFileParser("../test/test.mwb")
#    parser = MWBFileParser("../test/TLMVPSP.mwb")
    data = parser.parse()
    exporter = Doctrine2AnnotationExporter(data, "../output/")
    exporter.export()

if __name__ == '__main__':
    main()


