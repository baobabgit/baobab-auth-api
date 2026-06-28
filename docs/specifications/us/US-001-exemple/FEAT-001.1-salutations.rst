FEAT-001.1 — Générer des salutations
====================================

:Rattachée à: :ref:`us-001`
:Issue GitHub: ``[FEAT-001.1]`` (sub-issue de ``[US-001]``)
:Implémentation: :class:`example_package.greeter.Greeter`

Description
-----------

Fournir une classe capable de produire une salutation, formelle ou informelle,
à partir d'un nom valide.

Critères d'acceptation
----------------------

#. ``greet()`` renvoie une salutation informelle.
#. ``greet(formal=True)`` renvoie une salutation formelle.
#. Un nom vide lève ``ValueError``.

Tâches (backlog — suivies dans GitHub)
--------------------------------------

* ``TASK-001.1.1`` Implémenter la classe ``Greeter``.
* ``TASK-001.1.2`` Couvrir ``Greeter`` par des tests (≥ 90 %).
