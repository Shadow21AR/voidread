---
title: "Enable AVX/AVX2 Support in Kali VM on VirtualBox"
description: "Enable AVX/AVX2 Support in Kali VM on VirtualBox"
date: 2025-06-21T10:00:00+05:30
categories:
  - virtualization
  - avx
  - kali
tags:
  - virtualbox
  - avx
  - linux
  - tensorflow
  - llm
---

# Enabling AVX/AVX2 in Kali Linux VM on VirtualBox (from Windows Host)

When running AVX-dependent binaries (like TensorFlow, LLMs, or `h5` models) inside a VirtualBox VM, you may hit:

```bash
Illegal instruction (core dumped)
```

This guide walks through how to **enable AVX and AVX2 passthrough** to a Kali Linux VM hosted on Windows using VirtualBox.

---

## Background

Modern machine learning and inference workloads often rely on CPU instructions like:

* AVX / AVX2
* FMA (Fused Multiply-Add)

By default, VirtualBox doesn't expose these instructions unless:

* VT-x is enabled on host and guest
* Certain settings are correctly applied

---

## Host Setup (Windows)

### 1. Check If VT-x Is Enabled in BIOS

Open Task Manager → **Performance > CPU**
→ Look for:

```
Virtualization: Enabled
```

If not, reboot your system and enable **Intel Virtualization (VT-x)** in BIOS/UEFI.

---

### 2. Disable Hyper-V & Conflicts

Open **Command Prompt (Admin)** and run:

```cmd
bcdedit /set hypervisorlaunchtype off
```

Then, open **PowerShell (Admin)** and run:

```powershell
Get-WindowsOptionalFeature -Online | Where-Object {$_.FeatureName -match "Hyper-V|Containers|VirtualMachinePlatform"} | Format-Table FeatureName, State
```

If `VirtualMachinePlatform` is enabled, disable it:

```powershell
Disable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform
```

Then reboot.

---

## VirtualBox Configuration

### 3. Use `VBoxManage` to Enable AVX

Open `cmd` and run:

```cmd
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" setextradata "kali-linux" VBoxInternal/CPUM/IsaExts/AVX 1
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" setextradata "kali-linux" VBoxInternal/CPUM/IsaExts/AVX2 1
```

(Replace `"kali-linux"` with your VM name)

Also enable nested virtualization explicitly:

```cmd
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" modifyvm "kali-linux" --nested-hw-virt on
```

---

### 4. VirtualBox VM Settings

In VirtualBox GUI → `kali-linux` → **Settings**:

#### System > Motherboard:

* ✅ Enable EFI (special OSes only)
* ✅ Enable PAE/NX
* ✅ Chipset: ICH9 or PIIX3

#### System > Processor:

* CPUs: 2 or more
* ✅ Enable Nested VT-x/AMD-V (should no longer be greyed out)

#### Acceleration:

* ✅ Enable VT-x/AMD-V
* ✅ Enable Nested Paging
* Paravirtualization: **KVM**

---

## Testing Inside Kali VM

Boot into Kali Linux and run:

```bash
grep -o -w 'avx\|avx2' /proc/cpuinfo | sort -u
```

✅ Expected output:

```
avx
avx2
```

Run your binary (e.g. TensorFlow or LLM inference):

```bash
python payload.py
```

Output should NOT crash, and you may see:

```
This TensorFlow binary is optimized to use available CPU instructions...
To enable the following instructions: AVX2 FMA...
```

---

## Success

AVX and AVX2 instructions are now working in your Kali VM. You're ready to run high-performance models or any AVX-tuned software from inside your virtual machine.

---

## Optional: Re-enable WSL2 or Hyper-V

If you need WSL2 or Docker later, re-enable:

```powershell
Enable-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform
```

Then reboot.

---

## Troubleshooting

* If "Nested VT-x" is greyed out:

  * Make sure `VirtualMachinePlatform` is disabled
  * Ensure VM is 64-bit
  * Use EFI boot
  * Remove IDE controllers

---