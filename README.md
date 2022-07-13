# mini-dns-server
This project is done in Linux OS

## How to install
1. Copy the file to a cloud instance of your choice. This can be done using `scp`.
2. First, go to directory where this file exist.
3. Use the `scp` command.
>`scp -P <remote_port> dns_server.py <remote_user>@<remote_host>:<target_directory>`<br>
>Fill `<?>` with your own remote server credentials.
4. Run the python file on the remote host.

## How to make a dns query
1. Install `dig`.
2. Run `dig -p <port> <remote_host> <domain_name>`.
3. Check results, if the domain exist in the server dictionary it will return an IP address.