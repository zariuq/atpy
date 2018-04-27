ENIGMA
======

O Brave man!  You've come so far, don't let it slip away...


Quick start
-----------


Requirements
------------

You can use binaries provided in `bin/` compiled for x86.  Otherwise you need
AI4Reason fork of E with Enigma support.  You can obtain it from github, like
this:

   $ git clone https://github.com/ai4reason/eprover.git
   $ cd eprover
   $ git fetch
   $ git checkout ENIGMA

Then compile E and (included) LIBLINEAR:

   $ ./configure
   $ make 
   $ cd CONTRIB/liblinear
   $ make

You need the following binaries in your `PATH` for *atpy* to work:

   PROVER/eprover
   SIMPLE_APPS/enigma-features
   CONTRIB/liblinear/train
   CONTRIB/liblinear/predict


Installation
------------

Directory `atpy` should be added to your `PYTHONPATH`.


Usage
-----

