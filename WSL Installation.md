# WSL Installation Guide — Windows 11

> **Windows Subsystem for Linux (WSL)** lets you run a full Linux environment directly on Windows 11, without a VM or dual-boot.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Step 1 — Enable WSL (one command)](#step-1--enable-wsl-one-command)
- [Step 2 — Choose a Linux Distribution](#step-2--choose-a-linux-distribution)
- [Step 3 — First Launch & User Setup](#step-3--first-launch--user-setup)
- [Step 4 — Update Linux Packages](#step-4--update-linux-packages)
- [Step 5 — Verify WSL Version](#step-5--verify-wsl-version)
- [Step 6 — (Optional) Set WSL 2 as Default](#step-6--optional-set-wsl-2-as-default)
- [Step 7 — (Optional) Install Windows Terminal](#step-7--optional-install-windows-terminal)
- [Useful WSL Commands](#useful-wsl-commands)
- [File System — Where Things Live](#file-system--where-things-live)
- [Networking Tips](#networking-tips)
- [Uninstalling a Distribution](#uninstalling-a-distribution)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| OS | Windows 11 (any edition) |
| Windows build | 22000 or later (`winver` to check) |
| Architecture | x64 or ARM64 |
| BIOS | Virtualization enabled (Intel VT-x / AMD-V) |
| Permissions | Administrator account |

> **Virtualization check:** Open Task Manager → Performance → CPU. Look for *Virtualization: Enabled*. If disabled, enable it in your BIOS/UEFI settings.

---

## Step 1 — Enable WSL (one command)

Open **PowerShell** or **Command Prompt** as **Administrator** and run:

```powershell
wsl --install
```

This single command:
- Enables the **Virtual Machine Platform** and **WSL** Windows features
- Downloads and installs the latest **WSL 2 Linux kernel**
- Sets **WSL 2** as the default version
- Installs **Ubuntu** (the default distribution)

**Restart your PC** when prompted.

> ℹ️ If WSL was already partially installed, run `wsl --update` to make sure you have the latest kernel.

---

## Step 2 — Choose a Linux Distribution

After restart, Ubuntu will launch automatically. If you want a **different distro**, list available ones first:

```powershell
wsl --list --online
```

Example output:

```
NAME                                   FRIENDLY NAME
Ubuntu                                 Ubuntu
Debian                                 Debian GNU/Linux
kali-linux                             Kali Linux Rolling
Ubuntu-22.04                           Ubuntu 22.04 LTS
Ubuntu-24.04                           Ubuntu 24.04 LTS
OracleLinux_9_1                        Oracle Linux 9.1
openSUSE-Leap-15.6                     openSUSE Leap 15.6
```

Install a specific distro:

```powershell
wsl --install -d <DistroName>
```

**Example — install Debian:**

```powershell
wsl --install -d Debian
```

You can install **multiple distributions** side by side.

---

## Step 3 — First Launch & User Setup

After installation, the distro will open and ask you to create a **Unix user account**:

```
Enter new UNIX username: adam
New password:
Retype new password:
passwd: password updated successfully
```

> ⚠️ The password prompt is silent — you won't see characters as you type. This is normal.

This user is separate from your Windows account and will be the default sudo user inside WSL.

---

## Step 4 — Update Linux Packages

Once inside your Linux terminal, immediately update the package index and upgrade installed packages:

```bash
sudo apt update && sudo apt upgrade -y
```

For Arch-based distros (e.g., if using a custom image):

```bash
sudo pacman -Syu
```

---

## Step 5 — Verify WSL Version

Back in PowerShell, confirm WSL 2 is active:

```powershell
wsl --list --verbose
```

Expected output:

```
  NAME      STATE           VERSION
* Ubuntu    Running         2
```

The `VERSION` column should show **2**. If it shows `1`, upgrade it:

```powershell
wsl --set-version Ubuntu 2
```

---

## Step 6 — (Optional) Set WSL 2 as Default

Ensure all future distro installs use WSL 2 by default:

```powershell
wsl --set-default-version 2
```

---

## Step 7 — (Optional) Install Windows Terminal

**Windows Terminal** provides tabs, profiles, and a much better experience than the default console.

Install from the Microsoft Store:

```powershell
winget install --id Microsoft.WindowsTerminal -e
```

Once installed, your WSL distros appear automatically as profiles in the dropdown.

---

## Useful WSL Commands

| Command | Description |
|---------|-------------|
| `wsl` | Launch the default distro |
| `wsl -d <Name>` | Launch a specific distro |
| `wsl --list --verbose` | List all installed distros with WSL version |
| `wsl --list --online` | Show available distros to install |
| `wsl --install -d <Name>` | Install a specific distro |
| `wsl --set-default <Name>` | Change the default distro |
| `wsl --shutdown` | Stop all running WSL instances |
| `wsl --terminate <Name>` | Stop a specific distro |
| `wsl --update` | Update the WSL kernel |
| `wsl --status` | Show WSL configuration |
| `wsl --export <Name> file.tar` | Backup a distro |
| `wsl --import <Name> <Path> file.tar` | Restore a distro |
| `wsl --unregister <Name>` | Remove a distro (⚠️ deletes all data) |

---

## File System — Where Things Live

Understanding where files live is essential to avoid performance issues.

### Linux files (fast ✅)

Your Linux home directory lives inside WSL's virtual disk:

```
\\wsl$\Ubuntu\home\<username>\
```

Access it from Windows Explorer by typing `\\wsl$` in the address bar.

### Windows files (accessible, slower ⚠️)

Windows drives are mounted under `/mnt/` inside WSL:

```bash
ls /mnt/c/Users/YourName/
```

> **Performance tip:** Keep your project files inside the Linux filesystem (`~/projects/`) for best I/O speed. Cross-filesystem access (e.g., working on `/mnt/c/` from WSL) is significantly slower.

### Open current Linux folder in Windows Explorer

```bash
explorer.exe .
```

### Open VS Code from WSL

```bash
code .
```

> Requires the **Remote - WSL** extension in VS Code (installed automatically on first use).

---

## Networking Tips

WSL 2 uses a virtualized network adapter. By default:

- WSL can access the internet directly
- Windows can reach WSL services via `localhost` (e.g., a web server on port 3000)
- Other devices on your LAN **cannot** reach WSL services by default (requires port forwarding)

**Find your WSL IP:**

```bash
ip addr show eth0 | grep "inet "
```

**Forward a port from Windows to WSL (run as Admin in PowerShell):**

```powershell
netsh interface portproxy add v4tov4 listenport=3000 listenaddress=0.0.0.0 connectport=3000 connectaddress=$(wsl hostname -I)
```

---

## Uninstalling a Distribution

> ⚠️ This permanently deletes all data inside that distro.

```powershell
wsl --unregister Ubuntu
```

To fully remove WSL itself, go to:
**Settings → Apps → Installed apps → Windows Subsystem for Linux** → Uninstall.

---

## Troubleshooting

### `wsl --install` fails with error 0x80370102

**Cause:** Virtualization is disabled in BIOS.  
**Fix:** Restart → enter BIOS/UEFI → enable Intel VT-x or AMD-V → save and reboot.

---

### `Error: 0xc03a001a` when launching distro

**Cause:** WSL 2 virtual disk issue, often after a Windows update.  
**Fix:**

```powershell
wsl --shutdown
wsl --update
```

---

### Linux filesystem is slow on `/mnt/c/`

**Cause:** Cross-filesystem performance penalty in WSL 2.  
**Fix:** Move your working files to `~/` inside WSL.

---

### Cannot connect to the internet from WSL

**Fix — reset DNS:**

```bash
sudo rm /etc/resolv.conf
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
sudo chattr +i /etc/resolv.conf
```

---

### WSL version shows `1` after install

```powershell
wsl --set-default-version 2
wsl --set-version <DistroName> 2
```

---

## Additional Resources

- [Official Microsoft WSL Documentation](https://learn.microsoft.com/en-us/windows/wsl/)
- [WSL GitHub Repository](https://github.com/microsoft/WSL)
- [Windows Terminal Documentation](https://learn.microsoft.com/en-us/windows/terminal/)
- [VS Code Remote – WSL](https://code.visualstudio.com/docs/remote/wsl)

---

*Guide written for Windows 11 — WSL 2. Last updated: 16 May 2026.*
