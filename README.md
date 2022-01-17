# Threader3003

![visitor badge](https://visitor-badge.glitch.me/badge?page_id=LIIIs4ma.threader3003) ![language](https://img.shields.io/badge/language-python3-3572A5)

Threader3003 is an alternate version of threader3000. 

A script written in Python3 that allows multi-threaded full port scanning in **15 seconds.** 


## Installation

```
cd /opt
git clone https://github.com/LIIIs4ma/threader3003.git
cd threader3003
chmod +x threader3003.py
ln -s $(pwd)/threader3003.py /usr/local/bin/threader3003
```

## Options

```
-h, --help  show this help message and exit
-i I        IP address of the target [ex: -i 10.10.10.10]
-r R        Specify number of retries [ex: -r 1] [default: 1, max: 3]]
-t T        Specify number of thread [ex: -t 200] [default: 200, max: 250]
-p P        Set range of ports [ex: -p 1000] It means 0 to 1000 [default: 65536]
```

## Usage

```bash
threader3003
threader3003 -i 10.10.10.10
threader3003 -i 10.10.10.10 -r 3
threader3003 -i 10.10.10.10 -p 1023
```

## Screenshots

![image](https://user-images.githubusercontent.com/12685802/149636032-6227d8e0-7bae-43d5-93e9-082e1b5a2fa6.png)

## To-Do

- Automatically run on open ports
- Show which retry you are currently on 
- No open port scan flags has verbose
- Would you like to try well-known ports again?
- If KeyboardInterrupt occurs when scanning. Ask to user: Would you like to nmap founded open ports?
- OOP

## Can I use this tool to scan Facebook or other websites I don't have permission to scan?

*No. That would be illegal.  This tool is under a free license for use, however it is up to the user to observe all applicable laws and appropriate uses for this tool.  The creator does not condone, support, suggest, or otherwise promote unethical or illegal behavior.  You use this tool at your own risk, and under the assumption that you are utilizing it against targets and infrastructure to which you have permission to do so.  Any use otherwise is at your peril and against the terms of use for the tool.*

## Tested on

Linux kali 5.10.0-kali9-amd64 #1 SMP Debian 5.10.46-4kali1 (2021-08-09) x86_64 GNU/Linux
