import RPi.GPIO as GPIO
# import time_tracker

GPIO.setmode(GPIO.BCM)


class PotOhm:
    def __init__(self, pinA, pinB):
        self.pin_a = pinA
        self.pin_b = pinB

    def discharge(self):
        GPIO.setup(self.pin_a, GPIO.IN)
        GPIO.setup(self.pin_b, GPIO.OUT)
        GPIO.output(self.pin_b, False)
        # time.sleep(0.004)

    def charge_time(self):
        GPIO.setup(self.pin_b, GPIO.IN)
        GPIO.setup(self.pin_a, GPIO.OUT)
        count = 0
        GPIO.output(self.pin_a, True)
        while not GPIO.input(self.b_pin):
            count = count + 1
        return count

    def analog_read(self):
        self.discharge()
        return self.charge_time()

'''
if __name__ == "__main__":
    pA = input("PortA: ")
    pB = input("PortB: ")
    Temp_Pot = PotOhm(pA,pB)
    print(Temp_Pot.analog_read())
    # time.sleep(1)
