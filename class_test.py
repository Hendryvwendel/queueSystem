class Microwave:
    
    def __init__(self, brand, power) -> None:
        self.on = False
        self.brand = brand
        self.power = power
       

    def turn_on(self) -> None:
        if self.on == False:
            self.on = True
            print(f'{self.brand} is on')
        else:
            print(f'{self.brand} is already on')

    def turn_off(self) -> None:
        if self.on == True:
            self.on = False
            print(f'{self.brand} is off')
        else:
            print(f'{self.brand} is already off')

    def run(self, time) -> None:
        self.time = time
        if self.on == True:
            print(f'{self.brand} is running for {self.time} seconds')
        else:
            print(f'{self.brand} is off, turn it on first')


samsung = Microwave('Samsung', 1000)
aeg = Microwave('AEG', 1200)

samsung.turn_on()
samsung.run(30)
samsung.turn_off()

aeg.turn_on()
aeg.run(40)
aeg.turn_off()
    

        