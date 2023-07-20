# Features: 
- multiple account support
- asynchronous scraper and adder 
- proxy support 
- filtering users by last online time and first name (more filters in later releases)
- Free tool

Still in development, soon more features will be added 

# Getting api_id and api_hash
* Go to http://my.telegram.org and log in.
* Click on API development tools and fill the required fields.
* copy "api_id" n "api_hash" after clicking create app 

# Installation and usage on windows
- Install python at least version 3.10 [how to install](https://www.digitalocean.com/community/tutorials/install-python-windows-10)
- Download the archive directly and unzip it or u can install git and download archive using git clone [install git](https://github.com/git-guides/install-git) (https://github.com/git-guides/install-git)

## Usage via terminal 
- open terminal - click win + R and then type cmd.exe
- ```pip3 install telethon```
- ```git clone https://github.com/evilbream/TG_adder_with_proxy```
- ```cd Tg_adder_with_proxy``` change directory to downloaded folder.
- ```tg_accs.txt```  - it’ll open  tg_accs.txt to which u can add name, api_id, api_hash and phone and save changes in this file. In the opened file there is an example, replace it with your own data, the data in the example is made up and will not work. If u later want to add more accounts. 
- ```proxy.txt```  - it’ll open  proxy.txt  if you want to use a proxy, add the data there and save, as shown in the example, all data also is made up.
- ```exclude_list.txt``` - it'll open exclude_list.txt. If u want to filter users by first name run it and add words. Users with this words in first name will be excluded
- ```python main_parser.py``` - To Scarpe members from group
- ```python main_adder.py``` - Add Scarped members to ur group.

## Usage via PyCharm
- download and install PyCharm community edition [jetbrains.com](https://www.jetbrains.com/pycharm/download/?section=windows)
- Open downloaded folder Tg_adder_with_proxy with PyCharm
- Add data as in example to file tg_accs.txt
- Add data as in example to proxy.txt if u wanna use proxy 
- Add data to exclude.txt if u wanna filter users by first name 
- Run in  PyCharm main_parser.py to scrape members 
- Run  in  PyCharm main_adder.py to add members

### Errors n questions
If u have any questions or errors fill free to text me

* Telegram - [malevolentkid](https://t.me//malevolentkid)
