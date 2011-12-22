
from mworkbenchexporter.exporter.doctrine2.annotation import Doctrine2AnnotationExporter


DOCTRINE2_ANNOTATION = 'doctrine2:annotation'


def get_exporter(engine):
    if engine == DOCTRINE2_ANNOTATION:
        return Doctrine2AnnotationExporter
    else:
        return None


