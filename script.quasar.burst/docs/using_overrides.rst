Using overrides
---------------

Definitions are loaded from `burst/providers/definitions.py` starting with all
the default providers in the `providers.json` file. You can override existing
definitions using either an `overrides.py` or `overrides.json` file.

Using a Python file is deprecated but will remain supported.

Start by adding a new file named `overrides.json` in your `userdata`_ folder,
ie. in `~/.kodi/userdata/addon_data/script.quasar.burst/overrides.json` and
either paste the content of an existing provider or start with small overrides:

.. code-block:: js

    {
        'torlock': {
            'name': 'MyTorLock'
        }
    }

If you are using the older Python format, put all your overrides in the
`overrides` variable within that file, as such:

.. code-block:: js

    overrides = {
        'torlock': {
            'name': 'MyTorLock'
        }
    }

.. _userdata: http://kodi.wiki/view/Userdata
