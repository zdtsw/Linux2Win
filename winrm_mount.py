import winrm
import sys
import getopt


def parse_args():
    password = None
    server = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "s:p:a:")
        for opt, arg in opts:
            if opt == "-s":
                server = arg
            elif opt == "-p":
                password  = arg
            elif opt == "-a":
                action = arg
    except getopt.GetoptError:
        print "I NEED PASSWORD AND SERVER NAME"


def main():
    server, password = = parse_args()
    endpoint = "%s://%s:%s/wsman" % ("http", server, "5985")
    username = "MYCOMPANY.COM\jenkins_user"

    c = winrm.Protocol(endpoint=endpoint, transport="ntlm", username=username, password=password, server_cert_validation='ignore')
    shell_id = c.open_shell()
    if action == "mount"
        command_id = c.run_command(shell_id, 'C:\\Temp\\mountk.bat')
    elif action == "unmount"
        command_id = c.run_command(shell_id, 'C:\\Temp\\mountk2.bat')

    std_out, std_err, status_code = c.get_command_output(shell_id, command_id)

    print "######################STDOUT: %s" % (std_out)

    c.cleanup_command(shell_id, command_id)
    c.close_shell(shell_id)

    sys.exit(status_code)

if __name__ == "__main__":
    main()

