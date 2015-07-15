# gdbasm
Assembler plugin for gdb

## What is it?
It is a script for gdb.

## What does it do?
It lets you overwrite/modify assembly code in a location of choice.

## How do I use it?
First, load it in gdb by using the command `source`.  When debugging,
you can use the command `asm [address]` to start assembling code at
the specified address. If no address is given, then the current
program counter is used.  It will consume input until an empty line is
found.

```
(gdb) source gdbasm.py
(gdb) x/3i $eip
=> 0x8048a37 <main+3>:  and    $0xfffffff0,%esp
   0x8048a3a <main+6>:  sub    $0x18bd0,%esp
   0x8048a40 <main+12>: mov    %gs:0x14,%eax
(gdb) asm
> nop
> xorl %eax, %eax
> nop
> 
(gdb) x/3i $eip
=> 0x8048a37 <main+3>:  nop
   0x8048a38 <main+4>:  xor    %eax,%eax
   0x8048a3a <main+6>:  nop
(gdb) 
```

## How does it work?
It calls `as` to assemble your code, and then overwrites the memory
with the generated opcodes. If you want to use `nasm`, just modify
AsmGen to generate an AssemblerNASM object instead of an AssemblerAS
object.

## What is its license?
BSD 3.

## How can I make it auto-load?
Just add the following line to the file .gdbinit in your home folder.

```
source gdbasm.py
```
