target = "<detector name="/group/clas12/gemc/4a.1.0/experiments/clas12/targets/target" factory="TEXT" variation="lH2"/>"
bst = "detector name="/group/clas12/gemc/4a.1.0/experiments/clas12/bst/bst"        factory="TEXT" variation="java"/>"
cnd = "<detector name="/group/clas12/gemc/4a.1.0/experiments/clas12/cnd/cnd"        factory="TEXT" variation="original"/>"
ctof = "<detector name="/group/clas12/gemc/4a.1.0/experiments/clas12/ctof/ctof"      factory="TEXT" variation="cad"/>"
ctof_cad = "detector name="/group/clas12/gemc/4a.1.0/experiments/clas12/ctof/cad/"      factory="CAD"/>"
htcc = "<detector name="/group/clas12/gemc/4a.1.0/experiments/clas12/htcc/htcc"      factory="TEXT" variation="original"/>"
solenoid = "detector name="/group/clas12/gemc/4a.1.0/experiments/clas12/magnets/solenoid"   factory="TEXT" variation="original"/>"
torus = "<detector name="/group/clas12/gemc/4a.1.0/experiments/clas12/magnets/torus"      factory="TEXT" variation="original"/>"
beamline = "<detector name="/group/clas12/gemc/4a.1.0/experiments/clas12/beamline/beamline" factory="TEXT" variation="FTOn"/>"
ft = "<detector name="/group/clas12/gemc/4a.1.0/experiments/clas12/ft/ft"             factory="TEXT" variation="FTOn"/>"
forwardCarriage = "<detector name="/group/clas12/gemc/4a.1.0/experiments/clas12/fc/forwardCarriage" factory="TEXT" variation="original"/>"
dc = "<detector name="/group/clas12/gemc/4a.1.0/experiments/clas12/dc/dc"              factory="TEXT" variation="java"/>"
ftof = "<detector name="/group/clas12/gemc/4a.1.0/experiments/clas12/ftof/ftof"          factory="TEXT" variation="java"/>"
ec = "<detector name="/group/clas12/gemc/4a.1.0/experiments/clas12/ec/ec"              factory="TEXT" variation="java"/>"
pcal = "<detector name="/group/clas12/gemc/4a.1.0/experiments/clas12/pcal/pcal"          factory="TEXT" variation="java"/>"
ltcc = "<detector name="/group/clas12/gemc/4a.1.0/experiments/clas12/ltcc/ltcc"          factory="TEXT" variation="original"/>"
ltcc_cad_cone = "detector name="/group/clas12/gemc/4a.1.0/experiments/clas12/ltcc/cad_cone/"     factory="CAD"/>"
ltcc_cad = "detector name="/group/clas12/gemc/4a.1.0/experiments/clas12/ltcc/cad/"          factory="CAD"/>"

mustInclude = "	<option name="SCALE_FIELD" value="clas12-torus-big, -1"/>


	<!-- hall field  -->
	<option name="HALL_FIELD"  value="clas12-solenoid"/>


	<!-- fields, precise mode -->
	<option name="FIELD_PROPERTIES" value="clas12-torus-big, 2*mm, G4ClassicalRK4, linear"/>
	<option name="FIELD_PROPERTIES" value="clas12-solenoid, 0.5*mm, G4HelixSimpleRunge, linear"/>


	<!-- beam conditions -->
	<option name="BEAM_P"   value="e-, 4.0*GeV, 0.0*deg, 10*deg"/>
	<option name="SPREAD_P" value="0*GeV, 0*deg, 0*deg"/>


	<option name="SAVE_ALL_MOTHERS" value="0"/>

	<option name="PHYSICS" value="FTFP_BERT + STD + Optical"/>

	<option name="OUTPUT"   value="evio, out.ev"/>

	<!--  Will print message every 10 events -->
	<option name="PRINT_EVENT"    value="10" />


	<!--  RF Signal needs event time window defined by LUMI_EVENT.
	      If Backround is activated make sure to use LUMI_EVENT below instead.-->
	<option name="LUMI_EVENT"  value="0, 248.5*ns, 4*ns" />
	<option name="RFSETUP"     value="0.499, 40, 20" />


	<!--  beam background. for 250 ns timewindow we have 124,000 e- on
	      a LH2 target at 10^35 luminosity
	      I suggest in this case to set SAVE_ALL_MOTHERS to 0
	      or the many tracks will slow down the simulation a lot
	 		For background studies use field in fast mode:
	 -->

	<!--
	<option name="LUMI_EVENT"     value="124000, 248.5*ns, 4*ns" />
	<option name="LUMI_P"         value="e-, 11*GeV, 0*deg, 0*deg" />
	<option name="LUMI_V"         value="(0.,0.,-4.5)cm" />
	<option name="LUMI_SPREAD_V"  value="(0.01, 0.01)cm" />
	 -->"
