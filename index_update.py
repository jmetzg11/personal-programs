import openpyxl
import os
"""This program will bring up prompts where I can update my index price
   that are located on an excel file

   Couldn't make a convenient loop because the bank has a fixed order and
   some indices I convert currencies for readability reasons
"""
os.chdir('C:\\Users\\jesse\\Desktop')

wb=openpyxl.load_workbook('expensences.xlsx')
sheet=wb['total']

print('enter TECH')
TECH=input()
sheet['C8']='=I2*'+TECH

print('enter TMOS')
TMOS=input()
sheet['C9']='='+TMOS

print('enter FXDE')
FXDE=input()
sheet['C10']='='+FXDE

print('enter FXKZ')
FXKZ=input()
sheet['C11']='='+FXKZ

print('enter FXUS')
FXUS=input()
sheet['C12']='='+FXUS

print('enter FXRW')
FXRW=input()
sheet['C13']='='+FXRW

print('enter FXCN')
FXCN=input()
sheet['C14']='='+FXCN

print('enter TIPO')
TIPO=input()
sheet['C15']='=I2*'+TIPO

print('enter TSPX')
TSPX=input()
sheet['C16']='=I2*'+TSPX

print('enter FXWO')
FXWO=input()
sheet['C17']='='+FXWO

print('enter AKNX')
AKNX=input()
sheet['C18']='=I2*'+AKNX

print('enter VTBE')
VTBE=input()
sheet['C19']='=I2*'+VTBE

print('enter exchange rate')
rate=input()
sheet['I2']='='+rate

# Saving the updates
wb.save('expensences.xlsx')
