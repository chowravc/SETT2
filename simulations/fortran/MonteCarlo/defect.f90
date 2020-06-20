program defect
implicit none

character(100) :: buffer
integer :: N = 200, endT=1001
real(8) :: beta,mu,measuredT,zeroE,meanK,totalK,meanDelPhi
integer, dimension(100) :: tPoints
integer, allocatable, dimension(:) :: logTPoints
real(8), allocatable, dimension(:,:) :: grid,dgrid,oldGrid
real(8) :: x,g,windingN
real(8),parameter :: PI = 4*atan(1.0_8)
character(12) :: fileNames
character(20) :: dfileNames

real(8) :: t1=1.2,t2=1.0,dT
integer :: i,j,t,timePrint=1,tt

!read in arguments (g,beta,mu,N,endT)
call getarg(1,buffer)
read(buffer,*), g

call getarg(2,buffer)
read(buffer,*),beta

call getarg(3,buffer)
read(buffer,*),mu

call getarg(4,buffer)
read(buffer,*),N

call getarg(5,buffer)
read(buffer,*),endT

do t=1,100
    dT = (LOG10(REAL(endT))/100)
    tPoints(t) =  INT(10**(t*dT))
enddo
logTPoints= tPoints(unique(tPoints))
!write(*,*) logTPoints
!calculate zero temperature energy
zeroE = -g*4.0

!Initial Random Grid
!write(*,*) 'initialize grid'
allocate(grid(N,N))
allocate(oldgrid(N,N))
!write(*,*) grid(N,N)
call random_seed()
do i=1,N
    do j=1,N
!        write(*,*) i,j
        call random_number(x)
        grid(i,j) = x*2*PI-PI
    end do
enddo
!open temperature V time file
open(61,file='tVT.dat',status = 'unknown', position='append')
!initialize defect grid
allocate(dgrid(N,N))
dgrid=0
!write(*,*) 'metropolis algo. commence'
!Preform the metropolis algorithm with XY hamiltonian
do t=1,endT
    !write(*,*) 'time', t
    oldGrid = grid
    call metro(grid,beta,N)
    
    totalK = SUM((acos(cos(grid-oldGrid)))**2)
    meanK = totalK/N**2
    meanDelPhi = sqrt(totalK)/N*2
    write(fileNames,'(A3,I0.3,A4)') 'out', t,'.dat'
    write(dfileNames,'(A6,I0.3,A4)') 'defect', t,'.dat'
        !
    if (logSpace(t) .eq. 1) then
        !print *, trim(fileNames)

        open(1,file=fileNames)
        open(3,file=dfileNames)
        ! calculate defects and average energy, and write grid to file
        measuredT = 0.

        do i=1,N
            do j=1,N
            write(1,'(F10.5)',advance="no") grid(i,j)
            measuredT = (hamXY(i,j,grid(i,j),g,mu))/N/N+measuredT
            windingN=(windN(grid(modulo(i-2,N)+1,j)-grid(i,j)))+&
                &(windN(grid(modulo(i-2,N)+1,modulo(j-2,N)+1)-grid(modulo(i-2,N)+1,j)))+&
                &(windN(grid(i,modulo(j-2,N)+1)-grid(modulo(i-2,N)+1,modulo(j-2,N)+1)))+&
                &(windN(grid(i,j)-grid(i,modulo(j-2,N)+1)))
            if (windingN .ge. 1) then
                dgrid(i,j) =1
            else if (-1*windingN .ge. 1) then
                dgrid(i,j)=-1
            else
                dgrid(i,j)=0
            endif
            write(3,'(F10.5)',advance="no") dgrid(i,j)
            enddo
            write(1,*)
            write(3,*)
        enddo
        measuredT = (measuredT-zeroE)
        write(61,'(I10,A, F10.5)') t,',', measuredT
        write(*,*) t,' ', measuredT,meanDelPhi,meanK/2,1/beta


        close(1)
        close(3)
    endif
end do
close(61)

deallocate(grid)
contains
    function windN(angle)
        real(8) :: angle, windN
        windN = (angle-asin(sin(angle)) / (2*PI) )
        end function windN
    function logSpace(t)
        integer :: t, logSpace
        if (t .eq. logTPoints(timePrint)) then
            logSpace = 1
            timePrint = timePrint +1
        else
            logSpace = 0
        endif
        !write(*,*) 'lTP', logTPoints(timePrint)

            end function logSpace

    function hamXY(i,j,theta,g,mu)
        integer :: i,j,ii,jj
        real(8):: theta
        real(8) :: g,hamXY,mu
        real(8), dimension(3) :: x,y
        !write(*,*) 'hamxy', i,j
        x =(/ grid(modulo(i-2,N)+1,j),theta,grid(modulo(i,N)+1,j)/)
        y =(/ grid(i,modulo(j-2,N)+1),theta,grid(i,modulo(j,N)+1)/)
        hamXY = -g*(cos(x(2)-x(1))+cos(x(2)-x(3))+cos(y(2)-y(1))+cos(y(2)-y(3)))-mu*cos( (theta-45/2/PI) )
        end function hamXY
        
        subroutine normAngle(i,j,N)
            integer:: i,j,n
                grid(i,j) = asin(sin(grid(i,j)))
                end subroutine normAngle
        subroutine metro(state,beta,N)
        real(8) :: theta, thetaP,x,delE,E1,E2,beta,flucE,u
        integer :: N,ii,jj,i,j
        real(8), dimension(N,N) :: state
        do ii=1,N
            do jj=1,N
                call random_number(x)
                call random_number(u)

                i = 1+floor(N*u)
                call random_number(u)
                j = 1+floor(N*u)

                theta = state(i,j)
                thetaP = (x*2*PI-PI)
               ! write(*,*) 'metro',i,j
                E1 = hamXY(i,j,theta,g,mu)
                E2 = hamXY(i,j,thetaP,g,mu)
                delE = E2-E1
                call random_number(flucE) 
                if (delE < 0) then
                    state(i,j) = thetaP
                else if (flucE .le. exp(-delE*beta)) then
                    state(i,j) = thetaP
                end if
            end do
        end do
    end subroutine metro
            

    function dtrack(dgrid,grid)
        real(8), dimension(N,N) :: dgrid
        real(8), dimension(3,3) :: grid
        real(8)                 :: angle=0
        integer                 :: dtrack,i,j
        do i=1,3
            !angle=angle+grid(i,j)-grid(2,2)/9., j=1,3)
            !write(*,*) (grid(i,j), j=1,3)
        enddo
        if (angle .ge. 2*PI) then
            dtrack=1

        else  
            dtrack=0
        endif

    endfunction dtrack

    function angleDist(theta1,theta2)
        real(8) :: d1,d2,angleDist,theta1,theta2
        angleDist = acos(cos(theta1-theta2))
        end function angleDist


function remove_dups(input)
  integer :: input(100)       ! The input
  integer :: remove_dups(size(input))  ! The output
  integer :: k                   ! The number of unique elements
  integer :: i, j
 
  k = 1
  remove_dups(1) = input(1)
  outer: do i=2,size(input)
     do j=1,k
        if (remove_dups(j) == input(i)) then
           ! Found a match so start looking again
           cycle outer
        end if
     end do
     ! No match found so add it to the output
     k = k + 1
     remove_dups(k) = input(i)
  end do outer
  end function remove_dups
    function unique(input)
     !   find "indices", the list of unique numbers in "list"
     integer( kind = 4 ) :: kx, input(100)
     integer( kind = 4 ),allocatable :: unique(:)
     logical :: mask(100)
     mask(1)=.true.
     do kx=100,2,-1
       mask(kx)= .not.(any(input(:kx-1)==input(kx)))
     end do
     unique=pack([(kx,kx=1,100)],mask)
    end function unique
end program defect
