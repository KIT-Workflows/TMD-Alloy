!*******************************************************************************
!    Copyright (c) 2014 Ricardo Grau-Crespo, Said Hamad
!
!    This file is part of the SOD package.
!
!    SOD is free software: you can redistribute it and/or modify
!    it under the terms of the GNU General Public License as published by
!    the Free Software Foundation, either version 3 of the License, or
!    (at your option) any later version.
!
!    SOD is distributed in the hope that it will be useful,
!    but WITHOUT ANY WARRANTY; without even the implied warranty of
!    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
!    GNU General Public License for more details.
!
!    You should have received a copy of the GNU General Public License
!    along with SOD.  If not, see <http://www.gnu.org/licenses/>.
!
!******************************************************************************

    PROGRAM invertOUTSOD 
       IMPLICIT NONE


       INTEGER :: i,j,k,p,q,m,m1,m2,Mm,Mm1,Mm2,op,nop,npos,pos,nsubs,aux
       INTEGER :: posInverted
       CHARACTER*20 :: auxstring
       INTEGER,DIMENSION(:), ALLOCATABLE:: omega
       INTEGER,DIMENSION(:,:), ALLOCATABLE:: conf, confInverted


!!!!!! Input files

       OPEN (UNIT=10,FILE="OUTSOD_original")

!!!!!! Output files

       OPEN (UNIT=11,FILE="OUTSOD_inverted")

!
! DEFINITION OF VARIABLES:
!
! nsubs               numbers of substitutions
! npos		      Number of atoms of the target species 
! pos		      Index for the positions
! conf		      List of all independent configurations for the structure with nsubs substitutions 
! conf1		      List of all independent configurations for the structure with 1 substitutions 
! conf2		      List of all independent configurations for the structure with 2 substitutions 
!                     All configurations are given as a list of the substituted positions
! m		      Index for the configurations (conf)     
! Mn                  Total number of configurations in conf (m=1,Mm)
! m1		      Index for the configurations (conf1) for the structure with 1 defect    
! Mm1                 Total number of configurations in conf1 (m1=1,Mm1) for the structure with 1 defect    
! m2		      Index for the configurations (conf2) for the structure with 2 defects    
! Mm2                 Total number of configurations in conf2 (m2=1,Mm2) for the structure with 2 defects    



!       WRITE (*,*) "**************************************************************************** " 
!       WRITE (*,*) "         SOD (Site Occupancy Disorder) program, version 0.43  " 
!       WRITE (*,*) "         Module invertSOD                                                    " 
!       WRITE (*,*) " " 
!       WRITE (*,*) "         Authors: R. Grau-Crespo and S. Hamad                                " 
!       WRITE (*,*) " " 
!       WRITE (*,*) "         Contact:  <r.grau-crespo@reading.ac.uk> " 
!       WRITE (*,*) "**************************************************************************** " 
!       WRITE (*,*) " " 
!       WRITE (*,*) " " 
!       WRITE (*,*) " " 
!       WRITE (*,*) "Reading input files..." 
!       WRITE (*,*) " " 

!ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
!      Reading the original OUTSOD file 
!ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc


!          10  substitutions in 12 sites
!           5  configurations
!     1      6    1    2    3    4    5    6    7    8    9   10
!     2     24    1    2    3    4    5    6    7    8    9   11
!     3      6    1    2    3    4    5    7    8    9   10   11
!     4      6    1    2    3    4    5    7    8    9   10   12


        read(10,*)  nsubs,auxstring,auxstring,npos
        write(11,*) npos-nsubs,"substitutions in",npos,"sites"
        read(10,*)  Mm
        write(11,*) Mm,"configurations"

        ALLOCATE(conf(1:Mm,1:nsubs))
        ALLOCATE(confInverted(1:Mm,1:npos-nsubs))
        ALLOCATE(omega(1:Mm))

        do m=1,Mm
           read(10,*)   aux,omega(m),conf(m,1:nsubs)
        enddo


        do m=1,Mm
           posInverted=0
           do pos=1,npos
               if (.NOT. ANY( conf(m,:)==pos) ) then
                  posInverted=posInverted+1
                  confInverted(m,posInverted)=pos
              endif
           enddo
        enddo


        do m=1,Mm
           write(11,10)   m,omega(m),confInverted(m,1:npos-nsubs)
  10       format(i6,1x,i6,30(1x,i4))
        enddo




!!!!!!Deallocating arrays
       DEALLOCATE(conf)
       DEALLOCATE(confInverted)
       DEALLOCATE(omega)



    END PROGRAM invertOUTSOD

