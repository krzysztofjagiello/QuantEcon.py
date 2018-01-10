"""
Our version of sphinx-apidoc

@author : Spencer Lyon
@date : 2014-07-16

This file should be called from the command line. It accepts one
additional command line parameter. If we pass the parameter `single`
when running the file, this file will create a single directory named
modules where each module in quantecon will be documented. The index.rst
file will then contain a single list of all modules.

If no argument is passed or if the argument is anything other than
`single`, two directories will be created: models and tools. The models
directory will contain documentation instructions for the different
models in quantecon, whereas the tools directory will contain docs for
the tools in the package. The generated index.rst will then contain
two toctrees, one for models and one for tools.

Examples
--------
$ python qe_apidoc.py  # generates the two separate directories
$ python qe_apidoc.py foo_bar  # generates the two separate directories
$ python qe_apidoc.py single  # generates the single directory


Notes
-----
1. This file can also be run from within ipython using the %%run magic.
To do this, use one of the commands above and replace `python` with
`%%run`

2. Models has been removed. But leaving infrastructure here for qe_apidoc
in the event we need it in the future


"""
import os
import sys
from glob import glob


######################
## String Templates ##
######################

module_template = """{mod_name}
{equals}

.. automodule:: quantecon.{mod_name}
    :members:
    :undoc-members:
    :show-inheritance:
"""

game_theory_module_template = """{mod_name}
{equals}

.. automodule:: quantecon.game_theory.{mod_name}
    :members:
    :undoc-members:
    :show-inheritance:
"""

markov_module_template = """{mod_name}
{equals}

.. automodule:: quantecon.markov.{mod_name}
    :members:
    :undoc-members:
    :show-inheritance:
"""

random_module_template = """{mod_name}
{equals}

.. automodule:: quantecon.random.{mod_name}
    :members:
    :undoc-members:
    :show-inheritance:
"""

util_module_template = """{mod_name}
{equals}

.. automodule:: quantecon.util.{mod_name}
    :members:
    :undoc-members:
    :show-inheritance:
"""

all_index_template = """=======================
QuantEcon documentation
=======================

Auto-generated documentation by module:

.. toctree::
   :maxdepth: 2

   {generated}


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""

split_index_template = """=======================
QuantEcon documentation
=======================

The `quantecon` python library consists of a number of modules which
includes game theory (game_theory), markov chains (markov), random
generation utilities (random), a collection of tools (tools),
and other utilities (util) which are
mainly used by developers internal to the package.

.. toctree::
   :maxdepth: 2

   game_theory
   markov
   random
   tools
   util

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""

split_file_template = """{name}
{equals}

.. toctree::
   :maxdepth: 2

   {files}
"""

######################
## Helper functions ##
######################


def source_join(f_name):
    return os.path.join("source", f_name)

####################
## Main functions ##
####################


def all_auto():
    # Get list of module names
    mod_names = glob("../quantecon/[a-z0-9]*.py")
    mod_names = list(map(lambda x: x.split('/')[-1], mod_names))

    # Ensure source/modules directory exists
    if not os.path.exists(source_join("modules")):
        os.makedirs(source_join("modules"))

    # Write file for each module
    for mod in mod_names:
        name = mod.split(".")[0]  # drop .py ending
        new_path = os.path.join("source", "modules", name + ".rst")
        with open(new_path, "w") as f:
            gen_module(name, f)

    # write index.rst file to include these autogenerated files
    with open(source_join("index.rst"), "w") as index:
        generated = "\n   ".join(list(map(lambda x: "modules/" + x.split(".")[0],
                                     mod_names)))
        temp = all_index_template.format(generated=generated)
        index.write(temp)


def model_tool():
    # list file names with game_theory
    game_theory_files = glob("../quantecon/game_theory/[a-z0-9]*.py")
    game_theory = list(map(lambda x: x.split('/')[-1][:-3], game_theory_files))
    # Alphabetize
    game_theory.sort()

    # list file names with markov
    markov_files = glob("../quantecon/markov/[a-z0-9]*.py")
    markov = list(map(lambda x: x.split('/')[-1][:-3], markov_files))
    # Alphabetize
    markov.sort()

    # list file names with random
    random_files = glob("../quantecon/random/[a-z0-9]*.py")
    random = list(map(lambda x: x.split('/')[-1][:-3], random_files))
    # Alphabetize
    random.sort()

    # list file names of tools (base level modules)
    tool_files = glob("../quantecon/[a-z0-9]*.py")
    tools = list(map(lambda x: x.split('/')[-1][:-3], tool_files))
    # Alphabetize
    tools.remove("version")
    tools.sort()

    # list file names of utilities
    util_files = glob("../quantecon/util/[a-z0-9]*.py")
    util = list(map(lambda x: x.split('/')[-1][:-3], util_files))
    # Alphabetize
    util.sort()

    for folder in ["game_theory", "markov", "random", "tools", "util"]:
        if not os.path.exists(source_join(folder)):
            os.makedirs(source_join(folder))

    # Write file for each game_theory file
    for mod in game_theory:
        new_path = os.path.join("source", "game_theory", mod + ".rst")
        with open(new_path, "w") as f:
            equals = "=" * len(mod)
            f.write(game_theory_module_template.format(mod_name=mod, equals=equals))

    # Write file for each markov file
    for mod in markov:
        new_path = os.path.join("source", "markov", mod + ".rst")
        with open(new_path, "w") as f:
            equals = "=" * len(mod)
            f.write(markov_module_template.format(mod_name=mod, equals=equals))

    # Write file for each random file
    for mod in random:
        new_path = os.path.join("source", "random", mod + ".rst")
        with open(new_path, "w") as f:
            equals = "=" * len(mod)
            f.write(random_module_template.format(mod_name=mod, equals=equals))

    # Write file for each tool (base level modules)
    for mod in tools:
        new_path = os.path.join("source", "tools", mod + ".rst")
        with open(new_path, "w") as f:
            equals = "=" * len(mod)
            f.write(module_template.format(mod_name=mod, equals=equals))

    # Write file for each utility
    for mod in util:
        new_path = os.path.join("source", "util", mod + ".rst")
        with open(new_path, "w") as f:
            equals = "=" * len(mod)
            f.write(util_module_template.format(mod_name=mod, equals=equals))

    # write (index|models|tools).rst file to include autogenerated files
    with open(source_join("index.rst"), "w") as index:
        index.write(split_index_template)

    gt = "game_theory/" + "\n   game_theory/".join(game_theory)
    mark = "markov/" + "\n   markov/".join(markov)
    rand = "random/" + "\n   random/".join(random)
    tlz = "tools/" + "\n   tools/".join(tools)
    utls = "util/" + "\n   util/".join(util)
    #-TocTree-#
    toc_tree_list = {"game_theory": gt,
                     "markov": mark,
                     "tools": tlz,
                     "random": rand,
                     "util": utls,
                     }

    for f_name in ("game_theory", "markov", "random", "tools", "util"):
        with open(source_join(f_name + ".rst"), "w") as f:
            m_name = f_name
            if f_name == "game_theory":
                f_name = "Game Theory"                                             #Produce Nicer Title for Game Theory Module
            if f_name == "util":
                f_name = "Utilities"            #Produce Nicer Title for Utilities Module
            temp = split_file_template.format(name=f_name.capitalize(),
                                              equals="="*len(f_name),
                                              files=toc_tree_list[m_name])
            f.write(temp)

if __name__ == '__main__':
    if "single" in sys.argv[1:]:
        all_auto()
    else:
        model_tool()
