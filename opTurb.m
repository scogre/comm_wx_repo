dd=.001;
Ri=dd:dd:10;


khoverkm=(1./(7*Ri))./  (1./(6.873*Ri+(1./(1+6.873*Ri))));

k2=1./(7*Ri);

loglog(Ri, k2, Ri,khoverkm)
legend('1/7Ri','full')
grid






