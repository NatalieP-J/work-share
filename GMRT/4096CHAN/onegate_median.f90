! optimized version which takes two pulsar gates
! and computes variance
!
integer ongate
character*200 fn,argv
icount=iargc()
write(*,*) 'iargc=',icount
if (icount .eq. 0) then
   write(*,*) 'usage: plag infile nt nchan nself n ngate ongate'
   stop
endif
n=4096
nt=600
nchan=30
nself=1
ngate=16
fn='corrfilt.dat'
do i=1,icount
   call getarg(i,argv)
   if (i .eq. 1) fn=argv
   if (i .eq. 2) read(argv,*) nt
   if (i .eq. 3) read(argv,*) nchan
   if (i .eq. 4) read(argv,*) nself
   if (i .eq. 5) read(argv,*) n
   if (i .eq. 6) read(argv,*) ngate
   if (i .eq. 7) read(argv,*) ongate
   ! set nself=1 if autocorrelations are in the file, otherwise set to -1
enddo
write(*,*) 'infile=',fn,' nt=',nt
nout=n
write(*,*) 'nself=',nself
write(*,*) 'nchan=',nchan
write(*,*) 'ngate=',ngate
write(*,*) 'ongate=',ongate
call plag(n,nt,nout,nchan,nself,fn,ngate,ongate)
end

!integer, parameter :: n=4096,nt=250,nout=n,nchan=30,ncorr=nchan*(nchan+1)/2,nfit=4
subroutine plag(n,nt,nout,nchan,nself,fnin,ngate,ongate)
  integer, parameter :: nred=32
  integer ongate
  real, dimension(2*nout,nt,ngate) :: rpow
  real, dimension(2*nout/nred,ngate) :: rpows
  real, dimension(2*nout) :: rc
  real, dimension(nout,nt,ngate) :: rpowr
  real, dimension(nout,nt,ngate) :: rpowt
  real, dimension(nout,ngate) :: rpowrs
  real, dimension(nout,ngate) :: rpowts
  complex, dimension(nout,nt,ngate) :: cpowr
  complex, dimension(nout,ngate) :: cpowrs
  complex, dimension(n+1) :: cbuf
  real, dimension(2*n) :: rbuf
  !equivalence(cbuf,rbuf)
  integer*1, dimension(2*nout,nt,ngate) :: ipow
  integer*1, dimension(2*nout/nred,ngate) :: ipows
  integer*1, dimension(nout,nt,ngate) :: ipowr
  integer*1, dimension(nout,ngate) :: ipowrs
  complex, dimension(n) :: oneshot
  complex, dimension(n+1) :: cfftarray
  complex, dimension(ngate,n,nchan*(nchan+nself)/2,4) :: diffgates
  complex, dimension(4,n,nchan*(nchan+nself)/2) :: onecum, bgcum,allgate
  complex, dimension(n/2,nchan*(nchan+nself)/2) :: pulsargate,ctmpmedian
  real, dimension(n,nchan*(nchan+nself)/2) :: var
  real, dimension(n) :: rpow1
  character*200 fn,fnin
  integer igatecount(nt,ngate,n)
  complex cmedian
  external cmedian


  ncorr=nchan*(nchan+nself)/2
  if (nself>0) nself=0
  k=0
  open(10,file=fnin,status='old',form='binary',access='direct',recl=8*n)
  open(20,file='onegate.float',form='binary')
  open(30,file='offgate.float',form='binary')
  open(40,file='allgate.float',form='binary')
  open(50,file='var.float',form='binary')
  do it=1,nt,4
     write(*,*) 'i=',it
     onecum=0
     allgate=0
     bgcum=0
     var=0
     do i=it,it+3
        icount=0
        do igate=1,ngate
           do k=1,ncorr
              read(10,rec=(i-1)*ncorr*ngate+(igate-1)*ncorr+k) oneshot
              allgate(i-it+1,:,k)=allgate(i-it+1,:,k)+oneshot
              if ( mod(ngate+igate-ongate+1,ngate) .le. 2 ) then
                 onecum(i-it+1,:,k)=onecum(i-it+1,:,k)+oneshot/3
              else
                 if (k .eq. 1) icount=icount+1
                 diffgates(icount,:,k,i-it+1)=oneshot
              endif
           enddo
        enddo
        do igate=1,ngate-4,2
           var=var+abs(diffgates(igate,:,:,i-it+1)-diffgates(igate+1,:,:,i-it+1))**2
        enddo
        do k=1,ncorr
           do in=1,n
!              bgcum(i-it+1,in,k)=bgcum(i-it+1,in,k)+cmedian(diffgates(1,in,k,i-it+1),ngate-3)
              bgcum(i-it+1,in,k)=bgcum(i-it+1,in,k)+sum(diffgates(:ngate-3,in,k,i-it+1))/(ngate-3)
           enddo
        end do
     enddo
     onecum=onecum-bgcum
     do k=1,ncorr
       do in=1,n/2
         ctmpmedian(in,k)=cmedian(onecum(1,2*in-1,k),8)
       enddo
     enddo
     pulsargate=ctmpmedian
     write(20) ctmpmedian
     pulsargate=conjg(pulsargate)/abs(pulsargate)
     do k=1,ncorr
       do in=1,n/2
         ctmpmedian(in,k)=cmedian(bgcum(1,2*in-1,k),8)
       enddo
     enddo
     ctmpmedian=ctmpmedian*pulsargate
     write(30) ctmpmedian
    do k=1,ncorr
       do in=1,n/2
         ctmpmedian(in,k)=cmedian(allgate(1,2*in-1,k),8)
       enddo
     enddo
     ctmpmedian=ctmpmedian*pulsargate
     write(40) ctmpmedian
     var=var+cshift(var,1,dim=1)
     write(50) var(::2,:)
  end do
end subroutine plag
complex function cmedian(c,n)
  complex c(n)
  call rmedian(cmedian,c,n,2)
end function cmedian

subroutine rmedian(a,b,nt,n)
real, dimension(n,nt) :: b
real, dimension(n) :: a
real, dimension(nt) :: t
integer, dimension(nt) :: iorder

!  a=sum(b,2)!  return
!!$omp parallel do default(shared) private(j,i,t,iorder)
  do in=1,n
     j=0
     do i=1,nt
        if (b(in,i) .ne. 0) then
           j=j+1
           t(j)=b(in,i)
        endif
     end do
     if (j .eq. 0) then
        a(in)=0
        cycle
     end if
!     t=b(in,:)
     call quick_sort(t,iorder,j)
     if (mod(j,2) .eq. 0) then
        a(in)=(t(j/2)+t(j/2+1))/2
     else
        a(in)=t((j+1)/2)
     endif
  end do
end subroutine rmedian


