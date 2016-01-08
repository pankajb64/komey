import pxssh

px = pxssh.pxssh()
px.login("try.rummycircle.com", "pankaj.b", "Amazon24x7$")
px.prompt()
px.interact()
px.sendline("pwd")
px.prompt()
px.sendline("sleep 5")
px.prompt()
px.logout()
