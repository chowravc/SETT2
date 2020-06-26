program 2pCor
!Program: to calculate the correlation function given a grid
    character(100) :: buffer
    real, allocatable, dimension(:,:) :: x
    real(8), dimension(10) :: xtest
    complex, dimension(100*100) :: defect
    real :: aveDNN=0,temp=0,aveD=0
    real , dimension(4):: ll
    real(8), allocatable, dimension(:) :: defectD
    integer :: time,row, col,indx=1, defectN=0,N
    character(100) :: fileNames


    call getarg(1,buffer)
    read(buffer,"(A100)"), fileNames

    call getarg(2,buffer)
    read(buffer,*), N

    call getarg(3,buffer)
    read(buffer,*), time
   ! write(*,*) fileNames
    allocate(x(N,N))
    open(unit=99, file=fileNames,status='old',action='read')
    do row = 1, N
        read(99,*) (x(row,col), col=1,N)
    enddo

    !define correlation function



    function 2pCor(r,grid,N)
        integer :: r,i,j,N
        real :: 2pCor
        do i = 1,N,r
            do j = 1,N,r
                do i

 
