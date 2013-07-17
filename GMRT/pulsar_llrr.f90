! perform SVD on pulsar
! diagonalize ll and rr separately, and apply their product on lr
!
integer, parameter :: n=64,nout=1,nt=6,nchan=64,ncorrtot=nchan*(nchan+1)/2,ncorr=ncorrtot,nr=1

complex, dimension(n,ncorr) :: cmatin,cmatin1
complex, dimension(n,ncorr) :: cmatinc,cmatt
complex, dimension(n,ncorr,nt) :: cmatinctime
complex, dimension(nout,ncorr) :: cmatout
complex, dimension(ncorr,nt) :: cmattout
complex, dimension(ncorr) :: cmattnorm,cmatnorm,cmatnorm1,cmatnormin,canorm
real, dimension(ncorr) :: rmask
real, dimension(nchan) :: weight
character*80 fn

cmatnormin=1
klmax=5
weight=1.0
weight(5:32)=0.01
weight(37:)=0.01
!weight((/9,10,11,12/))=0.01 !Set tracking to 1.0
!weight((/1,2,3,4,5,6,7,8,13,14/))=1.0 !Set a few good drifters
k=0
do i=1,nchan
   do j=i,nchan
      k=k+1
      cmatnormin(k)=1/(weight(i)*weight(j))
   end do
end do
fn='onegate.float'

write(*,*) 'opening ',fn
open(30,file=fn,status='old',form='binary')
!   1234567891123456789212345678931234567894123456789512345

cmatinc=0
do i=1,nt
   read(30) cmatin
   cmatin=cmatin/spread(cmatnormin,1,n)
   cmatinctime(:,:,i)=cmatin
enddo 
!cmatt=cmatinc
call rmedian(cmatt,cmatinctime,nt,2*n*ncorr)
call cutrm(cmatt,n,ncorr)
call pca(cmatt,n,nchan)

do kl=1,klmax
   write(*,*) 'kl=',kl
   rewind(30)
   cmatout=0
   if (kl .eq. klmax) then
      open(100,file='cmatoutvec.dat')
      open(200,file='cmatoutval.dat')
   endif
   do k=1,nt
      cmatout=0
      cmatin=0
      read(30) cmatin1
      cmatin1=cmatin1/spread(cmatnormin,1,n)
      cmatin=cmatin+cmatin1
      cmatin=cmatin*conjg(cmatt)/abs(cmatt+1.e-20)/sum(abs(cmatt)/n/ncorr)
      do j=1,n
         cmatout=cmatout+cmatin(j::n,:)      
      enddo
      call cmedian(cmatout,transpose(cmatin),n,ncorr)
      call pca(cmatout,nout,nchan)
      cmattout(:,k)=cmatout(1,:)
   end do
! normalize phases to be 1 at the beginning
   cmattout=cmattout*spread(conjg(cmattout(:,1))/abs(cmattout(:,1)),2,nt)
! normalize the time average gain on each antenna to be one
   cmattout=cmattout/spread(sqrt(sum(abs(cmattout)**2,2)/nt),2,nt)
   if (kl .eq. klmax) then
      close(200)
      close(100)
   endif
   rewind(30)
   cmatinc=0
   cmattout=cmattout/sqrt(sum(abs(cmattout**2))/(nt*ncorr))
   cmattnorm=sum(abs(cmattout)**2,2)
   do i=1,nt
      read(30) cmatin
      cmatin=cmatin/spread(cmatnormin,1,n)
      cmatin=cmatin*spread(conjg(cmattout(:,i)),1,n)
      cmatinctime(:,:,i)=cmatin
   enddo
   !cmatt=cmatinc
   call rmedian(cmatt,cmatinctime,nt,2*n*ncorr)
   if (kl .eq. klmax) then
      open(100,file='bandpassvec0.dat')
      open(200,file='bandval.dat')
   endif

call cutrm(cmatt,n,ncorr)
   call pca(cmatt,n,nchan)
enddo
open(10,file='cmatt.dat',form='binary')
write(10) cmatt
close(10)
rewind(30)
open(10,file='modelcal.dat',form='binary')
open(20,file='datacal.dat',form='binary')
open(25,file='modelraw.dat',form='binary')
cmattnorm=cmattnorm+1.e-20
cmatnorm=0
cmatnorm1=0

do i=1,nt
      read(30) cmatin
      cmatin=cmatin/spread(cmatnormin,1,n)
      cmatin=cmatin*conjg(cmatt)*spread(conjg(cmattout(:,i)),1,n)
      cmatin1=cmatt*conjg(cmatt)*spread(abs(cmattout(:,i))**2/cmattnorm,1,n)
      cmatnorm=cmatnorm+sum(cmatin*conjg(cmatin1),1)
      cmatnorm1=cmatnorm1+sum(abs(cmatin1)**2,1)
      write(20) cmatin
      write(25) (cmatt)*spread((cmattout(:,i)),1,n)
      write(10) cmatin1 !,cmatin,cmatin-cmatin1
end do
close(10)
close(20)
end

subroutine cmedian(ca,cb,nt,n)
complex, dimension(n,nt) :: cb
complex, dimension(n) :: ca
real, dimension(n,nt) :: b
real, dimension(n) :: ar,ai

b=real(cb)
call rmedian(ar,b,nt,n)
b=aimag(cb)
call rmedian(ai,b,nt,n)
ca=cmplx(ar,ai)
end subroutine cmedian


subroutine rmedian(a,b,nt,n)
real, dimension(n,nt) :: b
real, dimension(n) :: a
real, dimension(nt) :: t
integer, dimension(nt) :: iorder


!  a=sum(b,2)
!  return
  do in=1,n
     t=b(in,:)
     if (.true.) then
     call quick_sort(t,iorder,nt)
     else
     do i=1,nt
        do j=1,nt-i
           if (t(j)<t(j+1)) then
              tmp=t(j)
              t(j)=t(j+1)
              t(j+1)=tmp
           endif
        enddo
     enddo
     endif
     if (mod(nt,2) .eq. 0) then
        a(in)=(t(nt/2)+t(nt/2+1))/2
     else
        a(in)=t((nt+1)/2)
     endif
  end do
  a=a*nt
end subroutine rmedian


subroutine pca(cmat,n,nchan)
  complex, dimension(n,nchan*(nchan+1)/2) :: cmat,cmatdiff,cmatin,cmat1,cmat2
  complex, dimension(nchan/2,nchan/2) :: sfvecll,sfvecrr,stmp
  complex, dimension(n,nchan)::ovec1
  complex, dimension(nchan/2)::ovecll,ovecrr,cphase
  complex ctmp
  CHARACTER     JOBZ, UPLO
  INTEGER       INFO, LDA, N, LWORK
  REAL          RWORK( 3*nchan-2 ), W( nchan/2 )
  COMPLEX       WORK( 10000*nchan )
  integer mloc(1)
integer, dimension(nchan) :: ipol,iantenna


!not sure value of nchan, assuming 64
if (nchan .eq. 60) then
   ipol=0
   ipol(29:58)=1
   iantenna(:28)=(/(i,i=1,28)/)
   iantenna(29:58)=(/(i,i=1,30)/)
   iantenna(59:60)=(/29,30/)
else
   ipol=0
   ipol(nchan/2+1:nchan)=1
   iantenna(:nchan/2)=(/(i,i=1,nchan/2)/)
   iantenna(nchan/2+1:nchan)=(/(i,i=1,nchan/2)/)
endif


  cmatin=cmat
  LWORK=10000*nchan
  JOBZ='V'
  UPLO='U'
  LDA=nchan/2
  do ic=1,n
     k=0
     do i=1,nchan
        do j=i,nchan
           k=k+1
           if (ipol(i) .ne. ipol(j)) cycle
           i1=iantenna(i)
           j1=iantenna(j)
           if (ipol(i) .eq. 0) then
              sfvecll(i1,j1)=cmat(ic,k)
              sfvecll(j1,i1)=conjg(sfvecll(i1,j1))
           else
              sfvecrr(i1,j1)=cmat(ic,k)
              sfvecrr(j1,i1)=conjg(sfvecrr(i1,j1))
           end if
        end do
     end do
     do i=1,nchan/2
        sfvecll(i,i)=0
        sfvecrr(i,i)=0
     enddo
     stmp=sfvecll
     call CHEEV( JOBZ, UPLO, nchan/2, sfvecll, LDA, W, WORK, LWORK, RWORK, INFO )
     if (info .ne. 0) then
        write(*,*) 'cheev ll info=',info,n
        write(*,*) stmp
        stop
     endif

     write(200,*) w
     ovecll=sfvecll(:,nchan/2)/(sfvecll(1,nchan/2))
     ovecll=sqrt(w(nchan/2))*ovecll/sqrt(sum(abs(ovecll**2)))
     call CHEEV( JOBZ, UPLO, nchan/2, sfvecrr, LDA, W, WORK, LWORK, RWORK, INFO )
     if (info .ne. 0) write(*,*) 'cheev rr info=',info,n
     write(200,*) w
     ovecrr=sfvecrr(:,nchan/2)/(sfvecrr(1,nchan/2))
     ovecrr=sqrt(w(nchan/2))*ovecrr/sqrt(sum(abs(ovecrr**2)))

!     write(*,*) sum(abs(ovec1(ic,:)**2))/w(nchan)
     if (n .eq. 1) then
!        ctmp=sum(ovecll*conjg(ovecrr))
!	ovecrr=ovecrr*ctmp/abs(ctmp)
	cphase=ovecrr+overll
	cphase=cphase/abs(cphase)
        ovecrr=abs(ovecrr)*(cphase)
        ovecll=abs(ovecll)*(cphase)
     end if
!     ovec1(ic,:28)=ovecll(:28)
!     ovec1(ic,59:60)=ovecll(29:30)
!     ovec1(ic,29:58)=ovecrr

     ovec1(ic,:nchan/2)=ovecll(:nchan/2)
     ovec1(ic,nchan/2+1:nchan)=ovecrr
     k=0
     do i=1,nchan
        do j=i,nchan
           k=k+1
           cmat(ic,k)=ovec1(ic,i)*conjg(ovec1(ic,j))
        end do
     end do
  end do
  do j=1,nchan
     do i=1,n
        write(100,*) real(ovec1(i,j)),aimag(ovec1(i,j))
     end do
  end do

end subroutine pca

subroutine cutrm(a,n,ncorr)
complex a(n,ncorr)
complex cbuf(n+1)

return
end
