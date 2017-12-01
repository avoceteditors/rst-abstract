##############
RST Abstract
##############

When using Sphinx to generate documentation, have you ever wanted it to programmatically set an arbitrary title or provide an abstract of the target section in links?  RST Abstract is the first stage to providing that.  It introduces an ``abstract`` directive for defining the link title and writing the abstract text.  It also creates a ``meta`` build process, which collects section and rubric titles with abstracts in a JSON file for reference by other extensions.

Installation
=============

Currently, RST Abstract is only available on GitHub.  To install, clone this repository to your local directory, then call the following command:

.. code-block:: console

   $ python3 setup.py install --user

Configuration
==============

In your ``conf.py`` configuration file, add the following lines to add RST Abstract to your builds:

.. code-block:: python

   import rst_abstract
   ...

   extensions = ['rst_abstract']

Usage
=====

RST Abstract provides a dedicated builder for collecting metadata from your project.  To run this builder, run Sphinx calling ``meta``:

.. code-block:: console

   $ sphinx-build -b meta /path/to/source metadata.json

By default, the ``meta`` builder only collects section and rubric titles.  In cases where you would like to provide more information, you can set an abstract under either a section or rubric.  The ``meta`` builder will then read the first child instance under this section for data.

For instance,

.. code-block:: rst

   Section Title
   ==============
   .. _`slug`
   .. abstract:: Link Title

      Abstract text

