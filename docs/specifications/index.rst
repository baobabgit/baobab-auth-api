Spécifications (cahier des charges)
===================================

Cette section est la **source de vérité stable** du besoin. Elle décrit les
**User Stories (US)** et leurs **Features (FEAT)**. Le **backlog** (les tâches,
volatile) vit, lui, dans GitHub Issues / Projects et n'est pas dupliqué ici.

Le **cahier des charges brut** (entrée humaine) se dépose dans
``cahier-des-charges/`` ; le rôle Product Owner en dérive les ``us/`` ci-dessous.
Chaque US/FEAT porte un champ ``:origin:`` indiquant sa provenance (cahier des
charges ou projet externe demandeur).

Hiérarchie et identifiants
--------------------------

================  =====================  ==============================
Niveau            Identifiant            Suivi
================  =====================  ==============================
User Story        ``US-001``             Issue GitHub ``[US-001]``
Feature           ``FEAT-001.1``         Sub-issue ``[FEAT-001.1]``
Tâche (backlog)   ``TASK-001.1.1``       Sub-issue ``[TASK-001.1.1]``
================  =====================  ==============================

Ces identifiants sont propagés dans les commits, les noms de tests et les
docstrings (champ ``:spec:``), assurant la traçabilité besoin → code → test.

.. toctree::
   :maxdepth: 2
   :caption: User Stories

   us/index

.. toctree::
   :maxdepth: 1

   glossary
