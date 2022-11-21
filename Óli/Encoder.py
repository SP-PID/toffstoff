
import board
import digitalio

encA = digitalio.DigitalInOut(board.D16)
encA.direction = digitalio.Direction.INPUT
encA.pull = digitalio.Pull.DOWN

encB = digitalio.DigitalInOut(board.D17)
encB.direction = digitalio.Direction.INPUT
encB.pull = digitalio.Pull.DOWN

direction = ''

i = 0
iold = 0
while True:
    if encA.value == True:
        if encB.value == True:
            direction = 'Forward'
        else:
            direction = 'Backwards'
        while encA.value == True:
            d = 1
        iold = i
        if direction == 'Forward':
            i += 1
        else:
            i -= 1
    if i != iold:
        print(((i/7)/100)*14.337)
        iold = i
