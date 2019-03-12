#!/usr/bin/env python

from __future__ import print_function

import sys
import zipfile
import subprocess as sp
from operator import attrgetter
from xml.etree import ElementTree


_, output_jar_path, input_jar_path, pom_file_path = sys.argv

pom_file_tree = ElementTree.parse(pom_file_path)
group_id, artifact_id, version = list(map(attrgetter('text'),
                                          pom_file_tree.getroot()[1:4]))

directory_inside_jar = 'META-INF/maven/{}/{}/'.format(group_id, artifact_id)

# Copy input file to output file
with open(input_jar_path, 'rb') as input_jar:
    with open(output_jar_path, 'wb') as output_jar:
        output_jar.write(input_jar.read())

with zipfile.ZipFile(output_jar_path, 'a') as output_jar:
    # Update the JAR contents to simulate Maven structure

    # pom.xml
    with open(pom_file_path) as pom_file:
        output_jar.writestr(directory_inside_jar + 'pom.xml', pom_file.read())

    # pom.properties
    output_jar.writestr(directory_inside_jar + 'pom.properties', '\n'.join((
        "#Generated by Bazel",
        "#{}".format(sp.check_output('date', env={'LANG': 'C'}).strip()),
        "version={}".format(version),
        "groupId={}".format(group_id),
        "artifactId={}".format(artifact_id)
    )))