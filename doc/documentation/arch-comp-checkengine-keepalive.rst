=========
Keepalive
=========

Introduction and goals
======================

The keepalive module implements the long-running helper process pattern used by the Checkmk Microcore (CMC).
Instead of spawning a new Python process for every check execution (which would be prohibitively expensive), the CMC starts helper processes once and keeps them alive.
The core sends commands over stdin / a file descriptor, and the helper processes return check results on the same channel.

As shown in :doc:`arch-comp-omd`, the microcore spawns several helper child processes, including:

* ``cmk --checker`` — the checker helper
* ``cmk --real-time-checks`` — the real-time checks helper

Both are backed by this module (``cmk/base/nonfree/keepalive/``).

The module is an **enterprise-only** component (Checkmk Enterprise License), required only when running with the CMC.
Nagios-based setups use a different, per-invocation execution model.


Architecture
============

White-box overall system
------------------------

.. uml:: arch-comp-checkengine-keepalive-overview.puml

Interfaces
----------

**Inbound (from CMC via stdin / file descriptor):**

* A ``*``-prefixed line triggers a **config reload**.
* Otherwise the line is a **command** (hostname, parameters) parsed by the specific executor, followed by a **timeout** on the next line.

**Outbound (to CMC via file descriptor):**

* Formatted check results: ``<3-digit status>\n<8-digit length>\n<payload>``.
* Individual service results inside the payload use a tab-separated format with optional caching metadata.


Runtime view
============

The ``do_keepalive()`` main loop
--------------------------------

1. Initialise a ``Loader`` (loads the packed config) and a ``CompositeObserver`` (memory, file descriptors, globals).
2. **Loop**, reading lines from stdin:

   a. A ``*``-prefixed line triggers a **config reload** (unless the executor opts out, as ``CheckerExecutor`` does — it reloads by config serial instead).
   b. Otherwise the line is a **command** parsed by the executor class.

3. Read a **timeout** on the next line.
4. Invoke the executor (``__call__``), which runs checks and writes results via ``KeepaliveSubmitter``.
5. Write the formatted result (status code + output) to the core's file descriptor.
6. Run resource observers; restart the process if memory usage exceeds 500 % of its initial size.

.. uml:: arch-comp-checkengine-keepalive-loop.puml


Components that depend on keepalive
====================================

``cmk/base/nonfree/cmc_helpers.py``
   Primary consumer.
   Defines the CLI modes ``--checker`` and ``--real-time-checks``.
   Calls ``do_keepalive()`` with ``CheckerExecutor`` or ``RTCExecutor`` respectively and constructs the ``KeepaliveConfig`` from the packed config.

CMC C++ core (``non-free/packages/cmc/src/CheckHelperPool.cc``)
   The C++ microcore spawns and manages the keepalive helper processes.
   It communicates with them over stdin / file descriptors using the protocol defined in the keepalive module.

``cmk/checkengine/submitters.py``
   References ``KeepaliveSubmitter`` as the enterprise-edition submission path (vs. ``PipeSubmitter`` for Nagios).


Key internal dependencies
=========================

``cmk.checkengine``
   Check execution, parsing, plugin resolution, value store, submitters.

``cmk.base.config`` / ``cmk.base.checkers``
   ``ConfigCache``, ``CheckerConfig``, ``CheckerPluginMapper``, parsers, summarizers.

``cmk.fetchers``
   Decryption of real-time agent data.

``cmk.ccc``
   Exception handling, timeouts, cleanup, host-address types.

``livestatus``
   Querying timeperiod-active status from the core.


Risks and technical debts
=========================

* The ``KeepaliveConfig`` dataclass carries a full ``ConfigCache`` — the TODO in the source acknowledges this is too coarse.
* ``g_total_check_output`` is a module-level mutable global, making the result accumulation hard to test and reason about.
* ``GlobalVariablesObserver`` relies on copying *all* module globals, which is fragile and only runs when verbose logging is enabled.
* The byte-at-a-time ``_read_line()`` implementation is intentionally non-performant to avoid buffering issues; any protocol change could allow a more efficient approach.

