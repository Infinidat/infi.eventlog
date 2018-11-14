Overview
========
A simple utility for parsing Windows Event Log.

Usage
-----

    from infi.eventlog import LocalEventLog
    eventlog = LocalEventLog()
    event = eventlog.event_query().next()
    print event

Checking out the code
=====================

Run the following:

    easy_install -U infi.projector
    projector devenv build

Python 3 support is experimental and not fully tested.
