program randTest
implicit none

character(100) :: buffer
real(8),parameter :: PI = 4*atan(1.0_8), delTime=0.05
integer, dimension(13) :: seed
integer :: seedN,i
real :: num


!read in arguments (g,beta,mu,N,endT)
call getarg(1,buffer)
read(buffer,*), seedN

seed = (/(i, i=seedN,seedN+14 )/)
!write(*,*) grid(N,N)
call random_seed(put=seed)
do i=1,5
    call random_number(num)
    write(*,*) num
enddo

endprogram randTest
