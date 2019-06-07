import subprocess
import shlex
import xml.etree.ElementTree as ET

niktoportlist = []


def nmapexec():

    cmd = "nmap -sC -oX nmap_xml.xml " + ipaddr

    try:
        rout = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE).communicate()[0]
        rout = rout.decode()
        print(rout)
        with open("nmap_result.txt", "w") as nmap:
            nmap.write(rout)
    except Exception as e:
        print("Error >> ".format(e))
    xml_parse()


def xml_parse():

    tree = ET.parse('nmap_xml.xml')
    root = tree.getroot()

    for data in root.iter('port'):
        for service in data.iter('service'):
            if service.attrib['name'] == 'http':
                print(data.attrib['portid'])
                niktoportlist.append(data.attrib['portid'])
            if service.attrib['name'] == 'https':
                print(data.attrib['portid'])
                niktoportlist.append(data.attrib['portid'])


def niktoexec():

    with open("nikto_result.txt", "w") as nikto:
        for ports in niktoportlist:

            cmd = "nikto -h " + ipaddr + " -port " + ports
            print(cmd)

            try:
                rout = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE, stdout=subprocess.PIPE).communicate(
                    input='n')[0]
                rout = rout.decode()
                print(rout)
                nikto.write(rout)

            except Exception as e:
                print("Error >> ".format(e))


def enumexec():

    cmd = "enum4linux -U -o " + ipaddr

    try:
        rout = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE).communicate()[0]
        rout = rout.decode()
        print(rout)
        with open("enum4linux_result.txt", "w") as enum4linux:
            enum4linux.write(rout)
    except Exception as e:
        print("Error >> ".format(e))


ipaddr = str(raw_input("Enter IP : "))
nmapexec()
niktoexec()
enumexec()
