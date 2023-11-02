def foo(a, b, /, c, *d, e, f, **g):
    return True


foo(1,2,3,4,5,6,7,e=8,f=9,x=10,y=11,z=12,k=13)
foo(1,2,3,4,5,6,7,x=8,k=9,f=10,y=11,z=12,e=13)
