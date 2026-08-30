*************
Mopidy-Subidy
*************

.. image:: https://img.shields.io/pypi/v/Mopidy-Subidy
    :target: https://pypi.org/project/Mopidy-Subidy/
    :alt: Latest PyPI version

A Subsonic backend for Mopidy using `py-sonic
<https://github.com/crustymonkey/py-sonic>`_.


Installation
============

Install the latest release from PyPI by running::

    python3 -m pip install Mopidy-Subidy

Install the development version directly from this repo by running::

    python3 -m pip install https://github.com/justinthegeek/mopidy-subidy/archive/master.zip

See https://mopidy.com/ext/subidy/ for alternative installation methods.


Configuration
=============

Before starting Mopidy, you must add configuration for Mopidy-Subidy to your
Mopidy configuration file::

   [subidy]
   url=https://path.to/your/subsonic/server
   username=subsonic_username
   password=your_secret_password

In addition, the following optional configuration values are supported:

- ``enabled`` -- Defaults to ``true``. Set to ``false`` to disable the
  extension.

- ``legacy_auth`` -- Defaults to ``false``. Setting to ``true`` may solve some
  connection errors.

- ``api_version`` -- Defaults to ``1.14.0``, which is the version used by
  Subsonic 6.2.

- ``cache_ttl`` -- Defaults to ``3600`` (seconds). Controls how long browse,
  lookup, and playlist responses from the Subsonic server are cached before
  being re-fetched. The cache is persisted to disk between Mopidy restarts.


State of this plugin
====================

The following things are supported:

- Browsing all artists/albums/tracks
- Searching for any terms
- Browsing, creating, editing and deleting playlists
- Searching explicitly for one of: artists, albums, tracks

The following things are **not** supported:

- Subsonic's smart playlists
- Searching for a combination of filters (artist and album, artist and track, etc.)


Credits
=======

- Original author: `Frederick Gnodtke <https://github.com/Prior99>`__
- Current maintainer: `justinthegeek <https://github.com/justinthegeek>`__
- `Contributors <https://github.com/justinthegeek/mopidy-subidy/graphs/contributors>`_
