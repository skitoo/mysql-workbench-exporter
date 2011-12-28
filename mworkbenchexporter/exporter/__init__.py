
from mworkbenchexporter.exporter.doctrine2.annotation import Doctrine2AnnotationExporter
from mworkbenchexporter.exporter.doctrine2.yaml import Doctrine2YamlExporter


DOCTRINE2_ANNOTATION = 'doctrine2:annotation'
DOCTRINE2_YAML = 'doctrine2:yaml'

ENGINES_LIST = [DOCTRINE2_ANNOTATION]

def get_exporter(engine):
    if engine == DOCTRINE2_ANNOTATION:
        return Doctrine2AnnotationExporter
    elif engine == DOCTRINE2_YAML:
        return Doctrine2YamlExporter
    else:
        return None


