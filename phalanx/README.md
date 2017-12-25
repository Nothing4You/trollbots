# Phalanx
A localhost clone flooder for IRC

##### Information
The script will clone flood an IRC network. The nickname, username, realname, and hostname of the clones will all be completely random. The clones will all have the same IP address, so you will have setup higher session limits for clone connections. Also, in order for this script to work, the clones will require operator privledges.

##### Session Limit
**Note:** This is an example if you wanted to clone from localhost. Any IP address will work. but you will get a faster connection being on localhost.

Edit the `~/services/conf/operserv.conf` config file for Anope, and change `maxsessionlimit` to **500**.

On your IRC do `/msg OperServ reload` and then `/msg OperServ exception add 127.0.0.1 500 Phalanx`.

Edit ~/unrealircd/conf/unrealircd.conf` and add `allow { ip 127.0.0.1; class phalanx; maxperip 500; };` and `class phalanx { pingfreq 120; maxclients 500; sendq 15M; recvq 5000; options { nofakelag; }; };`

##### Commands
The clones will accept any message startign with a `!` and sned the raw data that follows after it.
For example, doing `!JOIN #test` and then `PRIVMSG #test :SUP` will make the clones join #test and say "SUP" in that channel.

| Command | Description |
| --- | --- |
| !attack \<nick> | Send a Privage Message and SAJOIN \<nick> to a random channel. |
| !recycle | Get a new nickname, username, realname, and hostname. |
