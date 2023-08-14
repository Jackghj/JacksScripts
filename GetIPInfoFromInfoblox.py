## Script to get all infomations about a list of IP's. (Used to find where IP's where located and who i should contact about getting some vulnerabities fixed)
import requests
import urllib3
import os
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
IP = ""

def infobloxdata():
        global IP
        print (IP)

        headers = {
        }

        json_data = [
                {
                'method': 'GET',
                'object': 'ipv4address',
                'data': {
                        'ip_address': (IP),
                },
        'args': {
            '_return_fields': 'network,comment',
        },
        'assign_state': {
            'my_net': 'network',
        },
        'enable_substitution': True,
        'discard': True,
    },
    {
        'method': 'GET',
        'object': 'network',
        'enable_substitution': True,
        'data': {
            'network': '##STATE:my_net:##',
        },
        'args': {
            '_return_fields+': 'extattrs,comment',
        },
        'discard': False,
    },
    {
        'method': 'STATE:DISPLAY',
    },
        ]

        response = requests.post('https://infoblox.company.dk/wapi/v2.11/request', headers=headers, json=json_data, verify=False, auth=('username', 'Password'))



        #Krydsfelt output
        outpututf = str(response.content, 'utf-8')
        print (outpututf)
        #print (outpututf)
        #print (outpututf)
        try:
                outputkryds2 = str(outpututf.split('Krydsfelt"' ,1)[1])
                outputkryds3 = str(outputkryds2.split('"value": ', 1)[1])
                outputkryds4 = str(outputkryds3.split('"', 1)[1])
                outputkryds5 = str(outputkryds4.split(']', 1)[0])
                outputkryds6 = str(outputkryds5.split('"', 1)[0])
                outputkryds7 = str(outputkryds5.split('"', 1)[1])
                outputkryds8 = str(outputkryds7.split('"', 1)[1])
                #print (outputkryds6)
                if outputkryds8.find("network") != -1:
                        print("Krydsfelt: " + outputkryds6)
                        outputkryds9 = str(outputkryds6)
                        outputkryds10 = str(outputkryds9.split(',', 1))
                        outputkryds11 = outputkryds10.replace("\\", '')
                        outputkryds12 = outputkryds11.replace("'", '')
                        outputkryds13 = outputkryds12.replace('n', '')
                        outputkryds14 = outputkryds13.replace('"', '')
                        outputkryds15 = outputkryds14.replace('[', '')
                        outputkryds16 = outputkryds15.replace(']', '')
                        outputkryds17 = outputkryds16.replace(' ', '')
                else:
                        print("Krydsfelte: " + outputkryds6 + ", " + outputkryds8)
                        outputkryds9 = (outputkryds6 + ", " + outputkryds8)
                        outputkryds10 = str(outputkryds9.split(',', 1))
                        outputkryds11 = outputkryds10.replace('\\', '')
                        outputkryds12 = outputkryds11.replace("'", '')
                        outputkryds13 = outputkryds12.replace('n', '')
                        outputkryds14 = outputkryds13.replace('"', '')
                        outputkryds15 = outputkryds14.replace('[', '')
                        outputkryds16 = outputkryds15.replace(']', '')
                        outputkryds17 = outputkryds16.replace(' ', '')
        #Krydsfelt
        except IndexError:
                print ("Intet krydsfelt??")
                outputkryds17 = ("N/A")
        #Network type
        try:
                outputtype2 = (outpututf.split('"inheritance_source": {' ,1)[0])
                outputtype3 = str(outputtype2.split('"value":', 1)[1])
                outputtype4 = str(outputtype3.split('"value":', 1)[1])
                outputtype5 = str(outputtype4.split('"', 1)[1])
                outputtype6 = str(outputtype5.split('"', 1)[0])
                print ("Network type: " + outputtype6)
                outputtypeE = outputtype6
        except IndexError:
                try:
                        outputtypeA = str(outpututf.split('Network Type', 1)[1])
                        outputtypeB = str(outputtypeA.split('value', 1)[1])
                        outputtypeC = str(outputtypeB.split('"', 1)[1])
                        outputtypeD = str(outputtypeC.split('"', 1)[1])
                        outputtypeE = str(outputtypeD.split('"', 1)[0])
                        print ("Network type: " + outputtypeE)
                except IndexError:
                        print ("Ingen network type")
                        outputtypeE = ("N/A")
        #SiteDONE
        try:
                outputsite2 = (outpututf.split('"Site"' ,1)[1])
                outputsite3 = (outputsite2.split('"value": "',1)[1])
                outputsite4 = (outputsite3.split('"', 1))
                outputsite5 = (outputsite4[0])
                print ("Lokation: " + outputsite5)
        except IndexError:
                outputsite5 = ("N/A")
        #VlanDONE
        try:
                outputvlan = (outpututf.split('"VLAN Nummer": {\n                    "value": ', 1)[1])
                outputvlan2 = outputvlan.split('\n',1)
                outputvlan3 = outputvlan2[0]
                print ("vlan: " + outputvlan3)
        except IndexError:
                print ("Intet vlan??")
                outputvlan3 = ("N/A")
        #VRF
        #print (outpututf)
        try:
                outputvrf2 = str(outpututf.split('VRF"' ,1)[1])
                outputvrf3 = str(outputvrf2.split('"value": "', 1)[1])
                outputvrf4 = str(outputvrf3.split('"', 1)[0])
                #print (outpututf)
                print ("VRF: " + outputvrf4)
        except IndexError:
                print ("Ingen VRF")

        ###SUbnet
        outputnet2 = str(outpututf.split('"network"' ,1))
        outputnet3 = str(outputnet2.split(': "', 1)[1])
        outputnet4 = str(outputnet3.split(':', 1)[1])
        outputnet5 = str(outputnet4.split('"', 1)[0])
        #print (outputnet2)
        print ("Subnet: " + outputnet5)

        ####Comments
        repons1 = ("https://infoblox.company.dk/wapi/v2.11/ipv4address?ip_address=")
        repons2 = ("&_return_fields=comment")
        repons3 = repons1+IP+repons2
        nyresponse = requests.get((repons3), verify=False, auth=('username', 'password'))
        output = str(nyresponse.content, 'utf-8')
        print (output)
        outputcomment2 = (output.split('"comment"',1)[1])
        outputcomment3 = (outputcomment2.split('"',1)[1])
        outputcomment4 = (outputcomment3.split('"',1)[0])
        print (outputcomment4)
        try:
                outputkrydsA = str(outpututf.split('Krydsfelt"' ,1)[1])
                if outputkrydsA.find("Proto") != -1:
                        print(output2.split("comment"))
                        outputkryds17 = ("N/A")
                else:
                        a = ("aaaa")
        except IndexError:
                a = ("aaa")
        try:
                outputcom2 = str(outpututf.split('"comment"' ,1)[1])
                outputcom3 = str(outputcom2.split('"', 1)[1])
                outputcom4 = str(outputcom3.split('"', 1)[0])
                outputcom5 = str(outputcom4.split('"', 1)[0])
                print ("commennt: " + outputcom4)
        except IndexError:
                print ("ingen comments")
                outputcom4 = ("N/A")
        ##Sagsnummer
        try:
                outputsag2 = str(outpututf.split('"Sagsnummer"' ,1)[1])
                outputsag3 = str(outputsag2.split('value', 1)[1])
                outputsag4 = str(outputsag3.split('"', 1)[1])
                outputsag5 = str(outputsag4.split('"', 1)[1])
                outputsag6 = str(outputsag5.split('"', 1)[0])
                print ("Sagsnummer: " + outputsag6)
        except IndexError:
                print ()
                outputsag6 = ("N/A")

        ###NAME og used status (Nyt curl)
        time.sleep(1)
        params = {
                '_return_as_object': '1',
                'ip_address': IP,
        }

        responseA = requests.get('https://infoblox.company.dk/wapi/v2.11/ipv4address', params=params, verify=False, auth=('username', 'password'))
        responseB = str(responseA.content, 'utf-8')
        print (responseB)
        ### Name
        try:
                outputname = str(responseB.split('"names"' ,1)[1])
                outputname2 = str(outputname.split('"', 1)[1])
                outputname3 = str(outputname2.split('"', 1)[0])
                print ("outputname: " + outputname3)
        except IndexError:
                print ()
                outputname3 = ("N/A")
        ### Used/Active
        try:
                outputstatus = str(responseB.split('"status"' ,1)[1])
                outputstatus2 = str(outputstatus.split('"', 1)[1])
                outputstatus3 = str(outputstatus2.split('"', 1)[0])
                print ("outputstatus: " + outputstatus3)
        except IndexError:
                print ()
                outputstatus3 = ("N/A")
        ### Mac address
        try:
                outputmac = str(responseB.split('"mac_address"' ,1)[1])
                outputmac1 = str(outputmac.split('"', 1)[1]) 
                outputmac2 = str(outputmac1.split('"', 1)[0])
                print ("outputmac: " + outputmac2)
        except IndexError:
                print ()
                outputmac2 = ("N/A")







        print (outputkryds17)
        
        with open("test.txt", "a") as myfile:
                myfile.write(IP +";" + outputnet5 + ";" + outputkryds17 + ";" + outputtypeE + ";" + outputsite5 + ";" + outputcom4 + ";" + outputsag6 + ";" + outputname3 + ";" + outputstatus3 + ";" + outputcomment4 + ";" + outputmac2 + "\n")


file = open('input.txt', 'r')
lines = file.readlines()

for index, line in enumerate(lines):
        IP = (line.strip())
        infobloxdata()
