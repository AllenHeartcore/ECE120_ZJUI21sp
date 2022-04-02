# WSL, A Substitution for VirtualBox

*This note on setting up the Windows Subsystem for Linux (WSL) environment, with some minor modifications, is originally written by Haozhe Chen, a former TA from the ECE220 course.*

## **A. What is WSL?**

The full name of WSL is **Windows Subsystem for Linux**. It "includes most command-line tools, utilities, and applications -- directly on Windows, unmodified, without the overhead of a traditional virtual machine or dual-boot setup". You can learn more details about it on this webpage: [What is Windows Subsystem for Linux | Microsoft Docs](https://docs.microsoft.com/en-us/windows/wsl/about).

WSL is supported on Windows 10 or newer versions. 

**NOTE 1**: Using WSL for this course is **completely voluntary**! Installing the provided VM ([`ECE220vmv3.ova`](https://zjuintl-my.sharepoint.com/:f:/g/personal/kindrv_intl_zju_edu_cn/EmegqYbzXkhKuGgJZ_U65dMBvj4jFkA1iJPYdvQFpMaoUw?e=x9Rgwx)) on VirtualBox is the best option and meets all the requirements. WSL is only for those who have unfixable bugs on VirtualBox or who are interested.
**NOTE 2**: If you decide to use WSL, you are choosing **a way with less help**. For the problems that occur only on WSL, you need to debug or find the solutions on your own. Instructors only help to answer problems that happen to VB.

## **B. What can WSL give you?**

The most intuitive benefit is that it allows you to use Linux on Windows without opening a VM. (Actually, WSL is a VM, but it is so light and well-optimized that you can treat it as a command-line software.) It brings convenience when you interact between the host and guest systems. Here are some demos:

1. You can easily **access files/folders** on both Windows and WSL.
   ![mkdir.gif](https://campuspro-uploads.s3.us-west-2.amazonaws.com/55061238-78dc-4c63-b9f8-33927a6a4b58/62f8f202-3052-4610-985a-f7a976bac03f/mkdir.gif)

2. You can **open GUI software** on Linux with a Windows window
   ![lc3sim-tk.gif](https://campuspro-uploads.s3.us-west-2.amazonaws.com/55061238-78dc-4c63-b9f8-33927a6a4b58/d166febd-9786-46ff-ba57-1c8ad47ad6e9/lc3sim-tk.gif)

3. You can **edit your file** with Windows software but run it with Linux (WSL).
   ![vscode_modified.gif](https://campuspro-uploads.s3.us-west-2.amazonaws.com/55061238-78dc-4c63-b9f8-33927a6a4b58/36914a6e-de06-4716-8067-e533535f5d2d/vscode_modified.gif)

4. You can discover more benefits with yourself!

## **C. How to install WSL?**

### **C1. Installing WSL itself**

There are two ways to install WSL: 

1. Following the instructions in [Installing WSL on Windows 10 | Microsoft Docs](https://docs.microsoft.com/en-us/windows/wsl/install-win10) will install WSL to your C disk. You can find the files in path `C:\Users\{YouUserName}\AppData\Local\Packages\CanonicalGroupLimited.Ubuntu18.04onWindows_79rhkp1fndgsc\LocalState\rootfs` or simply access `\\wsl$` with the file explorer. Be aware that the WSL will take about 10G memory and even more as you install the software in it.

2. If your C disk is almost full or you just want to install it somewhere else, you can try the portable version. Follow the instruction in [Manually download Windows Subsystem for Linux (WSL) Distros | Microsoft Docs](https://docs.microsoft.com/en-us/windows/wsl/install-manual). We still highly recommend reading through the instruction in method 1 to have an overview of WSL.

### **C2. Installing X server**

To use GUI software on WSL, you need to install an X server, such as VcXsrv, Xming, and Remote Desktop Software. X server makes it possible to use GUI software on WSL as a Windows GUI software.

VcXsrv is recommended for its stability. You download it via this link: [VcXsrv Windows X Server download | SourceForge.net](https://sourceforge.net/projects/vcxsrv). Just keep the default configure when setting up.

After successfully installing VcXsrv, you can find an `XLaunch` in your startup list. Please remember to Launch the X server every time you want to use GUI software on WSL.

## **D. How to use `lc3tools` in WSL?**

### **D1. Installing the basic tools**

WSL is a tiny distribution and lacks some basic compiling tools. Install it with the following command.

``` bash
$ sudo apt install make gcc flex wish
```

### **D2. Installing `lc3tools`**

Just follow the steps given in `Guide2VMImage.docx`

``` bash
$ wget 'http://lumetta.web.engr.illinois.edu/lc3tools.0.13.tar.bz2' -O lc3tools.tar.bz2
$ tar -jxvf lc3tools.tar.bz2
$ cd lc3tools
# edit ./configure here!
$ ./configure --installdir /usr/bin
$ make
$ sudo make install
```

For those who use Ubuntu WSL, you may want to modify `./configure` a little to avoid errors about "-lcurses":

* Enter the `lc3tools` folder, use `nano ./configure` to edit the file.

* Set the value of `OS_SIM_LIBS` to be "", instead of "-lcurses"

* It should looks like this:![image.png](https://campuspro-uploads.s3.us-west-2.amazonaws.com/55061238-78dc-4c63-b9f8-33927a6a4b58/22e21485-69fc-4665-9694-6b5f60f74955/image.png)

* `Ctrl + O` , `Enter` to save the file and `Ctrl + X` to leave the file

* `./configure --installdir /usr/bin`, `make`, `sudo make install`.....

You can try `lc3as` in the command line to verify your installation. Then type `quit` to exit.

### **D3. Using `lc3tools` with GUI**

As you can start `lc3sim-tk` in Ubuntu VM,  you can also open a window in WSL for this software. Just try the following command:

``` bash
$ DISPLAY=:0 lc3sim-tk
```

The `DISPLAY=:0` means to send the GUI content to the DISPLAY with the name "0". That is the virtual ***display*** you started with VcXsrv, the X server.

You will see two poped windows of "lc3sim-tk" just like what you see in Ubuntu. **CONGRATULATIONS!!**

![image.png](https://campuspro-uploads.s3.us-west-2.amazonaws.com/55061238-78dc-4c63-b9f8-33927a6a4b58/7e17060f-b488-4702-bc9b-f548fbadd3b8/image.png)

## **E. Other tips**

Using WSL means there are two environments on your computer: the host (Windows) and the guest (WSL). Since the files can be easily visited on both sides, you can choose either environment to set up your workspace.
Here is my personal configuration -- you can make your own.

### **E1. Where are my files?**

Windows-->WSL: You can access your WSL files from Windows by typing` \\wsl$` in explorer.

WSL-->Windows: `cd /mnt/c` or replace "c" with "d"/"e"/"f"...

### **E2. Editor / IDE**

Using WSL means you can take advantage of various Windows software.

For example, you can set up a workspace on the WSL and connect via VSCode with the `remote: WSL` extension. Detailed instructions can be found here: [Work in Windows Subsystem for Linux with Visual Studio Code](https://code.visualstudio.com/docs/remote/wsl-tutorial#:\~:text=In%20the%20WSL%20terminal%2C%20make%20sure%20you%20are,Code%20to%20your%20path%20when%20it%20was%20installed.)

Other IDEs like Clion from Jetbrain support WSL function as well. You are free to try it, but it has no lc3 extension and may be overly elaborate for ECE220.

## **Good luck with setting up WSL!**
## **Hopefully, it can be a great productivity tool!**

<br/> <br/> <br/>

# Minimize Your Quartus Installation with ModelSim Support

Installing the full features of Quartus Lite requires over 25G on your computer. The following is an installation guide to help you get the essentials for **Lab 5**. 

## ***PLEASE FOLLOW THE STEPS IN THE GIVEN ORDER.***

1. Download [Intel Cyclone V Device Support](https://download.altera.com/akdlm/software/acdsinst/21.1std/842/ib_installers/cyclonev-21.1.0.842.qdz) and [Quartus Lite 21.1 Setup](https://download.altera.com/akdlm/software/acdsinst/21.1std/842/ib_installers/QuartusLiteSetup-21.1.0.842-windows.exe). Make sure the two files appear in the **same folder**. 
3. Run the setup. In the "**Select components**" step, be sure to select `Devices - Cyclone V (1430.9MB)`. **Record** the installation path -- it could be something like `D:\intelFPGA_lite\21.1`. 
3. Download [ModelSim 20.1.1 Setup](https://download.altera.com/akdlm/software/acdsinst/20.1std.1/720/ib_installers/ModelSimSetup-20.1.1.720-windows.exe) and run it. Choose the Starter version. You probably need to **manually alter the installation path** to match the path previously recorded. 
4. Run the Quartus software located in `[INSTALLATION_PATH]\quartus\bin64\quartus.exe`. In **Tools -> Options** menu, go to **General / EDA Tool Options** section and specify the location of ModelSim as `[INSTALLATION_PATH]\modelsim_ase\win32aloem`. There does *not* exist a field called ModelSim-Altera -- don't worry. 
6. Create (1) the project [.qpf], (2) the circuit [.bdf], (3) the waveform [.vwf], and compile the files as specified in the [Lab 5 Guide](https://wiki.illinois.edu/wiki/display/zjuiece120/Lab+5). 
7. When you are about to run the simulation, a little tweaking is required. In the waveform file, (1) go to **Simulation -> Simulation Settings**, (2) switch **HDL Language** from Verilog to VHDL, and (3) delete the ``-novopt`` flag in the 5th line of **ModelSim Script**. 

Everything should work fine now. Seek the TAs' help in case new problems arise! 

## **Useful Links**

[Intel Official Support](https://www.intel.com/content/www/us/en/support.html) (Your first go-to site in case of bugs)

[Intel Product Support Forum - Quartus](https://community.intel.com/t5/Intel-Quartus-Prime-Software/bd-p/quartus-prime-software)

[How to Begin a Simple FPGA Design](https://learning.intel.com/developer/learn/course/external/view/elearning/192/how-to-begin-a-simple-fpga-design)

[Become an FPGA Designer in 4 Hours](https://learning.intel.com/developer/learn/course/external/view/elearning/210/university-self-guided-lab-become-an-fpga-designer-in-4-hours)