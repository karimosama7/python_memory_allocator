class MemoryAllocator:
    def __init__(self, size):
        self.MAX = size
        self.memory = [
            ("Unused", 0, size - 1)
        ]  # Format: (status, start_address, end_address)

    def request_memory(self, process_id, size, strategy="F"):
        """
        Allocate memory to a process using specified strategy
        F - First fit
        B - Best fit
        W - Worst fit
        """
        if size <= 0:
            return f"Error: Invalid size. Size must be positive."

        # Find all unused memory blocks
        unused_blocks = []
        for i, block in enumerate(self.memory):
            if block[0] == "Unused":
                block_size = block[2] - block[1] + 1
                if block_size >= size:
                    unused_blocks.append((i, block_size))

        if not unused_blocks:
            return f"Error: Not enough contiguous memory for process {process_id} ({size} bytes)."

        # Select a block based on strategy
        selected_index = None

        if strategy == "F":  # First fit
            selected_index = unused_blocks[0][0]

        elif strategy == "B":  # Best fit
            selected_index = min(unused_blocks, key=lambda x: x[1])[0]

        elif strategy == "W":  # Worst fit
            selected_index = max(unused_blocks, key=lambda x: x[1])[0]

        else:
            return f"Error: Invalid strategy '{strategy}'. Use F, B, or W."

        # Get the selected block
        start_address = self.memory[selected_index][1]
        end_address = self.memory[selected_index][2]
        block_size = end_address - start_address + 1

        # Allocate memory
        if block_size == size:
            # Perfect fit - replace the block
            self.memory[selected_index] = (
                f"Process {process_id}",
                start_address,
                end_address,
            )
        else:
            # Split the block
            self.memory[selected_index] = (
                f"Process {process_id}",
                start_address,
                start_address + size - 1,
            )
            self.memory.insert(
                selected_index + 1, ("Unused", start_address + size, end_address)
            )

        return f"Allocated {size} bytes to Process {process_id} at addresses [{start_address}:{start_address + size - 1}]"

    def release_memory(self, process_id):
        """Release memory allocated to the specified process"""
        process_blocks = []
        for i, block in enumerate(self.memory):
            if block[0] == f"Process {process_id}":
                process_blocks.append(i)

        if not process_blocks:
            return f"Error: No memory allocated to Process {process_id}."

        # Release blocks in reverse order to avoid index shifting issues
        for i in sorted(process_blocks, reverse=True):
            start_address = self.memory[i][1]
            end_address = self.memory[i][2]
            self.memory[i] = ("Unused", start_address, end_address)

        # Merge adjacent free blocks
        self.merge_adjacent_holes()

        return f"Released memory allocated to Process {process_id}"

    def merge_adjacent_holes(self):
        """Merge adjacent free memory blocks"""
        i = 0
        while i < len(self.memory) - 1:
            current = self.memory[i]
            next_block = self.memory[i + 1]

            if current[0] == "Unused" and next_block[0] == "Unused":
                # Merge the blocks
                merged = ("Unused", current[1], next_block[2])
                self.memory[i] = merged
                del self.memory[i + 1]
            else:
                i += 1

    def compact_memory(self):
        """Compact all unused memory holes into one block"""
        # Extract all allocated blocks
        allocated_blocks = []
        for block in self.memory:
            if block[0] != "Unused":
                allocated_blocks.append(block)

        if not allocated_blocks:
            return "No allocated memory to compact."

        # Calculate total allocated space
        total_allocated = sum(block[2] - block[1] + 1 for block in allocated_blocks)

        # Create a new memory layout
        new_memory = []
        current_address = 0

        # Add all allocated blocks sequentially
        for status, _, end in allocated_blocks:
            block_size = end - _ + 1
            new_memory.append(
                (status, current_address, current_address + block_size - 1)
            )
            current_address += block_size

        # Add the remaining space as a single unused block
        if current_address < self.MAX:
            new_memory.append(("Unused", current_address, self.MAX - 1))

        self.memory = new_memory
        return "Memory compaction completed."

    def status_report(self):
        """Report the regions of free and allocated memory"""
        report = []
        for status, start, end in self.memory:
            report.append(f"Addresses [{start}:{end}] {status}")

        return "\n".join(report)


def main():
    # Initialize with default memory size
    memory_size = 1048576  # 1MB default

    # Create the memory allocator
    allocator = MemoryAllocator(memory_size)

    print(f"Memory allocator initialized with {memory_size} bytes")

    while True:
        try:
            command = input("allocator> ").strip()

            if not command:
                continue

            parts = command.split()
            cmd = parts[0].upper()

            if cmd == "RQ":
                if len(parts) < 4:
                    print(
                        "Error: RQ command format: RQ <process_id> <memory_size> <strategy>"
                    )
                    continue

                process_id = parts[1]
                try:
                    size = int(parts[2])
                except ValueError:
                    print("Error: Memory size must be a positive integer")
                    continue

                strategy = parts[3].upper()
                if strategy not in ["F", "B", "W"]:
                    print(
                        "Error: Strategy must be F (First Fit), B (Best Fit), or W (Worst Fit)"
                    )
                    continue

                result = allocator.request_memory(process_id, size, strategy)
                print(result)

            elif cmd == "RL":
                if len(parts) < 2:
                    print("Error: RL command format: RL <process_id>")
                    continue

                process_id = parts[1]
                result = allocator.release_memory(process_id)
                print(result)

            elif cmd == "C":
                result = allocator.compact_memory()
                print(result)

            elif cmd == "STAT":
                result = allocator.status_report()
                print(result)

            elif cmd == "X":
                print("Exiting memory allocator. Goodbye!")
                break

            else:
                print(f"Unknown command: {cmd}")
                print(
                    "Available commands: RQ (request), RL (release), C (compact), STAT (status), X (exit)"
                )

        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
