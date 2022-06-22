=======
MAGNets
=======


.. image:: https://img.shields.io/pypi/v/magnets.svg
        :target: https://pypi.python.org/pypi/magnets

.. image:: https://travis-ci.com/meghnathomas/MAGNets.svg?branch=master
    :target: https://travis-ci.com/meghnathomas/MAGNets

.. image:: https://readthedocs.org/projects/magnets/badge/?version=latest
        :target: https://magnets.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://pepy.tech/badge/magnets
        :target: https://pepy.tech/project/magnets
        :alt: PyPI - Downloads


A Python package to aggregate and reduce water distribution network models


Overview
--------

MAGNets (Model AGgregation and reduction of water distribution Networks) is a Python package designed to perform the reduction and aggregation of water distribution network models. The software is capable of reducing a network around an optional operating point and allows the user to customize which junctions they would like retained in the reduced model. 


Installation: Stable release
--------

To install MAGNets, run this command in your terminal:

.. code:: python

   pip install magnets

This is the preferred method to install MAGNets, as it will always install the most recent stable release.

If you don’t have pip installed, this `Python installation guide`_ can guide you through the process.

.. _`Python installation guide`: https://docs.python-guide.org/starting/installation/


Installation: From sources
--------

The sources for MAGNets can be downloaded from the Github repo.

You can either clone the public repository:

.. code:: python

    git clone git://github.com/meghnathomas/magnets
    
Or download the tarball:

.. code:: python

    curl -OJL https://github.com/meghnathomas/magnets/tarball/master
    
Once you have a copy of the source, you can install it with:

.. code:: python

    python setup.py install
    

Requirements
--------

MAGNets requires Python version >= 3.6 as well as the installation of the following dependencies:

* wntr >= 0.3.0
* numpy
* scipy
* pandas
* matplotlib 
* networkx
* cycler
* decorator
* kiwisolver
* Pillow
* pyparsing
* python-dateutil
* pytz
* six

Getting Started
--------

To use MAGNets in a project, open a Python console or IDE and import the package using the following command:

.. code:: python

    import magnets as mg

The user can then call on the following function to reduce a hydraulic model of a water distribution network. 

.. code:: python

    wn2 = mg.reduction.reduce_model(inp_file, op_pt, node_to_keep, max_nodal_degree)

The parameters of the :code:`reduce_model` function are described as follows:

#. :code:`inp_file`: the EPANET-compatible .inp file of the water distribution network model.

#. :code:`op_pt`: (optional, default = 0) the operating point, or the reporting time step of the hydraulic simulation at which the non-linear headloss equations are linearized.

#. :code:`nodes_to_keep`: (optional, default = []) a list of nodes the user wishes to retain in the reduced model.

#. :code:`max_nodal_degree`: (optional, default = None) the maximum nodal degree of nodes being removed from the model. The nodal degree of a node is equal to the number of pipes incident to the node.

:code:`wn2` contains the water network model object of the reduced model. A .inp file of the reduced model is also written into the directory of the .inp file of the original network.

Use this `jupyter notebook`_ to run some useful examples of MAGNets. Additional example codes and 12 networks can be found in the `examples`_ folder.

.. _`jupyter notebook`: https://github.com/meghnathomas/MAGNets/blob/master/examples/MAGNets_Demo.ipynb
.. _`examples`: https://github.com/meghnathomas/MAGNets/tree/master/examples

Contact
-------
Meghna Thomas - meghnathomas@utexas.edu

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage