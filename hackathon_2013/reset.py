#!/usr/bin/python

import time
import RPi.GPIO as GPIO

LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18

LCD_WIDTH = 20
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 # LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 # LCD RAM address for the 4th line

E_PULSE = 0.00005
E_DELAY = 0.00005

LED1 = 4
LED2 = 17
LED3 = 27
LED4 = 22
WARNING_LIGHT = 10

def main():
  lcd_and_led_init()
  while True:
    GPIO.output(LED1, False)
    GPIO.output(LED2, False)
    GPIO.output(LED3, False)
    GPIO.output(LED4, False)
    GPIO.output(WARNING_LIGHT, False)
    lcd_byte(LCD_LINE_1, LCD_CMD)
    lcd_string("a",2)
    lcd_byte(LCD_LINE_2, LCD_CMD)
    lcd_string("b",2)
    lcd_byte(LCD_LINE_3, LCD_CMD)
    lcd_string("c",2)
    lcd_byte(LCD_LINE_4, LCD_CMD)
    lcd_string("d",2)

def lcd_and_led_init():
  GPIO.setmode(GPIO.BCM) 
  GPIO.setup(LCD_E, GPIO.OUT)
  GPIO.setup(LCD_RS, GPIO.OUT)
  GPIO.setup(LCD_D4, GPIO.OUT)
  GPIO.setup(LCD_D5, GPIO.OUT)
  GPIO.setup(LCD_D6, GPIO.OUT)
  GPIO.setup(LCD_D7, GPIO.OUT)
  lcd_byte(0x33,LCD_CMD)
  lcd_byte(0x32,LCD_CMD)
  lcd_byte(0x28,LCD_CMD)
  lcd_byte(0x0C,LCD_CMD)
  lcd_byte(0x06,LCD_CMD)
  lcd_byte(0x01,LCD_CMD)
  GPIO.setup(LED1, GPIO.OUT)
  GPIO.setup(LED2, GPIO.OUT)
  GPIO.setup(LED3, GPIO.OUT)
  GPIO.setup(LED4, GPIO.OUT)
  GPIO.setup(WARNING_LIGHT, GPIO.OUT)

def lcd_string(message,style):
  # Send string to display
  # style=1 Left justified
  # style=2 Centred
  # style=3 Right justified

  if style==1:
    message = message.ljust(LCD_WIDTH," ")
  elif style==2:
    message = message.center(LCD_WIDTH," ")
  elif style==3:
    message = message.rjust(LCD_WIDTH," ")

  for i in range(LCD_WIDTH):
    lcd_byte(ord(message[i]),LCD_CHR)

def lcd_byte(bits, mode):
  # Send byte to data pins
  # bits = data
  # mode = True  for character
  #        False for command

  GPIO.output(LCD_RS, mode) # RS

  # High bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x10==0x10:
    GPIO.output(LCD_D4, True)
  if bits&0x20==0x20:
    GPIO.output(LCD_D5, True)
  if bits&0x40==0x40:
    GPIO.output(LCD_D6, True)
  if bits&0x80==0x80:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)    
  GPIO.output(LCD_E, True)  
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)  
  time.sleep(E_DELAY)      

  # Low bits
  GPIO.output(LCD_D4, False)
  GPIO.output(LCD_D5, False)
  GPIO.output(LCD_D6, False)
  GPIO.output(LCD_D7, False)
  if bits&0x01==0x01:
    GPIO.output(LCD_D4, True)
  if bits&0x02==0x02:
    GPIO.output(LCD_D5, True)
  if bits&0x04==0x04:
    GPIO.output(LCD_D6, True)
  if bits&0x08==0x08:
    GPIO.output(LCD_D7, True)

  # Toggle 'Enable' pin
  time.sleep(E_DELAY)
  GPIO.output(LCD_E, True)
  time.sleep(E_PULSE)
  GPIO.output(LCD_E, False)
  time.sleep(E_DELAY)

if __name__ == '__main__':
  main()
