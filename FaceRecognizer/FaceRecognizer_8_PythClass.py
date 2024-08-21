
# 
class Rectangle:
    
    #constructor is "__init__ method"     
    def __init__ (self, colorA, widthA, lengthA):
        # note that self is 'name_of_object' 
        self.width  = widthA        
        self.length = lengthA
        self.color  = colorA
    
    def area(self):
        self.area = self.width * self.length
        return self.area
    
    
color1 = 'red'
wide1 = 3
len1 = 4
    
rect_Object = Rectangle(color1, wide1, len1)

print('Rectangle created is', rect_Object.color, ', having width of', rect_Object.width , 'and length of', rect_Object.length)

# area does NOT exist prior to .area() method call
# print(f'Rectangle Area internal data before calling method is {rect_Object.area} ')
print(f'Rectangle Area is {rect_Object.area()} ')
print(f'Rectangle Area internal data is {rect_Object.area} ')
