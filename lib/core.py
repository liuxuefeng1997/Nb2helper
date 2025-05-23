import ctypes
import logging
from ctypes import wintypes

# ------------------- 常量定义 -------------------

PROCESS_ALL_ACCESS = 0x1F0FFF
PROCESS_QUERY_INFORMATION = 0x0400
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
PROCESS_VM_READ = 0x0010
PROCESS_VM_WRITE = 0x0020
PROCESS_VM_OPERATION = 0x0008
MAX_PATH = 260
LIST_MODULES_ALL = 0x03
TH32CS_SNAPPROCESS = 0x00000002


# ------------------- 结构体定义 -------------------
class MEMORY_BASIC_INFORMATION(ctypes.Structure):
    _fields_ = [
        ("BaseAddress", wintypes.LPVOID),
        ("AllocationBase", wintypes.LPVOID),
        ("AllocationProtect", wintypes.DWORD),
        ("PartitionId", wintypes.WORD),
        ("RegionSize", ctypes.c_size_t),
        ("State", wintypes.DWORD),
        ("Protect", wintypes.DWORD),
        ("Type", wintypes.DWORD),
    ]


class SYSTEM_INFO(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ("wProcessorArchitecture", wintypes.WORD),
        ("wReserved", wintypes.WORD),
        ("dwPageSize", wintypes.DWORD),
        ("lpMinimumApplicationAddress", wintypes.LPVOID),
        ("lpMaximumApplicationAddress", wintypes.LPVOID),
        ("dwActiveProcessorMask", wintypes.LPVOID),
        ("dwNumberOfProcessors", wintypes.DWORD),
        ("dwProcessorType", wintypes.DWORD),
        ("dwAllocationGranularity", wintypes.DWORD),
        ("wProcessorLevel", wintypes.WORD),
        ("wProcessorRevision", wintypes.WORD),
    ]


class PROCESSENTRY32(ctypes.Structure):
    _fields_ = [
        ("dwSize", wintypes.DWORD),
        ("cntUsage", wintypes.DWORD),
        ("th32ProcessID", wintypes.DWORD),
        ("th32DefaultHeapID", ctypes.POINTER(wintypes.ULONG)),
        ("th32ModuleID", wintypes.DWORD),
        ("cntThreads", wintypes.DWORD),
        ("th32ParentProcessID", wintypes.DWORD),
        ("pcPriClassBase", wintypes.LONG),
        ("dwFlags", wintypes.DWORD),
        ("szExeFile", ctypes.c_char * MAX_PATH)
    ]


# ------------------- 函数声明 -------------------
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
psapi = ctypes.WinDLL('psapi', use_last_error=True)

# OpenProcess
kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
kernel32.OpenProcess.restype = wintypes.HANDLE

# Read/WriteProcessMemory
kernel32.ReadProcessMemory.argtypes = [wintypes.HANDLE, wintypes.LPCVOID, wintypes.LPVOID, ctypes.c_size_t,
                                       ctypes.POINTER(ctypes.c_size_t)]
kernel32.ReadProcessMemory.restype = wintypes.BOOL
kernel32.WriteProcessMemory.argtypes = [wintypes.HANDLE, wintypes.LPVOID, wintypes.LPCVOID, ctypes.c_size_t,
                                        ctypes.POINTER(ctypes.c_size_t)]
kernel32.WriteProcessMemory.restype = wintypes.BOOL

# EnumProcessModulesEx
psapi.EnumProcessModulesEx.argtypes = [
    wintypes.HANDLE,
    ctypes.POINTER(wintypes.HMODULE),
    wintypes.DWORD,
    ctypes.POINTER(wintypes.DWORD),
    wintypes.DWORD
]
psapi.EnumProcessModulesEx.restype = wintypes.BOOL

# GetModuleBaseNameW
psapi.GetModuleBaseNameW.argtypes = [
    wintypes.HANDLE, wintypes.HMODULE, wintypes.LPWSTR, wintypes.DWORD
]
psapi.GetModuleBaseNameW.restype = wintypes.DWORD

# IsWow64Process
kernel32.IsWow64Process.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.BOOL)]
kernel32.IsWow64Process.restype = wintypes.BOOL

# VirtualQueryEx
kernel32.VirtualQueryEx.argtypes = [
    wintypes.HANDLE, wintypes.LPCVOID,
    ctypes.POINTER(MEMORY_BASIC_INFORMATION), ctypes.c_size_t
]
kernel32.VirtualQueryEx.restype = ctypes.c_size_t

# CreateToolhelp32Snapshot
kernel32.CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
kernel32.CreateToolhelp32Snapshot.restype = wintypes.HANDLE

# Process32First
kernel32.Process32First.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32)]
kernel32.Process32First.restype = wintypes.BOOL

# Process32Next
kernel32.Process32Next.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32)]
kernel32.Process32Next.restype = wintypes.BOOL

# CloseHandle
kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
kernel32.CloseHandle.restype = wintypes.BOOL


# ------------------- 功能函数 -------------------
def get_module_base(pid, target_dll):
    """获取DLL模块基址"""
    h_process = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
    if not h_process:
        raise ctypes.WinError(ctypes.get_last_error())

    try:
        h_modules = (wintypes.HMODULE * 1024)()
        cb_needed = wintypes.DWORD()
        if not psapi.EnumProcessModulesEx(
                h_process,
                h_modules,
                ctypes.sizeof(h_modules),
                ctypes.byref(cb_needed),
                LIST_MODULES_ALL
        ):
            raise ctypes.WinError(ctypes.get_last_error())

        module_count = cb_needed.value // ctypes.sizeof(wintypes.HMODULE)
        for i in range(module_count):
            h_module = h_modules[i]
            base_name = ctypes.create_unicode_buffer(MAX_PATH)
            psapi.GetModuleBaseNameW(h_process, h_module, base_name, MAX_PATH)
            if base_name.value.lower() == target_dll.lower():
                return h_module
        logging.debug(f"模块未找到: {target_dll}")
    finally:
        kernel32.CloseHandle(h_process)


def is_64bit_process(pid):
    """判断进程位数"""
    system_info = SYSTEM_INFO()
    kernel32.GetNativeSystemInfo(ctypes.byref(system_info))

    h_process = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not h_process:
        raise ctypes.WinError(ctypes.get_last_error())

    try:
        is_wow64 = wintypes.BOOL()
        if not kernel32.IsWow64Process(h_process, ctypes.byref(is_wow64)):
            raise ctypes.WinError(ctypes.get_last_error())

        return system_info.wProcessorArchitecture == 9 and not is_wow64.value
    finally:
        kernel32.CloseHandle(h_process)


def read_memory(pid, address, size):
    """安全内存读取"""
    h_process = kernel32.OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, False, pid)
    if not h_process:
        raise ctypes.WinError(ctypes.get_last_error())

    try:
        mbi = MEMORY_BASIC_INFORMATION()
        if kernel32.VirtualQueryEx(h_process, address, ctypes.byref(mbi), ctypes.sizeof(mbi)) == 0:
            raise ctypes.WinError(ctypes.get_last_error())

        if mbi.Protect & 0xFF in [0, 1, 0x10]:
            raise logging.error(f"地址 0x{address: X} 不可读")

        buffer = ctypes.create_string_buffer(size)
        bytes_read = ctypes.c_size_t()
        if kernel32.ReadProcessMemory(h_process, address, buffer, size, ctypes.byref(bytes_read)):
            return buffer.raw[:bytes_read.value]
        else:
            raise ctypes.WinError(ctypes.get_last_error())
    finally:
        kernel32.CloseHandle(h_process)


def write_memory(pid, address, data):
    """写入内存"""
    h_process = kernel32.OpenProcess(PROCESS_VM_WRITE | PROCESS_VM_OPERATION, False, pid)
    if not h_process:
        raise ctypes.WinError(ctypes.get_last_error())

    try:
        buffer = ctypes.create_string_buffer(data)
        bytes_written = ctypes.c_size_t()
        if kernel32.WriteProcessMemory(h_process, address, buffer, len(data), ctypes.byref(bytes_written)):
            return bytes_written.value
        else:
            raise ctypes.WinError(ctypes.get_last_error())
    finally:
        kernel32.CloseHandle(h_process)


def read_pointer_chain(pid, base_address, offsets):
    """读取指针链"""
    current_address = base_address
    ptr_size = 8 if is_64bit_process(pid) else 4

    for idx, offset in enumerate(offsets):
        try:
            data = read_memory(pid, current_address, ptr_size)
            current_address = int.from_bytes(data, 'little') + offset
            # print(f"[调试] 层级 {idx + 1}: 0x{current_address:X} (偏移 +0x{offset:X})")
        except Exception as e:
            logging.debug(f"偏移链解析失败于层级 {idx + 1}: {str(e)}")
            raise RuntimeWarning(f"偏移链解析失败于层级 {idx + 1}: {str(e)}")
    return current_address
