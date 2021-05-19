## GenerationZ Challenge (challenge.fi) | Web | Securelogin
##### Author: Sanduuz | Date: 19.05.2021
---
### Challenge details:
* Points: 299
* Solves: 16
* Difficulty: Hard (?)
* Description:<big><pre>
The development team has made a proof of concept of the new Securelogin site. Somebody managed to put it to the public internet, but dev team is so confident that they don't think it matters so they left it open!

Can you prove them wrong?! Are you the one who fetches the flag from /etc/flag.txt - file?

You can find the challenge from: http://securelogin.challenge.fi:8880/
</pre></big>
* Note:<big><pre>
This challenge is based on a real world example of a finding from a bug bounty target. Pretty much 1=1, but some clues maybe around what to do...
</big></pre>

---

### Writeup:

**TL;DR**\
**Out-of-band XML External Entity (OOB-XXE) attack to read contents of /etc/flag.txt on server.**

The challenge starts with a website that looks like this:
![Website Frontpage](https://raw.githubusercontent.com/Sanduuz/CTFWriteUps/master/challenge.fi/Web/Securelogin/attachments/website_frontpage.png)

First we should take a look at the source code of the website. This can be achieved with the keyboard shortcut <kbd>CTRL</kbd>+<kbd>U</kbd> 

Source code | Vulnerable binary
:----------:|:-----------------:
![source code](https://raw.githubusercontent.com/Sanduuz/CTFWriteUps/master/PicoCTF2018/BinaryExploitation/BufferOverflow2/attachments/source.png) | ![vulnerable binary](https://raw.githubusercontent.com/Sanduuz/CTFWriteUps/master/PicoCTF2018/BinaryExploitation/BufferOverflow2/attachments/vuln.png)

##### Note: In order to exploit the vulnerable program locally, you will need to create a file called `flag.txt` with a fake flag inside. In order to get the real flag you have to exploit the vulnerable program in the shell server.

So let's debug the code first.\
In the very beginning some libraries are being imported but those can be ignored. After that, few variables are defined. _**BUFSIZE**_ with the value of 100 and _**FLAGSIZE**_ with the value of 64. The _**FLAGSIZE**_ can also be ignored (just make sure your fake flag is not over 64 characters long). After those variables are defined, the rest of the code is just defining the functions.

Now starting from the `main` function, it can be seen that the program sets some gid bits. This is because the program is an _**SUID binary**_ meaning that it has **elevated permissions** during execution. SUID binaries are used in actions which require higher privileges than the normal user has. These include actions such as changing a password. The program requires elevated privileges in order to read the `flag.txt` file because our user has no permissions to do so.

After the permissions have been handled the program prints a string `"Please enter your string: "` to _stdout_ and then calls for the `vuln` function. In `vuln` a **buffer** is created with the size of _**BUFSIZE**_ which is 100 bytes. After that the program reads our input from _stdin_ and **stores** it into the **buffer**. Our input is reflected back to us and the program exits.

That seems to be all about program flow, but what about the `win` function you might ask? We need to exploit a _**buffer overflow**_ vulnerability in the `vuln` function as the name tells us. A _**buffer overflow**_ is an anomaly where a buffer in the program is filled with too much data resulting in the overflowing and overwriting of data.

This leads us to a thing called _**stack**_. What is a _**stack**_?\
Stack is a segment in computer memory. There are other segments such as text, data, bss and heap. Segments like text hold the code that is executed and it is read-only so the data in those segments can not be overwritten. However in stack, the data is not read-only so it can be overwritten. The stack might be a bit confusing at first because it grows _'upside down'_ towards lower memory addresses. Now how can we access the `win` function when it's never called in our program? When a function call in program is done, some things are going on in the stack.

1. A _stack frame_ for the function is created and pushed onto the stack. Inside the _stack frame_ is the data that the function needs. In addition to parameters that the function might take, there's also a _**return address (RET)**_ and a _**stack frame pointer (SFP)**_. _**Return address (RET)**_ is the address in memory where the function will return after execution. _**Stack frame pointer (SFP)**_ is the value of _base pointer (BP)_ and is used to restore the value of _base pointer (BP)_ after execution.
2. The current value of _stack pointer (SP)_ is copied to _base pointer (BP)_
3. Memory is allocated on the stack for the local variables of the function. (In the `win` function for example the flag buffer)

When calling the `vuln` function, the stack should look something like this:
![Stack](https://raw.githubusercontent.com/Sanduuz/CTFWriteUps/master/PicoCTF2018/BinaryExploitation/BufferOverflow2/attachments/stack.png)

This can be confirmed by running the program in a debugger such as GDB and inspecting the stack after supplying our string.
![Vulnerable assembly]()

*** TO BE CONTINUED ***