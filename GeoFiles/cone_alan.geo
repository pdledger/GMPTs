#
## A cone
#
algebraic3d

# Cone given by bottom circle and top circle
# and cut by planes:

solid boxout = orthobrick (-1000, -1000, -1000; 1000, 1000, 1000) -bco=1;

#solid cutcone = cone ( 0, 0, 0; 15; 0, 0, 30; 1.0 )
#        and plane (0, 0, 0; 0, 0, -1)
#        and plane (0, 0, 30; 0, 0, 1);
#solid cutcone = cone ( 0, 0, 312.5; 1.0; 0, 0, 342.5; 15.0 )
#        and plane (0, 0, 312.5; 0, 0, -1)
#        and plane (0, 0, 342.5; 0, 0, 1);
solid cutcone = cone ( 0, 0, -22.5; 1.0; 0, 0, 7.5; 15.0 )
        and plane (0, 0, -22.5; 0, 0, -1)
        and plane (0, 0, 7.5; 0, 0, 1);


solid rest = boxout and not cutcone;

solid object= cutcone  -maxh=0.9;


tlo rest -transparent -col=[0,0,0];#air
tlo object -col=[1,0,0];#mat1 -mur=1.0 -sig=5.95E+07


