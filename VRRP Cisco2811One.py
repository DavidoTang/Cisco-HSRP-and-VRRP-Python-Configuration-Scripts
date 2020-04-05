#David Tang 2/18/20
#Switches HSRP to VRRP configuration for Cisco 2811 Router
from Exscript.util.interact import read_login
from Exscript.protocols import SSH2

vlans = ["5","10","20","30","40","50","60","70","80"]

priority1 = '110'
priority2 = '200'

account = read_login()
conn = SSH2()
conn.connect('10.21.3.4')
conn.login(account)
conn.execute('terminal length 0')
conn.execute('show running-config')
print(conn.response)

conn.execute('configure terminal')
for i in vlans:
    command = 'interface fa0/1.' + i
    conn.execute(command)
    print(conn.response)

    command = 'no standby 1'
    conn.execute(command)
    command = 'no standby 2'
    conn.execute(command)

    command = 'vrrp ' + i + ' priority ' + priority1
    conn.execute(command)
    command = 'vrrp ' + str(int(i)+1) + ' priority ' + priority2
    conn.execute(command)


    #VLAN 5 doesn't follow convention
    if(i == "5"):
        command = 'vrrp ' + i + ' ip 192.168.0.3'
        conn.execute(command)
        command = 'vrrp ' + str(int(i)+1) + ' ip 192.168.0.5'
        conn.execute(command)        
    #VLAN 10 doesn't follow convention
    elif(i == "10"):
        command = 'vrrp ' + i + ' ip 192.168.0.131'
        conn.execute(command)
        command = 'vrrp ' + str(int(i)+1) + ' ip 192.168.0.133'
        conn.execute(command)
    else:
        command = 'vrrp ' + i + ' ip 192.168.' + i[0:1] + ".3"
        conn.execute(command)
        command = 'vrrp ' + str(int(i)+1) + ' ip 192.168.' + i[0:1] + ".5"
        conn.execute(command)

conn.execute('do show running-config')
print(conn.response) 
