# Automated Installation Script for lc3tools v0.13

#### lc3tools_installer: [Linux](https://github.com/AllenHeartcore/AllenHeartcore_MiscPrograms/raw/main/ECE120_TA_resources/lc3tools_installer_linux), [Mac](https://github.com/AllenHeartcore/AllenHeartcore_MiscPrograms/raw/main/ECE120_TA_resources/lc3tools_installer_mac), try the [Compatible version](https://github.com/AllenHeartcore/AllenHeartcore_MiscPrograms/raw/main/ECE120_TA_resources/lc3tools_installer_compatible) if installation fails (GitHub may require a VPN). 

`cd` to where the script is located, and run the following commands: 

##### (Linux users)
```shell
chmod +x ./lc3tools_installer_linux
./lc3tools_installer_linux
```

##### (Mac users)
```shell
chmod +x ./lc3tools_installer_mac
./lc3tools_installer_mac
```

The following output signals a successful installation: 
```
<<< lc3tools Installer of _____ >>>

Installing support libraries...
Installing flex
Installing wish
Installing libreadline6-dev
Installing libncurses5-dev

Writing source files...
Writing COPYING
Writing NO_WARRANTY
Writing README
Writing configure
Writing lc3.def
Writing lc3.f
Writing lc3convert.f
Writing lc3os.asm
Writing lc3sim-tk.def
Writing lc3sim.c
Writing lc3sim.h
Writing Makefile.def
Writing symbol.c
Writing symbol.h

Configuring environment...
Configuring for ________________...
Installation directory is /usr/local/bin

Compiling files...
Compilation successful.

Building the module...
Build successful.

Done.

```

##### **WARNING:** Some `readline` functionality is removed from `lc3sim.c` (lines 675 and 1799) to suppress errors. 

##### **NOTE:** For those using the virtual machine provided by the professor, `lc3tools` have been pre-installed. 

### Please __**post a thread**__ below if you encounter any error messages. 

### Please __**Like**__ this note if the script works! 
