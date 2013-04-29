#!/usr/bin/python

import time
import datetime
import urllib2
import threading
import traceback
import RPi.GPIO as GPIO

UPDATE_FREQ = 3 # 3secs

LCD_RS = 7
LCD_E  = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18

LCD_WIDTH = 20 #4x20 LCD
LCD_CHR = True
LCD_CMD = False

LCD_LINE_1 = 0x80 #LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 #LCD RAM address for the 2nd line
LCD_LINE_3 = 0x94 #LCD RAM address for the 3rd line
LCD_LINE_4 = 0xD4 #LCD RAM address for the 4th line

E_PULSE = 0.00005
E_DELAY = 0.00005

LED1 = 4
LED2 = 17
LED3 = 27
LED4 = 22
WARNING_LIGHT = 10

class InfoWrapper:
  body = ""
  ST1 = ""
  ST2 = ""
  WARNING_LIGHT = ""
  LINE1 = ""
  LINE2 = ""
  LINE3 = ""
  LINE4 = ""

  def toString(self):
    return self.body

def main():
  print("starting...")
  info = InfoWrapper()
  lcd_and_led_init()
  while True:
    updateInfo(info, 0)
    printInfo(info)
    time.sleep(UPDATE_FREQ)

def printInfo(info):
  if info.ST1 == "1":
    GPIO.output(LED1, True) #OK, GREEN LED ON
    GPIO.output(LED2, False) #OK, RED LED OFF 
  else:
    GPIO.output(LED1, False) #FAIL, GREEN LED OFF
    GPIO.output(LED2, True) #FAIL, RED LED ON

  if info.ST2 == "1":
    GPIO.output(LED3, True) #OK, GREEN LED ON
    GPIO.output(LED4, False) #OK, RED LED OFF
  else:
    GPIO.output(LED3, False) #FAIL, GREEN LED OFF
    GPIO.output(LED4, True) #FAIL, RED LED ON

  if info.WARNING_LIGHT == "1":
    GPIO.output(WARNING_LIGHT, False) #OK, WARNING LIGHT OFF
  else:
    GPIO.output(WARNING_LIGHT, True) #FAIL, WARNING LIGHT ON
    
  lcd_byte(LCD_LINE_1,LCD_CMD)
  lcd_string(info.LINE1,2)
  
  lcd_byte(LCD_LINE_2,LCD_CMD)
  lcd_string(info.LINE2,2)
  
  lcd_byte(LCD_LINE_3,LCD_CMD)
  lcd_string(info.LINE3,2)
  
  lcd_byte(LCD_LINE_4,LCD_CMD)
  lcd_string(info.LINE4,2)  

def updateInfo(info,retryCnt):
  try:
    print(datetime.datetime.now().strftime("%Y %m %d %H:%M:%S.%f") + " - updateInfo(): updating (" + str(retryCnt+1) + ". attempt)")
    response = urllib2.urlopen('http://217.65.100.117/webapp/mediator?operation=get',timeout=5)
    body = response.read()
    info.body = body
    values = body.strip().split(';')
    info.ST1 = values[0]
    info.ST2 = values[1]
    info.WARNING_LIGHT = values[2] 
    info.LINE1 = values[3]
    info.LINE2 = values[4]
    info.LINE3 = values[5]
    info.LINE4 = values[6]
    print(datetime.datetime.now().strftime("%Y %m %d %H:%M:%S.%f") + " - updateInfo(): updated")
  except:
    print(datetime.datetime.now().strftime("%Y %m %d %H:%M:%S.%f") + " - updateInfo(): error occured")
    print(traceback.format_exc())
    if retryCnt < 2:
      time.sleep(2)
      updateInfo(info, retryCnt+1)    

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
