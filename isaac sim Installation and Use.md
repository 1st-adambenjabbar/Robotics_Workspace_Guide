# NVIDIA Isaac Sim Installation Guide
### Ubuntu (22.04 / 24.04) & Windows 11

In this section, I’ll walk you through installing Isaac Sim. I’ve personally set it up twice on Ubuntu and once on Windows 11. Unfortunately, my dual-boot configuration caused RTX GPU compatibility issues on Ubuntu, so I moved to Windows, where it runs flawlessly. You can also run Ubuntu via WSL on Windows if you prefer that workflow. Below, I’ll share complete installation guides for both operating systems.

> **Isaac Sim** is NVIDIA's GPU-accelerated robotics simulation platform built on Omniverse. This guide covers the **workstation (binary)** and **pip** installation methods for both Ubuntu and Windows 11, targeting **Isaac Sim 5.1.0** (latest stable, May 2026).

---

## Table of Contents

- [What Is Isaac Sim?](#what-is-isaac-sim)
- [System Requirements](#system-requirements)
- [Choosing an Installation Method](#choosing-an-installation-method)
- [Ubuntu Installation](#ubuntu-installation)
  - [Step 1 — Install NVIDIA Driver](#step-1--install-nvidia-driver-ubuntu)
  - [Step 2 — Install CUDA Toolkit](#step-2--install-cuda-toolkit-ubuntu)
  - [Step 3 — Install Python 3.11](#step-3--install-python-311-ubuntu)
  - [Step 4A — Install via pip (Recommended)](#step-4a--install-via-pip-recommended-ubuntu)
  - [Step 4B — Install via Binary (Workstation)](#step-4b--install-via-binary-workstation-ubuntu)
  - [Step 5 — First Launch (Ubuntu)](#step-5--first-launch-ubuntu)
- [Windows 11 Installation](#windows-11-installation)
  - [Step 1 — Install NVIDIA Driver](#step-1--install-nvidia-driver-windows)
  - [Step 2 — Install Python 3.11](#step-2--install-python-311-windows)
  - [Step 3 — Enable Long Path Support](#step-3--enable-long-path-support-windows)
  - [Step 4A — Install via pip (Recommended)](#step-4a--install-via-pip-recommended-windows)
  - [Step 4B — Install via Binary (Workstation)](#step-4b--install-via-binary-workstation-windows)
  - [Step 5 — First Launch (Windows)](#step-5--first-launch-windows)
- [Run the Compatibility Checker](#run-the-compatibility-checker)
- [(Optional) Install Isaac Lab](#optional-install-isaac-lab)
- [Useful Commands](#useful-commands)
- [Default Installation Paths](#default-installation-paths)
- [Troubleshooting](#troubleshooting)
- [Additional Resources](#additional-resources)

---

## What Is Isaac Sim?

Isaac Sim is a simulation platform for robotics built on **NVIDIA Omniverse**. It supports:

- Importing robots from **URDF, MJCF, and CAD** formats
- GPU-accelerated **PhysX** physics and **RTX** rendering
- **ROS / ROS2** integration
- Synthetic data generation and reinforcement learning via **Isaac Lab**
- Multi-sensor simulation at scale

> ⚠️ **Isaac Sim requires an NVIDIA RTX GPU with RT Cores.** Data-center GPUs without RT Cores (A100, H100) are **not supported**.

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **GPU** | NVIDIA RTX 3070 (8 GB VRAM) | NVIDIA RTX 4080 / higher |
| **VRAM** | 8 GB | 16 GB+ |
| **CPU** | Intel Core i7 / AMD Ryzen 7 | Intel Core i9 / Ryzen 9 |
| **RAM** | 32 GB | 64 GB+ |
| **Storage** | 50 GB SSD | 100 GB+ NVMe SSD |
| **OS (Linux)** | Ubuntu 22.04 LTS | Ubuntu 22.04 LTS |
| **OS (Windows)** | Windows 11 | Windows 11 |
| **NVIDIA Driver (Linux)** | 580.65.06+ | Latest production branch |
| **NVIDIA Driver (Windows)** | 580.88+ | Latest production branch |
| **Python** | 3.11 (for Isaac Sim 5.x) | 3.11 |
| **CUDA** | 12.x | 12.6+ |
| **Internet** | Required | Required |

> ⚠️ **Ubuntu 24.04** is not fully supported for source builds — if using 24.04, you must install `gcc-11 / g++-11` and cannot use GCC 12+. For most users, **Ubuntu 22.04 LTS** is the recommended Linux distribution.

> ℹ️ GPUs with less than 16 GB VRAM may struggle with complex scenes rendering more than 16 MP per frame.

---

## Choosing an Installation Method

| Method | Best For | Linux | Windows |
|--------|----------|-------|---------|
| **pip** | Beginners, most users | ✅ | ✅ |
| **Binary (Workstation)** | Full GUI, VS Code integration | ✅ | ✅ |
| **Docker Container** | CI/CD, headless servers | ✅ | ❌ |
| **Build from source** | Modifying Isaac Sim itself | ✅ | ✅ |

This guide covers **pip** and **binary (workstation)** methods.

---

## Ubuntu Installation

### Step 1 — Install NVIDIA Driver (Ubuntu)

Check your current driver:

```bash
nvidia-smi
```

If no driver is installed, or the version is below 580:

```bash
# Add the graphics PPA
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update

# Install the recommended production branch driver
sudo apt install nvidia-driver-580

# Reboot
sudo reboot
```

Verify after reboot:

```bash
nvidia-smi
# Driver Version should show 580.x or newer
```

> 💡 On a new GPU or if you encounter issues, install the `.run` installer directly from the [NVIDIA Unix Driver Archive](https://www.nvidia.com/en-us/drivers/unix/) for the latest production branch.

---

### Step 2 — Install CUDA Toolkit (Ubuntu)

Check if CUDA is already present:

```bash
nvcc --version
```

If not installed, install CUDA 12.6 (recommended):

```bash
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt install cuda-12-6
```

Add CUDA to your PATH (add to `~/.bashrc`):

```bash
echo 'export PATH=/usr/local/cuda-12.6/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.6/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
```

Verify:

```bash
nvcc --version
# nvcc: NVIDIA (R) Cuda compiler driver ... release 12.6
```

---

### Step 3 — Install Python 3.11 (Ubuntu)

Isaac Sim 5.x requires **exactly Python 3.11**.

```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev
```

Verify:

```bash
python3.11 --version
# Python 3.11.x
```

> ⚠️ **Ubuntu 24.04 note:** If building from source, install GCC 11 explicitly:
> ```bash
> sudo apt install gcc-11 g++-11
> sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 200
> sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 200
> ```

---

### Step 4A — Install via pip (Recommended, Ubuntu)

**1. Check GLIBC version (must be ≥ 2.35):**

```bash
ldd --version
# ldd (GNU libc) 2.35  ← Ubuntu 22.04 satisfies this
```

**2. Create a Python 3.11 virtual environment:**

```bash
python3.11 -m venv ~/env_isaacsim
source ~/env_isaacsim/bin/activate
```

**3. Upgrade pip:**

```bash
pip install --upgrade pip
```

**4. Install PyTorch with CUDA support:**

```bash
# For CUDA 12.x
pip install torch==2.7.0 torchvision==0.22.0 --index-url https://download.pytorch.org/whl/cu128
```

**5. Install Isaac Sim 5.1.0:**

```bash
pip install 'isaacsim[all,extscache]==5.1.0' --extra-index-url https://pypi.nvidia.com
```

> ℹ️ On first install, accept the NVIDIA EULA when prompted by typing `Yes`.

**6. Verify the installation:**

```bash
python -c "import isaacsim; print('Isaac Sim installed successfully')"
```

---

### Step 4B — Install via Binary (Workstation, Ubuntu)

**1. Download the binary:**

Go to [https://developer.nvidia.com/isaac-sim](https://developer.nvidia.com/isaac-sim) and download the latest **Linux binary** package (`.tar.gz`).

**2. Create the installation directory and extract:**

```bash
mkdir -p ~/isaacsim
tar -xzf ~/Downloads/isaac-sim-5.1.0-linux.tar.gz -C ~/isaacsim
cd ~/isaacsim
```

**3. Run the post-install script** (creates extension symlinks):

```bash
./post_install.sh
```

---

### Step 5 — First Launch (Ubuntu)

**pip install:**

```bash
source ~/env_isaacsim/bin/activate
isaacsim isaacsim.exp.full.kit
```

**Binary install:**

```bash
cd ~/isaacsim
./isaac-sim.sh
```

> ⏳ **First launch takes 10–20 minutes** — Isaac Sim downloads and caches all extensions. Subsequent launches are much faster.

To launch with a fresh config:

```bash
./isaac-sim.sh --reset-user
```

---

## Windows 11 Installation

### Step 1 — Install NVIDIA Driver (Windows)

1. Open **Device Manager** → Display adapters → note your GPU model.
2. Go to [https://www.nvidia.com/drivers](https://www.nvidia.com/drivers) and download the **580.88 or newer** production branch driver.
3. Run the installer. Choose **Custom Install** → check **Clean Install** for a fresh setup.
4. Reboot when prompted.

Verify in PowerShell:

```powershell
nvidia-smi
# Driver Version: 580.88 or newer
```

---

### Step 2 — Install Python 3.11 (Windows)

1. Download Python 3.11 from [https://www.python.org/downloads/release/python-3110/](https://www.python.org/downloads/release/python-3110/)
2. Run the installer.
3. ✅ Check **"Add Python 3.11 to PATH"** before clicking Install.

Verify in PowerShell:

```powershell
python --version
# Python 3.11.x
```

---

### Step 3 — Enable Long Path Support (Windows)

Windows limits file paths to 260 characters by default. Isaac Sim requires long path support.

**Option A — via PowerShell (Admin):**

```powershell
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" `
  -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

**Option B — via Group Policy:**

1. Press `Win + R` → `gpedit.msc`
2. Navigate to: **Local Computer Policy → Computer Configuration → Administrative Templates → System → Filesystem**
3. Enable **"Enable Win32 long paths"**

> ⚠️ Skipping this step commonly causes installation errors with deeply nested pip packages.

---

### Step 4A — Install via pip (Recommended, Windows)

Open **PowerShell** (not CMD):

**1. Create a virtual environment:**

```powershell
python -m venv C:\isaacsim\env_isaacsim
C:\isaacsim\env_isaacsim\Scripts\Activate.ps1
```

If you get an execution policy error:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**2. Upgrade pip:**

```powershell
pip install --upgrade pip
```

**3. Install PyTorch with CUDA 12 (required on Windows):**

```powershell
pip install torch==2.7.0 torchvision==0.22.0 --index-url https://download.pytorch.org/whl/cu128
```

**4. Install Isaac Sim 5.1.0:**

```powershell
pip install "isaacsim[all,extscache]==5.1.0" --extra-index-url https://pypi.nvidia.com
```

> ℹ️ Accept the NVIDIA EULA when prompted by typing `Yes`.

**5. Verify:**

```powershell
python -c "import isaacsim; print('Isaac Sim installed successfully')"
```

---

### Step 4B — Install via Binary (Workstation, Windows)

**1. Download the binary:**

Go to [https://developer.nvidia.com/isaac-sim](https://developer.nvidia.com/isaac-sim) and download the **Windows binary** package (`.zip`).

**2. Extract to `C:\isaacsim`:**

```powershell
Expand-Archive -Path "$env:USERPROFILE\Downloads\isaac-sim-5.1.0-windows.zip" -DestinationPath C:\isaacsim
cd C:\isaacsim
```

**3. Run the post-install script:**

```powershell
.\post_install.bat
```

---

### Step 5 — First Launch (Windows)

**pip install:**

```powershell
C:\isaacsim\env_isaacsim\Scripts\Activate.ps1
isaacsim isaacsim.exp.full.kit
```

**Binary install:**

```powershell
cd C:\isaacsim
.\isaac-sim.bat
```

> ⏳ **First launch takes 10–20 minutes** for extension caching. This is normal.

---

## Run the Compatibility Checker

Before reporting issues, run the built-in compatibility checker to verify your hardware meets requirements.

**From pip install:**

```bash
# Linux
pip install 'isaacsim[compatibility-check]==5.1.0' --extra-index-url https://pypi.nvidia.com
isaacsim isaacsim.exp.compatibility_check

# Windows (PowerShell)
pip install "isaacsim[compatibility-check]==5.1.0" --extra-index-url https://pypi.nvidia.com
isaacsim isaacsim.exp.compatibility_check
```

**From binary install:**

```bash
# Linux
./isaac-sim.compatibility_check.sh --/app/quitAfter=10 --no-window

# Windows
.\isaac-sim.compatibility_check.bat --/app/quitAfter=10 --no-window
```

The checker will highlight each requirement as **green** (pass), **yellow** (warning), or **red** (fail).

---

## (Optional) Install Isaac Lab

Isaac Lab is the framework for robot learning built on top of Isaac Sim. Install it after Isaac Sim is working.

```bash
# Clone the repository
git clone https://github.com/isaac-sim/IsaacLab.git
cd IsaacLab

# Linux
./isaaclab.sh --install

# Windows (PowerShell)
.\isaaclab.bat --install
```

Verify:

```bash
# Linux
./isaaclab.sh --help

# Windows
.\isaaclab.bat --help
```

> ℹ️ Isaac Lab requires the same Python 3.11 virtual environment as Isaac Sim. Activate it before running the install script.

---

## Useful Commands

| Action | Linux | Windows |
|--------|-------|---------|
| Launch full GUI | `./isaac-sim.sh` | `.\isaac-sim.bat` |
| Launch headless | `./isaac-sim.sh --headless` | `.\isaac-sim.bat --headless` |
| Reset user config | `./isaac-sim.sh --reset-user` | `.\isaac-sim.bat --reset-user` |
| Warmup shader cache | `./warmup.sh` | `.\warmup.bat` |
| Run Python script | `./python.sh my_script.py` | `.\python.bat my_script.py` |
| Compatibility check | `./isaac-sim.compatibility_check.sh` | `.\isaac-sim.compatibility_check.bat` |

---

## Default Installation Paths

| Platform | Method | Default Path |
|----------|--------|-------------|
| Linux | pip | `~/env_isaacsim/` |
| Linux | Binary | `~/.local/share/ov/pkg/isaac-sim-5.1.0/` |
| Windows | pip | `C:\isaacsim\env_isaacsim\` |
| Windows | Binary | `C:\Users\<user>\AppData\Local\ov\pkg\isaac-sim-5.1.0\` |

---

## Troubleshooting

### Isaac Sim crashes immediately on first launch

**Cause:** Shader cache not yet built.  
**Fix:** Run the warmup script first:

```bash
# Linux
./warmup.sh

# Windows
.\warmup.bat
```

---

### `ModuleNotFoundError: No module named 'isaacsim'`

**Cause:** Virtual environment not activated.  
**Fix:**

```bash
# Linux
source ~/env_isaacsim/bin/activate

# Windows
C:\isaacsim\env_isaacsim\Scripts\Activate.ps1
```

---

### `OSError: [Errno 36] File name too long` (Windows)

**Cause:** Long path support not enabled.  
**Fix:** Follow [Step 3 — Enable Long Path Support](#step-3--enable-long-path-support-windows) above and retry.

---

### `GLIBC_2.35 not found` (Ubuntu 20.04)

**Cause:** Ubuntu 20.04 ships with GLIBC 2.31, below the 2.35 minimum for pip install.  
**Fix:** Use the **binary workstation** installation method instead, or upgrade to Ubuntu 22.04.

---

### Black screen / no rendering after launch

**Cause:** GPU driver too old, or RTX features disabled.  
**Fix:**

```bash
# Linux — verify driver
nvidia-smi
# Update to 580.65.06+ if needed
```

Ensure you're not running on an integrated GPU. On laptops:

```bash
# Linux — force NVIDIA GPU
__NV_PRIME_RENDER_OFFLOAD=1 __GLX_VENDOR_LIBRARY_NAME=nvidia ./isaac-sim.sh
```

---

### `pip install` hangs or is very slow

**Cause:** Large package downloads (~10 GB total).  
**Fix:** Be patient. Use a wired connection. You can also pre-warm extensions after install:

```bash
isaacsim isaacsim.exp.full.kit --/app/quitAfter=120
```

---

### GPU not recognized as RTX / RT Cores error

**Cause:** A100/H100 data-center GPUs lack RT Cores and are unsupported.  
**Cause:** GPU driver mismatch.  
**Fix:** Only GeForce RTX / Quadro RTX / RTX Ada series GPUs are supported. Verify with `nvidia-smi` that the correct GPU is being used.

---

### Isaac Sim on Ubuntu 24.04 closes immediately

**Cause:** GCC version mismatch for source builds.  
**Fix:**

```bash
sudo apt install gcc-11 g++-11
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 200
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 200
```

---

## Additional Resources

- [Isaac Sim Official Documentation](https://docs.isaacsim.omniverse.nvidia.com/)
- [Isaac Sim GitHub Repository](https://github.com/isaac-sim/IsaacSim)
- [Isaac Lab Documentation](https://isaac-sim.github.io/IsaacLab/)
- [NVIDIA Omniverse Technical Requirements](https://docs.omniverse.nvidia.com/tech-requirements/tech-requirements/overview.html)
- [NVIDIA Developer Forums — Isaac Sim](https://forums.developer.nvidia.com/c/isaac/isaac-sim/)
- [NVIDIA Unix Driver Archive](https://www.nvidia.com/en-us/drivers/unix/)
- [Isaac Sim PyPI (NVIDIA)](https://pypi.nvidia.com/)

---

*Guide written for Isaac Sim 5.1.0 — Ubuntu 22.04 LTS & Windows 11 by BENJABBAR Adam . Last updated: May 2026.*
