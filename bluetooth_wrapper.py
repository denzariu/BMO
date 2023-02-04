import os, sys, time, pexpect

def findaddress():
  address=''
  p = pexpect.spawn('hcitool scan', encoding='utf-8')
  p.logfile_read = sys.stdout
  mylist = ['D4\:F0\:57\:[0-9A-F].[:][0-9A-F].[:][0-9A-F].',pexpect.EOF]
  p.expect(mylist)
  address=p.after
  if address==pexpect.EOF:
    return ''
  else:
    return address

def setbt(address):
  response=''
  p = pexpect.spawn('bluetoothctl', encoding='utf-8')
  p.logfile_read = sys.stdout
  p.expect('#')
  p.sendline("remove "+address)
  p.expect("#")
  p.sendline("scan on")

  mylist = ["Discovery started","Failed to start discovery","Device "+address+" not available","Failed to connect","Connection successful"]
  while response != "Connection successful":
    p.expect(mylist)
    response=p.after
    p.sendline("connect "+address)
    time.sleep(1)
  p.sendline("quit")
  p.close()
  #time.sleep(1)
  return


address='' 
while address=='':
  address=findaddress()
  time.sleep(1)
  
print (address," found")
setbt(address)
