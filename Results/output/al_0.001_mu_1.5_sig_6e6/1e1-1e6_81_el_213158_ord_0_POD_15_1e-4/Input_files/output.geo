#algebraic3d

#solid sphout = sphere (0, 0, 0; 200);
#solid sphin = sphere (0, 0, 0; 1) -maxh=0.1;

#solid rest = sphout and not sphin;

tlo rest -transparent -col=[0,0,1];#air
tlo object  -col=[1,0,0];#mat1 -mur=1.5 -sig=6E+06
