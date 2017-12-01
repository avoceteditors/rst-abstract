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

from sphinx.util.nodes import inline_all_toctrees
from sphinx.util.console import darkgreen, bold
from sphinx.util.osutil import ensuredir
from sphinx.builders import Builder

class MetaBuilder(Builder):
    """ Collects section and rubric titles from doctree
    as well as abstract text and generates a JSON file.
    """

    name = 'meta'

    # Prepare Documents
    def prepare_document(self, docnames):

        # Set Docnames
        self._docnames = docnames

    # Get Target URI's
    def get_target_uri(self, docname, typ=None):
        return docname

    # Get Outdated
    def get_outdated_docs(self):
        return 'all documents'

    # Assemble Doctree
    def assemble_doctree(self, master):
        tree = self.env.get_doctree(master)
        tree = inline_all_toctrees(self, set(), master, tree, darkgreen, [master])
        self.env.resolve_references(tree, master, self)

        return tree

    # Write
    def write(self, *ignored):

        # Fetch Document Names
        docnames = self.env.all_docs

        # Prepare Documents
        self.info(bold("Preparing Documents..."), nonl=True)
        self.prepare_document(docnames)
        self.info("Done")

        # Fetch Master Docname
        master = self.config.master_doc

        # Compile Document
        self.info(bold("Compiling Document"), nonl=True)
        doctree = self.assemble_doctree(master)
        self.info("Done")



    def finish(self):
        if hasattr(self.env, "rst_abstracts"):
            meta = self.env.rst_abstracts

            import json
            try:
                with open(self.config.rstabstract_metadata, 'w') as f:
                    json.dump(meta, f)
            except Exception as e:
                self.warn(bold("Error: Unable to write metadata to %s" %
                    self.config.rstabstract_metadata))
                print(e)





