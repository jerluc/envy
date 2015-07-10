Usage Guide
===========

Creating a new workspace
------------------------

Before you can start to build out your development environment, you will need to first create a new workspace.

.. code-block:: bash

    $ nv c
    Creating workspace [my-env]

This command will create a ``.envy`` directory in the current working directory, where all future workspace tools will be configured and stored.

Once you have created a new workspace, you are now able to enter the workspace environment.

Entering a workspace
--------------------

In order to use any tools or macros built in an existing workspace, you must first enter the workspace environment:

.. code-block:: bash

    $ nv e
    Entering workspace [my-env]; use "exit" to leave this workspace

This command must be executed from the root directory where the ``.envy`` configurationd directory is stored.

To simplify the process of creating a new workspace environment and then immediately entering it afterward, both ``c`` and ``e`` commands may also be invoked at the same time.

.. code-block:: bash

    $ nv c e
    Creating workspace [my-env]
    Entering workspace [my-env]; use "exit" to leave this workspace

Recording a macro
-----------------

One of the most useful features of Envy is the ability to easily record "macros" which are mini scripts to run common sequences of Bash commands. Once you have entered a workspace environment, you can record a macro using the ``record`` command (use the ``exit`` command to finish recording).

.. code-block:: bash

    my-env ⚡ $ record my-macro
    Recording macro "my-macro"; use "exit" to stop recording
    my-env ⚡ $ ▣ echo OH
    OH
    my-env ⚡ $ ▣ echo HAI
    HAI
    my-env ⚡ $ ▣ exit
    exit

Once recorded, you can then use the newly-recorded ``my-macro`` from your environment.

.. code-block:: bash

    my-env ⚡ $ my-macro
    OH
    HAI

Macros are recorded and saved to the ``.envy/macros`` directory, where they can be modified, shared, or removed.

.. raw:: html

    <style>.asciicast { max-height: 500px; }</style>
    <script type="text/javascript" src="https://asciinema.org/a/23272.js" id="asciicast-23272" async data-autoplay="1" data-loop="1"></script>

Destroying a workspace
----------------------

Sometimes (but rarely) it is useful to be able to remove an existing workspace environment. For this task, the ``d`` command can be used.

.. code-block:: bash

    $ nv d