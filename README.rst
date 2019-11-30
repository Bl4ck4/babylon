=======
Babylon
=======

Babylon is the API backend for the Mira frontend, designed for fetching recipes.

Description
===========

Herodotus ascribes to her (Semiramis; shorthand Mira) the artificial banks that confined the Euphrates and knows her name as borne by a gate of Babylon

Features
========

Installation
============

Examples
========

Contribute
==========

- Issue Tracker: https://github.com/t-persson/babylon/issues
- Source Code: https://github.com/t-persson/babylon

Support
=======

Start the API development server
--------------------------------

Create a virtual environment

.. code-block::

 virtualenv -p python3 venv

Install all requirements

.. code-block::

 pip install -r requirements.txt

Initialize database

.. code-block::

    cd src
    python -m babylon.app -i

Start the webserver

.. code-block::

 cd src
 python -m babylon.app