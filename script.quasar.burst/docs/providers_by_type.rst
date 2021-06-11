Providers by media type
-----------------------

Using overrides, you can enable or disable providers depending on the type of
media they contain. A `type` field can be set for this.

If a provider should be used for all media types, simply **do not** set its
`type` field, which is the default behavior.

Available types:
  - `movies`
  - `shows` as alias for both
    - `episodes`
    - `seasons`
  - `anime`


.. code-block:: js

    {
        'torlock': {
            'type': 'movies'
        }
    }

If you are using the older Python format:

.. code-block:: js

    overrides = {
        'torlock': {
            'type': 'movies'
        }
    }
