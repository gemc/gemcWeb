# clas12Tags


This is a series of tags of the GEMC source code to match the various simulation/calibration/reconstruction software versions.

The tags also contain the geometry files and the gcard to run gemc.

Every tag is installed in /group/clas12/gemc

To use: 

source /group/clas12/gemc/environment.csh

If no tag is given, the script will currently load 4a.1.0.

Tags
----

- 4a.1.0: Same as 4a.0.2 with:

  - fixed a bug that affect output file size 
  - fixed bug that affected multiple cad imports
  - added micromegas geometry and hit processes
  - RF output correct frequency in the clas12 gcard
  - updated FT geometry and hit process
  - updated ftof geometry
  - added reading of FTOF reading of tdc conversion constants from the database
  - check if strip_id is not empty in bmt_ and fmt_strip.cc, otherwise fill it.


- 4a.0.2: Same as 4a.0.1 but with full (box, mirrors, pmts shields and WC) LTCC geometry / hit process routine.
- 4a.0.1: Same as 4a.0.0 but with FTOF geometry fix
- 4a.0.0: KPP configuration. Fixes in source and hit process for FTOF, added EC gains. Java geometry uses now coatjava 3. Database fixed for DC geometry. Linear time-to-distance for DC.
  CTOF in the KPP position configuration in the new kpp.gcard.
- 3a.1.0: same as 3a.0.2 but with DC time-to-distance implementation.
- 3a.0.2: same as 3a.0.1 but with CND fix.
- 3a.0.1: same as 3a.0.0 but ctof has status working.
- 3a.0.0: git commit d3a5dc1, Dec 2 2016. Includes FTOF and CTOF paddle delays from CCDB, and CTOF center off-set.



To produce:
-----------

1. create new tag dir
2. change gcard to point to new location
3. change environment.csh to point to the new tag
4. mkdir source, scons -c in $GEMC and copy files from $GEMC - make sure to remove .git files
5. mkdir experiments, copy files from gemcApp/experiments
