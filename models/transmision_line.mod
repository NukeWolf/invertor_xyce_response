* .MODEL coax_lossy LTRA(R=0.2 L=252e-9
*     + C=101e-12
*     + LEN=1)

.MODEL trans_lossy LTRA(R=0.02 L=700n
    + C=3p
    + LEN=10)



.model coax_lumped transline(l=252e-9 c=101e-12)