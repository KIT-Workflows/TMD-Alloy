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
      
      subroutine cell(cellvector,a,b,c,alpha,beta,gamma)
      implicit none
      
      REAL, PARAMETER:: degtorad=3.1415926/180.0
 
      REAL, DIMENSION(3,3):: cellvector
      REAL :: a,b,c,alpha, beta, gamma, alp, bet, gam, cosa, cosb, cosg, sing
      REAL :: trm1      
      


      if (alpha.eq.90.0) then
        cosa=0.0d0
      else
        alp=alpha*degtorad
        cosa=cos(alp)
      endif
      if (beta.eq.90.0) then
        cosb=0.0d0
      else
        bet=beta*degtorad
        cosb=cos(bet)
      endif
      if (gamma.eq.90.0) then
        sing=1.0d0
        cosg=0.0d0
      else
        gam=gamma*degtorad
        sing=sin(gam)
        cosg=cos(gam)
      endif
      cellvector(2,1)=0.0d0
      cellvector(3,1)=0.0d0
      cellvector(3,2)=0.0d0
      cellvector(1,1)=a
      cellvector(1,2)=b*cosg
      cellvector(2,2)=b*sing
      cellvector(1,3)=c*cosb
      cellvector(2,3)=c*(cosa-cosg*cosb)/sing
      trm1=cellvector(2,3)/c
      cellvector(3,3)=c*sqrt(1.0d0-cosb**2-trm1**2)
      return
      end

