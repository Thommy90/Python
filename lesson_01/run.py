class A:
    def foo(self):
        print ("I am from A")

class B(A):
    def foo(self):
        super(C, self).foo()

class C(A):
    def foo(self):
        print ("I am from C")

class D(B, C):
    def foo(self):
        super().foo()

print(D.mro())
D().foo()