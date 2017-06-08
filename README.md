# Linux2Win
A set of simple python scripts which does remotely login to Windows from Linux and execute WinRM 
The reason why I have such scripts is because: 
1. I am not a Win guy
2. I do not have proper tool to login Win
3. I do not know what to do on Win for what I do want to be done there
4. I am lazy, I used Jenkins to do everything, apart from drinking water


- winrm_mt.py
    Usage: python -u winrm_mt.py -a Import -e CI -s pong.mycompany.com -v 1.0.0 -p '****' -c 'c:\temp\windows.bat'
    You should modify all these arguments if you want any of them to be used for your purpose
    multi-threading python script, which does start one thread to login Windows and run some commands there, start another thread which reads logs on local Linux server (logs is shipped from windows to linux)
    I hardcode the username for "mycompany.com\jenkins_user" when I use ntlm, but if you use kerberos, you might need some token setup and use "jenkins_user@mycompany.com"
    Also log path is hardcoded as /var/log/zdtsw.log
    To use this script, you also need to install td-agent on both Linux and Windows ( http://docs.fluentd.org/v0.12/articles/install-by-rpm ; http://nxlog.co/products/nxlog-community-edition/download )
    Also port 5985 need to be accessable on Windows server from Linux server
    I turn on "-u" when run this script from python, due to python does buffer for the logs


- winrm_mount.py
    do the mount or umount drive on windows depend on the flag you use
    This script can be easilly modified to fit for all kind of single cmd run on Windows, which put the cmd as argument to python
    in this case, I call a batch script on windows which is mount.bk or umount.bk which you can find under the "resoruce" folder. it is hardcode with k:\, you need to replace with mounting point, user "jenkins_user" and password for real use.

Prerequisite:
  You need to have the WinRM lib installed on your Linux ( https://github.com/diyan/pywinrm)
  You also need the WinRM installed on Windows side, see detail README for how to install and config
  You need a valid AD user which can be used to login to the Windows server. For testing purpose, you can have a local windows user as well (use basic protocal)



Some thanks for my friends: Marcus L ; Roger W; Simon E who gave me helps and hints
