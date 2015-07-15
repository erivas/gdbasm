import gdb
import os
from subprocess import check_call
from tempfile import mkstemp


def NewTempFile():
    (fd, fn) = mkstemp()
    os.close(fd)
    return fn


class AssemblerException(Exception):
    pass


class Assembler(object):
    def generate(self, srcs):
        raise NotImplementedError()


class AssemblerAS(Assembler):
    def generate(self, srcs):
        try:
            asmft = NewTempFile()
            oft = NewTempFile()
            binft = NewTempFile()

            pre = '.code32'
            asmf = open(asmft, 'w')
            text = pre + '\n' + '\n'.join(srcs) + '\n'
            asmf.write(text)
            asmf.close()

            check_call(['as', asmft, '-o', oft])
            check_call(['objcopy', '-O', 'binary', oft, binft])

            binf = open(binft, 'rb')
            ret = binf.read()
            binf.close()
            return ret
        except:
            raise AssemblerException()
        finally:
            if os.path.exists(asmft):
                os.remove(asmft)
            if os.path.exists(oft):
                os.remove(oft)
            if os.path.exists(binft):
                os.remove(binft)


class AssemblerNASM(Assembler):
    def generate(self, srcs):
        try:
            asmft = NewTempFile()
            binft = NewTempFile()

            pre = 'BITS 32'
            asmf = open(asmft, 'w')
            text = pre + '\n' + '\n'.join(srcs) + '\n'
            asmf.write(text)
            asmf.close()

            check_call(['nasm', '-fbin', '-o', binft, asmft])

            binf = open(binft, 'rb')
            ret = binf.read()
            binf.close()
            return ret
        except:
            raise AssemblerException()
        finally:
            if os.path.exists(asmft):
                os.remove(asmft)
            if os.path.exists(binft):
                os.remove(binft)


class AsmGen:
    asm = AssemblerAS

    def __call__(self):
        return self.asm()


class AsmCommand(gdb.Command):
    'Command for re-writing assembly.'

    def __init__(self):
        super(AsmCommand, self).__init__('asm',
                                         gdb.COMMAND_DATA,
                                         gdb.COMPLETE_NONE)

    def invoke(self, arg, from_tty):
        if arg != '':
            eip = int(arg, 16)
        else:
            eip = gdb.selected_frame().pc()
        code = []
        s = raw_input('> ')
        while s != '':
            code.append(s)
            s = raw_input('> ')

        try:
            asm = AsmGen()
            opcodes = asm().generate(code)

            offset = 0
            for opcode in opcodes:
                opcode = ord(opcode)
                address = eip + offset
                command = 'set *(char*)0x%x = 0x%02x' % (address, opcode)
                gdb.execute(command)
                offset += 1
        except AssemblerException:
            print 'Error when assembling.'


AsmCommand()
