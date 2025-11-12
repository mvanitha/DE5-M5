class Calculator:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def sum(self):
        return self.a + self.b
    def diff(self):
        return self.a - self.b
    def multiply(self):
        return self.a * self.b  
    def divide(self):
        return self.a / self.b    
    

myCalc = Calculator(2,4)
print(myCalc.sum())

