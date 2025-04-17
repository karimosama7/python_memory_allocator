# Memory Allocator Project

## Team Members
1. Ahmed Hussein Al-Ahmady
2. Ahmed Abdel-Halim Abdel-Halim Al-Ashmawi
3. Al-Zahraa El-Sayed Mohamed Mohamed Salem
4. Ola Tarek Nasr Gohar
5. Karim Osama Bayoumi Saleh

## Overview

This project implements a contiguous memory allocation system in Python. The system manages a contiguous region of memory and allows for dynamic memory allocation and deallocation using different allocation strategies. It simulates how operating systems handle memory management.

## Features

- **Memory Allocation**: Allocate memory blocks to processes using three different strategies:
  - First Fit (`F`): Allocates the first free block that is large enough
  - Best Fit (`B`): Allocates the smallest free block that is large enough
  - Worst Fit (`W`): Allocates the largest free block available

- **Memory Release**: Free memory allocated to specific processes

- **Memory Compaction**: Consolidate fragmented free memory blocks into a single contiguous block

- **Status Reporting**: Display the current state of memory, showing allocated and free regions

## Usage

### Running the Program

```bash
python memory_allocator.py
```

The program initializes with 1MB (1,048,576 bytes) of memory by default.

### Commands

| Command | Format | Description |
|---------|--------|-------------|
| RQ | `RQ <process_id> <memory_size> <strategy>` | Request memory allocation |
| RL | `RL <process_id>` | Release memory allocated to a process |
| C  | `C` | Compact memory (defragmentation) |
| STAT | `STAT` | Show memory allocation status |
| X  | `X` | Exit the program |

### Strategy Flags
- `F` - First Fit
- `B` - Best Fit
- `W` - Worst Fit

### Example Session

```
allocator> RQ P1 200000 F
Allocated 200000 bytes to Process P1 at addresses [0:199999]

allocator> RQ P2 300000 F
Allocated 300000 bytes to Process P2 at addresses [200000:499999]

allocator> RQ P3 200000 F
Allocated 200000 bytes to Process P3 at addresses [500000:699999]

allocator> STAT
Addresses [0:199999] Process P1
Addresses [200000:499999] Process P2
Addresses [500000:699999] Process P3
Addresses [700000:1048575] Unused

allocator> RL P2
Released memory allocated to Process P2

allocator> STAT
Addresses [0:199999] Process P1
Addresses [200000:499999] Unused
Addresses [500000:699999] Process P3
Addresses [700000:1048575] Unused

allocator> RQ P4 400000 F
Error: Not enough contiguous memory for process P4 (350000 bytes).

allocator> C
Memory compaction completed.

allocator> STAT
Addresses [0:199999] Process P1
Addresses [200000:399999] Process P3
Addresses [400000:1048575] Unused

allocator> RQ P4 400000 F
Allocated 350000 bytes to Process P4 at addresses [400000:749999]

allocator> STAT
Addresses [0:199999] Process P1
Addresses [200000:399999] Process P3
Addresses [400000:749999] Process P4
Addresses [750000:1048575] Unused
```

## Implementation Details

The memory allocator uses a list to represent memory regions, where each entry contains:
- Status (Process ID or "Unused")
- Start address
- End address

The program handles several key memory management operations:

- **Memory Request**: When a process requests memory, the allocator finds an appropriate hole based on the selected strategy. If a hole is found, it's either completely allocated or split into an allocated part and a remaining unused part.

- **Memory Release**: When memory is released, the allocator marks the region as unused and attempts to merge adjacent unused regions.

- **Memory Compaction**: This operation moves all allocated blocks to the beginning of memory, combining all free space into a single block at the end, thus eliminating external fragmentation.

## External Fragmentation Demonstration

The example session above demonstrates external fragmentation:
1. After releasing Process P2, there are two separate unused memory blocks
2. Even though the total free memory is enough for Process P4 (400000 bytes), no single contiguous block is large enough
3. After compaction, the free memory is consolidated, allowing Process P4 to be allocated
