# CUDA Installation Guide
### Ubuntu (22.04 / 24.04) & Windows 11

> **CUDA (Compute Unified Device Architecture)** is NVIDIA's parallel computing platform that unlocks GPU acceleration for deep learning, robotics simulation, scientific computing, and more. This guide covers a full install of the **CUDA Toolkit**, **cuDNN**, and a verification with **PyTorch** — on both Ubuntu and Windows 11.

---

## Table of Contents

- [What Is the CUDA Stack?](#what-is-the-cuda-stack)
- [System Requirements](#system-requirements)
- [Version Compatibility Matrix](#version-compatibility-matrix)
- [Pre-Installation Checklist](#pre-installation-checklist)
- [Ubuntu Installation](#ubuntu-installation)
  - [Step 1 — Verify GPU](#step-1--verify-gpu-ubuntu)
  - [Step 2 — Install NVIDIA Driver](#step-2--install-nvidia-driver-ubuntu)
  - [Step 3 — Install CUDA Toolkit](#step-3--install-cuda-toolkit-ubuntu)
  - [Step 4 — Set Environment Variables](#step-4--set-environment-variables-ubuntu)
  - [Step 5 — Install cuDNN](#step-5--install-cudnn-ubuntu)
  - [Step 6 — Verify the Full Stack](#step-6--verify-the-full-stack-ubuntu)
- [Windows 11 Installation](#windows-11-installation)
  - [Step 1 — Verify GPU](#step-1--verify-gpu-windows)
  - [Step 2 — Install NVIDIA Driver](#step-2--install-nvidia-driver-windows)
  - [Step 3 — Install Visual Studio Build Tools](#step-3--install-visual-studio-build-tools-windows)
  - [Step 4 — Install CUDA Toolkit](#step-4--install-cuda-toolkit-windows)
  - [Step 5 — Install cuDNN](#step-5--install-cudnn-windows)
  - [Step 6 — Verify the Full Stack](#step-6--verify-the-full-stack-windows)
- [WSL2 — CUDA on Windows via Linux](#wsl2--cuda-on-windows-via-linux)
- [Install PyTorch with CUDA](#install-pytorch-with-cuda)
- [Managing Multiple CUDA Versions](#managing-multiple-cuda-versions)
- [Default Installation Paths](#default-installation-paths)
- [Troubleshooting](#troubleshooting)
- [Additional Resources](#additional-resources)

---

## What Is the CUDA Stack?

CUDA is not a single install — it is a layered stack. Install in this exact order:

```
┌─────────────────────────────────────┐
│  Framework  (PyTorch / TensorFlow)  │  ← Python packages
├─────────────────────────────────────┤
│  cuDNN                              │  ← Deep learning primitives
├─────────────────────────────────────┤
│  CUDA Toolkit  (nvcc, libs)         │  ← Compiler + runtime
├─────────────────────────────────────┤
│  NVIDIA GPU Driver                  │  ← Kernel-level GPU interface
├─────────────────────────────────────┤
│  GPU Hardware                       │
└─────────────────────────────────────┘
```

Each layer must be compatible with the one below it. A mismatch at any level is the most common cause of CUDA failures.

---

## System Requirements

| Component | Minimum | Notes |
|-----------|---------|-------|
| **GPU** | NVIDIA GPU with CUDA compute capability ≥ 5.0 | Check [CUDA GPU list](https://developer.nvidia.com/cuda-gpus) |
| **OS (Linux)** | Ubuntu 22.04 LTS or 24.04 LTS | Ubuntu 20.04 is EOL (May 2025) |
| **OS (Windows)** | Windows 11 | Windows 10 support dropped in late 2025 |
| **RAM** | 8 GB | 16 GB+ recommended for ML workloads |
| **Storage** | 5 GB free | More for samples and frameworks |
| **Internet** | Required | Driver and package downloads |

---

## Version Compatibility Matrix

> ⚠️ Version mismatches are the #1 source of CUDA problems. Always confirm compatibility before installing.

### CUDA ↔ Driver minimum version

| CUDA Version | Min Driver (Linux) | Min Driver (Windows) |
|-------------|-------------------|---------------------|
| **CUDA 13.x** | 575.xx+ | 576.xx+ |
| **CUDA 12.8** | 570.xx+ | 572.xx+ |
| **CUDA 12.6** | 560.28.03+ | 560.76+ |
| **CUDA 12.4** | 550.54.14+ | 551.61+ |
| **CUDA 12.1** | 530.30.02+ | 531.14+ |
| **CUDA 11.8** | 520.61.05+ | 522.06+ |

### CUDA ↔ cuDNN compatibility

| CUDA Version | Compatible cuDNN |
|-------------|-----------------|
| CUDA 12.x | cuDNN 9.x |
| CUDA 12.1 | cuDNN 8.9+ |
| CUDA 11.8 | cuDNN 8.6 – 8.9 |

### CUDA ↔ GPU architecture

| GPU Architecture | Supported CUDA |
|-----------------|---------------|
| RTX 50 series (Blackwell) | CUDA 12.8+ |
| RTX 40 series (Ada) | CUDA 11.8+ |
| RTX 30 series (Ampere) | CUDA 11.1+ |
| RTX 20 / GTX 16 series (Turing) | CUDA 10.0+ |
| GTX 10 series (Pascal) | CUDA 8.0+ (use CUDA 12.x for current frameworks) |

> **Maxwell and Pascal** are not supported by CUDA 13.x. Use CUDA 12.x for those architectures.

### CUDA ↔ Visual Studio (Windows only)

| CUDA Version | Supported Visual Studio |
|-------------|------------------------|
| CUDA 12.9+ | VS 2019, VS 2022 |
| CUDA 12.5–12.8 | VS 2019, VS 2022 |
| CUDA 12.0–12.4 | VS 2019, VS 2022 |
| CUDA 11.8 | VS 2019, VS 2022 |

---

## Pre-Installation Checklist

Before starting, confirm:

- [ ] NVIDIA GPU present in the system
- [ ] GPU is [CUDA-capable](https://developer.nvidia.com/cuda-gpus)
- [ ] Virtualization / Secure Boot won't interfere (most desktop systems are fine)
- [ ] No conflicting old CUDA installation (or you plan to remove it first)
- [ ] Stable internet connection

---

## Ubuntu Installation

### Step 1 — Verify GPU (Ubuntu)

```bash
# Check if an NVIDIA GPU is detected by the system
lspci | grep -i nvidia
```

Expected output example:
```
01:00.0 VGA compatible controller: NVIDIA Corporation GA106 [GeForce RTX 3060]
```

No output means the GPU is either not installed, not detected, or not an NVIDIA card.

---

### Step 2 — Install NVIDIA Driver (Ubuntu)

**Check what's currently installed:**

```bash
nvidia-smi
```

If no driver is found, or the version is below the minimum for your target CUDA version:

```bash
# Add the graphics PPA
sudo add-apt-repository ppa:graphics-drivers/ppa
sudo apt update

# Install the recommended production driver (adjust version as needed)
sudo apt install nvidia-driver-570

# Reboot to load the new driver
sudo reboot
```

After reboot, verify:

```bash
nvidia-smi
```

Example output:
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 570.xx    Driver Version: 570.xx    CUDA Version: 12.8          |
+-----------------------------------------------------------------------------+
| GPU 0: NVIDIA GeForce RTX 3060 ...                                          |
```

> ℹ️ The `CUDA Version` shown by `nvidia-smi` is the **maximum CUDA version your driver supports**, not the installed toolkit version. These are two different things.

---

### Step 3 — Install CUDA Toolkit (Ubuntu)

**Method A — Network repository (recommended, always up to date):**

```bash
# Download and install the CUDA keyring for your Ubuntu version
# Ubuntu 22.04:
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb
# Ubuntu 24.04:
# wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb

sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update

# Install a specific version (recommended — pin the version)
sudo apt install cuda-toolkit-12-6

# Or install the latest available:
# sudo apt install cuda-toolkit
```

**Method B — Local .deb installer (offline-friendly):**

1. Go to [https://developer.nvidia.com/cuda-downloads](https://developer.nvidia.com/cuda-downloads)
2. Select: Linux → x86_64 → Ubuntu → your version → `deb (local)`
3. Follow the commands shown on the download page

**Method C — `.run` file (version-agnostic, best for new GPUs):**

```bash
# Download the runfile from https://developer.nvidia.com/cuda-downloads
# Select: Linux → x86_64 → Ubuntu → runfile (local)
chmod +x cuda_12.6.x_linux.run
sudo ./cuda_12.6.x_linux.run
```

> ⚠️ With the `.run` installer, **uncheck the driver** if you already installed it separately to avoid conflicts.

---

### Step 4 — Set Environment Variables (Ubuntu)

Add CUDA to your shell profile. For `bash`:

```bash
echo '' >> ~/.bashrc
echo '# CUDA Toolkit' >> ~/.bashrc
echo 'export PATH=/usr/local/cuda-12.6/bin${PATH:+:${PATH}}' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.6/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}' >> ~/.bashrc

source ~/.bashrc
```

For `zsh`, replace `~/.bashrc` with `~/.zshrc`.

> 💡 `/usr/local/cuda` is a symlink that points to the active CUDA version. You can use it instead of the versioned path for a more future-proof setup:
> ```bash
> export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}
> export LD_LIBRARY_PATH=/usr/local/cuda/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
> ```

**Verify the compiler is accessible:**

```bash
nvcc --version
```

Expected:
```
nvcc: NVIDIA (R) Cuda compiler driver
Cuda compilation tools, release 12.6, V12.6.xx
```

---

### Step 5 — Install cuDNN (Ubuntu)

cuDNN requires a **free NVIDIA Developer account** to download.

**Via apt (easiest, after adding the CUDA repo):**

```bash
# For CUDA 12.x — installs cuDNN 9
sudo apt install libcudnn9-cuda-12 libcudnn9-dev-cuda-12

# Verify
dpkg -l | grep cudnn
```

**Via local .deb (from developer.nvidia.com/cudnn):**

```bash
# Download the .deb package for your Ubuntu version from the cuDNN download page
sudo dpkg -i cudnn-local-repo-ubuntu2204-9.x.x.x_1.0-1_amd64.deb
sudo cp /var/cudnn-local-repo-ubuntu2204-9.x.x.x/cudnn-*-keyring.gpg /usr/share/keyrings/
sudo apt update
sudo apt install libcudnn9 libcudnn9-dev
```

---

### Step 6 — Verify the Full Stack (Ubuntu)

**Verify nvcc:**

```bash
nvcc --version
```

**Run the CUDA device query sample:**

```bash
# Clone the CUDA samples repository
git clone https://github.com/NVIDIA/cuda-samples.git
cd cuda-samples/Samples/1_Utilities/deviceQuery
make
./deviceQuery
```

Expected last line:
```
Result = PASS
```

**Quick Python check (after installing PyTorch — see below):**

```python
import torch
print(torch.cuda.is_available())       # True
print(torch.cuda.device_count())       # 1 (or more)
print(torch.cuda.get_device_name(0))   # NVIDIA GeForce RTX XXXX
print(torch.version.cuda)             # 12.6
```

---

## Windows 11 Installation

### Step 1 — Verify GPU (Windows)

Open **PowerShell** or **Command Prompt**:

```powershell
# Check for NVIDIA GPU
wmic path win32_VideoController get name
```

Or open **Device Manager** → **Display adapters** and confirm an NVIDIA GPU is listed.

---

### Step 2 — Install NVIDIA Driver (Windows)

1. Open **Device Manager** → note your exact GPU model
2. Go to [https://www.nvidia.com/drivers](https://www.nvidia.com/drivers)
3. Search for your GPU and download the latest **Game Ready** or **Studio** driver (≥ minimum version for your target CUDA)
4. Run the installer → choose **Custom Install** → check **Clean Installation**
5. Reboot

Verify in PowerShell:

```powershell
nvidia-smi
```

---

### Step 3 — Install Visual Studio Build Tools (Windows)

CUDA on Windows requires the **MSVC C++ compiler**. Install Visual Studio 2022 Build Tools (free):

1. Download from [https://visualstudio.microsoft.com/downloads/](https://visualstudio.microsoft.com/downloads/) → **Build Tools for Visual Studio 2022**
2. In the installer, select the **"Desktop development with C++"** workload
3. Complete the installation

> ℹ️ If you only need PyTorch/TensorFlow (not compiling custom CUDA kernels), you can skip this step.

---

### Step 4 — Install CUDA Toolkit (Windows)

1. Go to [https://developer.nvidia.com/cuda-downloads](https://developer.nvidia.com/cuda-downloads)
2. Select: **Windows → x86_64 → Windows 11 → exe (local)**
3. Download the installer (`cuda_12.6.x_windows.exe`, ~3 GB)
4. Run the installer and select components:

| Component | Include? |
|-----------|---------|
| CUDA Toolkit | ✅ Always |
| CUDA Visual Studio Integration | ✅ If you installed VS |
| NVIDIA GeForce Experience | Optional |
| NVIDIA Display Driver | ⚠️ Only if not already installed separately |

5. Complete the installation and **reboot**

**Verify in PowerShell:**

```powershell
nvcc --version
```

Expected:
```
Cuda compilation tools, release 12.6, V12.6.xx
```

If `nvcc` is not found, add it manually to your PATH:

```powershell
# Add to system PATH (run as Admin)
[System.Environment]::SetEnvironmentVariable(
  "PATH",
  $env:PATH + ";C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\bin",
  "Machine"
)
```

Then open a **new** PowerShell window and retry `nvcc --version`.

---

### Step 5 — Install cuDNN (Windows)

1. Go to [https://developer.nvidia.com/cudnn](https://developer.nvidia.com/cudnn) (free NVIDIA account required)
2. Download **cuDNN 9.x for CUDA 12.x** → Windows x86_64 → zip
3. Extract the zip — you'll get three folders: `bin`, `include`, `lib`
4. Copy files into the CUDA Toolkit directory:

```
bin\       → C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\bin\
include\   → C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\include\
lib\x64\   → C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\lib\x64\
```

5. Add cuDNN bin to PATH (if not already covered):

```powershell
[System.Environment]::SetEnvironmentVariable(
  "PATH",
  $env:PATH + ";C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\bin",
  "Machine"
)
```

**Verify:**

```powershell
where cudnn64_9.dll
# Should output: C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\bin\cudnn64_9.dll
```

---

### Step 6 — Verify the Full Stack (Windows)

**Run deviceQuery:**

```powershell
# Clone CUDA samples
git clone https://github.com/NVIDIA/cuda-samples.git
cd cuda-samples\Samples\1_Utilities\deviceQuery

# Build with VS 2022 (open the .sln file in Visual Studio, or use MSBuild)
msbuild deviceQuery_vs2022.sln /p:Configuration=Release /p:Platform=x64

# Run
.\x64\Release\deviceQuery.exe
```

Expected last line:
```
Result = PASS
```

**Quick PowerShell check:**

```powershell
# Check CUDA driver visibility
nvidia-smi

# Check compiler
nvcc --version
```

---

## WSL2 — CUDA on Windows via Linux

If you use WSL2 (Windows Subsystem for Linux), the setup is different and simpler:

> ✅ **WSL2 uses the Windows NVIDIA driver directly** — do NOT install a Linux driver inside WSL2. Only install the CUDA Toolkit (without the driver).

```bash
# Inside your WSL2 Ubuntu terminal:

# Add the WSL-Ubuntu specific CUDA repo
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt update
sudo apt install cuda-toolkit-12-6

# Set environment variables (same as native Ubuntu)
echo 'export PATH=/usr/local/cuda-12.6/bin${PATH:+:${PATH}}' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-12.6/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}' >> ~/.bashrc
source ~/.bashrc

# Verify
nvcc --version
nvidia-smi  # This reads through the Windows driver
```

> ⚠️ Select **WSL-Ubuntu** (not Ubuntu) as the distribution on the CUDA download page for the best compatibility.

---

## Install PyTorch with CUDA

After the CUDA stack is set up, install PyTorch with the matching CUDA build:

```bash
# CUDA 12.8 (latest, recommended for RTX 40/50 series)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

# CUDA 12.6
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126

# CUDA 12.4
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# CUDA 11.8 (legacy GPUs)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Verify PyTorch sees your GPU:**

```python
import torch

print("CUDA available:", torch.cuda.is_available())
print("GPU count:     ", torch.cuda.device_count())
print("GPU name:      ", torch.cuda.get_device_name(0))
print("CUDA version:  ", torch.version.cuda)
```

All four lines should return sensible values. If `torch.cuda.is_available()` returns `False`, see [Troubleshooting](#troubleshooting).

---

## Managing Multiple CUDA Versions

It is possible to have multiple CUDA versions installed simultaneously. Use symlinks or environment variables to switch between them.

### Linux — switching with symlinks

```bash
# List installed CUDA versions
ls /usr/local/ | grep cuda

# Switch active version (update the symlink)
sudo ln -sfn /usr/local/cuda-12.4 /usr/local/cuda

# Or set per-session via environment variable
export PATH=/usr/local/cuda-11.8/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:$LD_LIBRARY_PATH
```

### Linux — switching with conda environments

```bash
# Create a conda environment pinned to a specific CUDA version
conda create -n cuda11 python=3.10
conda activate cuda11
conda install cuda -c nvidia/label/cuda-11.8.0

conda create -n cuda12 python=3.11
conda activate cuda12
conda install cuda -c nvidia/label/cuda-12.6.0
```

### Windows — switching via PATH order

Windows resolves `nvcc` from the first matching entry in `PATH`. To switch:

1. Open **System Properties → Environment Variables → System Variables → Path**
2. Move the desired CUDA version's `bin` entry to the **top** of the list
3. Open a new terminal and verify with `nvcc --version`

---

## Default Installation Paths

| Platform | Component | Default Path |
|----------|-----------|-------------|
| Linux | CUDA Toolkit | `/usr/local/cuda-12.6/` |
| Linux | Active symlink | `/usr/local/cuda/` |
| Linux | cuDNN headers | `/usr/local/cuda/include/cudnn*.h` |
| Linux | cuDNN libs | `/usr/local/cuda/lib64/libcudnn*` |
| Windows | CUDA Toolkit | `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\` |
| Windows | cuDNN (after copy) | `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\bin\` |

---

## Troubleshooting

### `nvcc: command not found` after install

**Cause:** CUDA `bin` directory not in `PATH`.

```bash
# Linux — check if CUDA bin is in PATH
echo $PATH | grep cuda

# Fix — add to ~/.bashrc
echo 'export PATH=/usr/local/cuda/bin${PATH:+:${PATH}}' >> ~/.bashrc
source ~/.bashrc
```

On Windows, verify `C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v12.6\bin` is in System PATH, then open a new terminal.

---

### `nvidia-smi` works but `nvcc` says "command not found"

**Cause:** The NVIDIA driver is installed, but the **CUDA Toolkit** (separate package) is not.
**Fix:** Follow Step 3 (Install CUDA Toolkit) — the driver and toolkit are different packages.

---

### `torch.cuda.is_available()` returns `False`

Most likely causes:

1. **CPU-only PyTorch** was installed — reinstall with the correct `--index-url`:
   ```bash
   pip uninstall torch torchvision torchaudio
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126
   ```

2. **PyTorch CUDA version ≠ installed toolkit** — check:
   ```python
   import torch
   print(torch.version.cuda)   # PyTorch's CUDA
   # Compare with: nvcc --version
   ```

3. **Driver too old** — run `nvidia-smi` and compare the driver version against the matrix above.

---

### Version mismatch: `nvcc` reports different version than `nvidia-smi`

This is **expected and normal**. `nvidia-smi` shows the maximum CUDA version your driver *supports*. `nvcc` shows the *installed toolkit* version. As long as the toolkit version ≤ the driver's max version, you're fine.

---

### `CUDA error: no kernel image is available for execution on the device`

**Cause:** PyTorch was compiled against a different CUDA compute capability than your GPU.
**Fix:** Reinstall PyTorch with the wheel matching your CUDA version, or build from source targeting your GPU's `sm_xx`.

---

### CUDA install fails or hangs on Windows — "Windows Update is running"

**Cause:** The CUDA installer conflicts with an active Windows Update.
**Fix:** Wait for Windows Update to finish, reboot, then rerun the installer.

---

### `libcuda.so.1: cannot open shared object file` (Linux)

**Cause:** `LD_LIBRARY_PATH` not set, or pointing to wrong path.

```bash
# Check where libcuda lives
find /usr -name 'libcuda.so*' 2>/dev/null

# Add the correct path
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
```

---

### Multiple CUDA versions conflict (CMake picks wrong one)

```bash
# Tell CMake explicitly where to find your target CUDA
cmake .. -DCMAKE_CUDA_COMPILER=/usr/local/cuda-12.6/bin/nvcc \
         -DCUDA_TOOLKIT_ROOT_DIR=/usr/local/cuda-12.6
```

---

### WSL2 — `nvidia-smi` not found inside WSL

**Cause:** On WSL2, `nvidia-smi` is in `/usr/lib/wsl/lib/`, not on PATH by default.

```bash
echo 'export PATH=$PATH:/usr/lib/wsl/lib' >> ~/.bashrc
source ~/.bashrc
nvidia-smi
```

---

## Additional Resources

- [NVIDIA CUDA Downloads](https://developer.nvidia.com/cuda-downloads)
- [CUDA Toolkit Archive (all versions)](https://developer.nvidia.com/cuda-toolkit-archive)
- [NVIDIA cuDNN Downloads](https://developer.nvidia.com/cudnn)
- [CUDA GPU Compatibility List](https://developer.nvidia.com/cuda-gpus)
- [CUDA Installation Guide — Linux (official)](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/)
- [CUDA Installation Guide — Windows (official)](https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows/)
- [PyTorch — Get Started (version selector)](https://pytorch.org/get-started/locally/)
- [NVIDIA CUDA Samples (GitHub)](https://github.com/NVIDIA/cuda-samples)

---

*Guide written for CUDA 12.x / 13.x — Ubuntu 22.04 / 24.04 & Windows 11. Last updated: May 2026.*
