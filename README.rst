.. raw:: html

   <img src="https://github.com/meghnathomas/MAGNets/blob/master/logo/MAGNets_logo.png" align="center" alt="MAGNets">

A Python package to aggregate and reduce water distribution network models

.. image:: https://img.shields.io/pypi/v/magnets.svg
        :target: https://pypi.python.org/pypi/magnets
        
.. image:: https://pepy.tech/badge/magnets
        :target: https://pepy.tech/project/magnets
        :alt: PyPI - Downloads


Overview
--------

MAGNets (Model AGgregation and reduction of water distribution Networks) is a Python package designed to perform the reduction and aggregation of water distribution network models. The software is capable of reducing a network around an optional operating point and allows the user to customize which junctions they would like retained in the reduced model. MAGNets' reduction approach is based on the variable elimination method proposed by `Ulanicki et al (1996)`_.

.. _`Ulanicki et al (1996)`: https://www.researchgate.net/profile/Fernando-Martinez-Alzamora/publication/273796660_Simplification_of_Water_Distribution_Network_Models/links/550dca050cf2128741674d57/Simplification-of-Water-Distribution-Network-Models.pdf

Requirements
------------

MAGNets has been tested on Python version **3.6**, **3.7**, and **3.8**. A list of its dependencies can be found `here`_.

.. _`here`: https://github.com/meghnathomas/MAGNets/blob/master/requirements.txt

Installation: Stable release
----------------------------

Python distributions, such as Anaconda, are recommended to manage the Python environment as they already contain (or easily support the installation of) many Python packages (such as SciPy and NumPy) that are used in the MAGNets package. Instructions to download and install the Anaconda distribution can be found `at this link`_, and Anaconda for specific versions of Python can be found in the `Anaconda distribution archive`_. This `blog post`_ demonstrates how to easily change the Anaconda Python version to a version compatible with MAGNets using the command prompt.

.. _`at this link`: https://www.anaconda.com/products/distribution

.. _`Anaconda distribution archive`: https://repo.anaconda.com/archive/

.. _`blog post`: https://chris35wills.github.io/conda_python_version/

To install MAGNets, run this command in your terminal:

.. code:: python

   pip install magnets

This is the preferred method to install MAGNets, as it will always install the most recent stable release.

If you don’t have pip installed, this `Python installation guide`_ can guide you through the process.

.. _`Python installation guide`: https://docs.python-guide.org/starting/installation/


Installation: From sources
--------------------------

The sources for MAGNets can be downloaded from the Github repo.

You can either clone the public repository:

.. code:: python

    git clone https://github.com/meghnathomas/MAGNets
    
Or download the tarball:

.. code:: python

    curl -OJL https://github.com/meghnathomas/magnets/tarball/master
    
Once you have a copy of the source, you can install it with:

.. code:: python

    python setup.py install
    

Getting Started
---------------

Use this `jupyter notebook`_ to run some useful examples of MAGNets. Additional example codes and 12 test networks can be found in the `examples`_ and `publications`_ folders.

.. _`jupyter notebook`: https://github.com/meghnathomas/MAGNets/blob/master/examples/MAGNets_Demo.ipynb
.. _`examples`: https://github.com/meghnathomas/MAGNets/tree/master/examples
.. _`publications`: https://github.com/meghnathomas/MAGNets/tree/master/publications

**********************

Once MAGNets is installed on the system, it can be used in a projet through the means of a Python IDE. For example, to use MAGNets on Spyder, open Spyder either through the Anaconda GUI or by typing the following command in the command prompt:

.. code:: python

    spyder
    
Open a new script and import MAGNets using the following command:

.. code:: python

    import magnets as mg

The user can then call on the following function to reduce a hydraulic model of a water distribution network. 

.. code:: python

    wn2 = mg.reduction.reduce_model(inp_file, op_pt, nodes_to_keep, max_nodal_degree)

The parameters of the :code:`reduce_model` function are described as follows:

#. :code:`inp_file`: the EPANET-compatible .inp file of the water distribution network model.

#. :code:`op_pt`: (optional, default = 0) the operating point, or the reporting time step of the hydraulic simulation at which the non-linear headloss equations are linearized.

#. :code:`nodes_to_keep`: (optional, default = []) a list of nodes the user wishes to retain in the reduced model.

#. :code:`max_nodal_degree`: (optional, default = None) the maximum nodal degree of nodes being removed from the model. The nodal degree of a node is equal to the number of pipes incident to the node.

:code:`wn2` contains the water network model object of the reduced model. A .inp file of the reduced model is also written into the directory that contains the .inp file of the original network.

Cite Us
-------
To cite MAGNets, please use the following publication: `MAGNets: Model Reduction and Aggregation of Water Networks`_

.. _`MAGNets: Model Reduction and Aggregation of Water Networks`: https://ascelibrary.org/doi/full/10.1061/JWRMD5.WRENG-5486

::

   @article{doi:10.1061/JWRMD5.WRENG-5486,
    author = {Meghna Thomas  and Lina Sela },
    title = {MAGNets: Model Reduction and Aggregation of Water Networks},
    journal = {Journal of Water Resources Planning and Management},
    volume = {149},
    number = {2},
    pages = {06022006},
    year = {2023},
    doi = {10.1061/JWRMD5.WRENG-5486},
    URL = {https://ascelibrary.org/doi/abs/10.1061/JWRMD5.WRENG-5486},
    }

Contact
-------
Meghna Thomas - meghnathomas@utexas.edu

Lina Sela - linasela@utexas.edu

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
