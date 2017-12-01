# Copyright (c) 2017, Kenneth P. J. Dyer <kenneth@avoceteditors.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the name of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from .builder import MetaBuilder
from .nodes import abstract_node
from docutils import nodes
import json

# Fetch Instance
def fetch_instance(node, obj):
    """ Reads through child nodes until it finds the first
    instance of the target type.
    """
    try:
        return node[node.first_child_matching_class(obj)]
    except:
        return None

# Find Parent
def find_parent(node, target):
    """ Recursively checks parent nodes until it locates
    a node of the target type, then return the target node
    instance.
    """
    try:
        parent = node.parent
        if isinstance(parent, target):
            return parent
        else:
            return find_parent(parent, target)
    except:
        return None

# Parse Section
def parse_section(section, env):
    """ Process a section or rubric, find target refid
    and title, then check if the section has an abstract
    directive for additional information.
    """

    target = fetch_instance(section, nodes.target)
    if target is None:
        return (None, None)

    refid = target.get('refid')

    # Fetch Metadata
    abstract = fetch_instance(section, abstract_node)
    parent = find_parent(section, nodes.document)

    # Fetch Docname
    if parent is None:
        return (None, None)
    path = parent.get('source')
    docname = env.path2doc(path)

    # Determine Output
    if abstract is not None:
        body = abstract.astext()
        title = fetch_instance(abstract, nodes.paragraph)[0]

        if isinstance(title, nodes.literal):
            title = "<code>%s</code>" % title.astext()
        else:
            title = title.astext()

    else:
        title = fetch_instance(section, nodes.title).astext()
        body = title

    return (refid, {"title": title, "abstract": body, "docname": docname})

# Fetch Metadata from Doctree
def fetch_metadata(env, doctree):
    """ Process each section and rubric in the doctree,
    extract metadata from the node and set in on return
    dict.
    """

    meta = {}

    # Iterate through Sections
    for section in doctree.traverse(nodes.section):
        (refid, data) = parse_section(section, env)
        if refid is not None:
            meta[refid] = data

    # Iterate through Rubrics
    for rubric in doctree.traverse(nodes.rubric):
        (refid, data) = parse_section(rubric, env)
        if refid is not None:
            meta[refid] = data

    return meta


# Process Sections 
def process_sections(app, doctree, fromdocname):
    """ Event called after doctree-resolved, processes each
    section, rubric and abstract instance to collect metadata
    for other modules.
    
    When not running the MetaBuilder, checks for the JSON file
    that contains reads from the MetaBuilder process.  If it
    finds none, sets an empty dict on rst_abstracts"""

    env = app.builder.env
    path = env.config.rstabstract_metadata

    if isinstance(app.builder, MetaBuilder):
        print("\nLoading metadata from doctree...")
        meta = fetch_metadata(env, doctree)

        setattr(env, 'rst_abstracts', meta)
