#!/bin/bash

FLAG="Windowshater"

echo "[+] Start the SMB server"
smbserver.py -ip 172.17.0.4 -username jdhack -password "${FLAG}" vuln /workspace &
echo "[+] Start the HTTP server"
python3 -m http.server 80 &
echo "[+] Start the tcpdump"
tcpdump -i any -w dump.pcap &

echo "[+] Generate traffic for dump"

for i in {1..10}
do
    ping -c 2 google.com &> /dev/null
    curl https://google.com &> /dev/null
    dig jeannedhack.ctf.fr &> /dev/null
    ping -c 2 jeannedhack.ctf.fr &> /dev/null
    curl http://172.17.0.4/icanflag &> /dev/null
    curl http://jeannedhack.ctf.fr/getflag &> /dev/null
    curl http://jeannedhack.ctf.fr/flag.txt &> /dev/null
    ping justwannaflag.com &> /dev/null
    dig justwannaflag.com &> /dev/null
    curl http://172.17.0.4/pwn &> /dev/null
    curl http://172.17.0.4/\?q=\'+or+1=1+--+- &> /dev/null
    curl http://justwannaflag.com/flag &> /dev/null
    curl http://justwannaflag.com/please &> /dev/null
    curl http://justwannaflag.com/pleasegivemetheflag &> /dev/null
    ping -c 2 http://univ-rouen.fr &> /dev/null
    curl http://univ-rouen.fr &> /dev/null
    curl http://univ-rouen.fr/ctf/flag &> /dev/null
    curl http://univ-rouen.fr/ctf/give/flag &> /dev/null
    curl http://ctf.univ-rouen.fr/ssi/flag &> /dev/null
    curl http://ctf.univ-rouen.fr/ssi/flag?q=please &> /dev/null
    dig ctf.univ-rouen.fr &> /dev/null
    curl http://172.17.0.4/flag.txt &> /dev/null
    dig jeannedhackctf.univ-rouen.fr &> /dev/null
done

smbclient.py jdhack:${FLAG}@172.17.0.4

for i in {1..10}
do
    ping -c 2 google.com &> /dev/null
    curl https://google.com &> /dev/null
    dig jeannedhack.ctf.fr &> /dev/null
    ping -c 2 jeannedhack.ctf.fr &> /dev/null
    curl http://172.17.0.4/icanflag &> /dev/null
    curl http://jeannedhack.ctf.fr/getflag &> /dev/null
    curl http://jeannedhack.ctf.fr/flag.txt &> /dev/null
    ping justwannaflag.com &> /dev/null
    dig justwannaflag.com &> /dev/null
    curl http://172.17.0.4/pwn &> /dev/null
    curl http://172.17.0.4/\?q=\'+or+1=1+--+- &> /dev/null
    curl http://justwannaflag.com/flag &> /dev/null
    curl http://justwannaflag.com/please &> /dev/null
    curl http://justwannaflag.com/pleasegivemetheflag &> /dev/null
    ping -c 2 http://univ-rouen.fr &> /dev/null
    curl http://univ-rouen.fr &> /dev/null
    curl http://univ-rouen.fr/ctf/flag &> /dev/null
    curl http://univ-rouen.fr/ctf/give/flag &> /dev/null
    curl http://ctf.univ-rouen.fr/ssi/flag &> /dev/null
    curl http://ctf.univ-rouen.fr/ssi/flag?q=please &> /dev/null
    dig ctf.univ-rouen.fr &> /dev/null
    curl http://172.17.0.4/flag.txt &> /dev/null
    dig jeannedhackctf.univ-rouen.fr &> /dev/null
done

echo "[+] Kill server and tcpdump"
pkill smbserver
pkill python3
pkill tcpdump
