

def RectCalc(width, length):
    area = width * length
    perimeter = 2*width + 2*length
    # print(f'{area}')
    return area, perimeter


l1 = 3
w1 = 5
area1, per1 = RectCalc(l1,w1)
print(f'area and perimeter of rectangle1 = {area1} and {per1}')

l2 = 6
w2 = 4
area2, per2 = RectCalc(l2,w2)
print(f'area and perimeter of rectangle2 = {area2} and {per2}')




