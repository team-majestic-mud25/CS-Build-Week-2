"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.FL = [0] * 8

    def load(self):
        """Load a program into memory."""
        address = 0
        program = []
        #check sys args for a filename
        if len(sys.argv) != 2:
            print(f"usage: file.py filename", file=sys.stderr)
            sys.exit(1)
        try:
            #open the file,
            with open(sys.argv[1]) as f:
                for line in f:
                    #filter out spaces and comments.
                    comment_split = line.strip().split("#")
                    num = comment_split[0]
                    #handles blank spaces
                    if num == "":
                        continue
                    #force integer type
                    x= int(num, 2)
                    #load all the bits into a list called program.
                    program.append(x)
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")           
            sys.exit(2)
        #close the file
        f.close     
        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')
        print()

    def ram_read(self, count):
        return self.ram[count]

    def ram_write(self, address, value):
        self.ram[address] = value

    def run(self):
        """Run the CPU."""
        self.load()
        PRA = 0b01001000
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        ADD = 0b10100000
        CMP = 0b10100111
        JNE = 0b01010110
        JEQ = 0b01010101
        JMP = 0b01010100
        IR = self.pc
        SP = 243
        running = True

        while running:
            operand_a = self.ram_read(IR+1)
            operand_b = self.ram_read(IR+2)

            if self.ram[IR] == LDI:
                #load operand_b into ram at location ram[operand_a]
                self.ram_write(operand_a, operand_b)
                #increment the IR by three (the number of instructions per function)
                IR += 3
                #print(f"ram loaded with value of {self.ram[operand_a]}")

            elif self.ram[IR] == PRN:
                #print the thing and increment.
                print(f"YOUR PRINT SIRE: {self.ram[self.ram[IR+1]]}")
                IR += 2

            elif self.ram[IR] == MUL:
                #multiply r0 and r1
                temp = self.ram_read(operand_a) * self.ram_read(operand_b)
                print(f"{self.ram_read(operand_a)} times {self.ram_read(operand_b)}")
                #save the resulting value into r0.
                self.ram_write(operand_a, temp)
                IR += 3
            
            elif self.ram[IR] == PUSH:
                #decrement stack pointer by 1
                SP -= 1
                #add item into the current position on the stack 
                item = self.ram_read(operand_a)
                self.ram_write(SP, item)
                #increment IR but number of instructions in this call
                IR += 2

            elif self.ram[IR] == POP:
                #remove item from the current position
                item = self.ram_read(SP)
                self.ram_write(operand_a, item)
                #increment the SP by 1
                SP += 1
                IR += 2
            
            elif self.ram[IR] == CALL:
                #decrement stack pointer by 1
                SP -= 1
                #save current IR number somewhere (in the stack)
                self.ram_write(SP, IR)
                #move IR counter to location of subroutine.
                IR = self.ram_read(operand_a)
                #this should execute the subroutine, which will include a RET

            elif self.ram[IR] == RET:
                #Modifies IR counter back to saved IR from the call (plus two? because 2 instructions in CALL)
                IR = self.ram_read(SP) + 2
            
            elif self.ram[IR] == ADD:
                #add r0 and r0
                temp = self.ram_read(operand_a) + self.ram_read(operand_b)
                #save the resulting value into r0.
                self.ram_write(operand_a, temp)
                IR += 3

            elif self.ram[IR] == CMP:
                if self.ram_read(operand_a) == self.ram_read(operand_b):
                    self.FL[5] = 0  #Less than flag
                    self.FL[6] = 0  #Greater than flag
                    self.FL[7] = 1  #Equals flag
                elif self.ram_read(operand_a) > self.ram_read(operand_b):
                    self.FL[5] = 0
                    self.FL[6] = 1
                    self.FL[7] = 0
                elif self.ram_read(operand_a) < self.ram_read(operand_b):
                    self.FL[5] = 1
                    self.FL[6] = 0
                    self.FL[7] = 0
                IR += 3

            elif self.ram[IR] == JMP:
                IR = self.ram_read(operand_a)

            elif self.ram[IR] == JEQ:
                if self.FL[7] == 1:
                    IR = self.ram_read(operand_a)
                else:
                    IR += 2

            elif self.ram[IR] == JNE:
                if self.FL[7] == 0:
                    IR = self.ram_read(operand_a) 
                else:
                    IR += 2 
            elif self.ram[IR] == PRA:
                #print the value stored in r0 as an ascii
                value = chr(self.ram_read(operand_a))
                print(f"{value}")
                IR += 2
            elif self.ram[IR] == HLT: 
                running = False

            else:
                print(f"unrecognized input, moving to next cycle")
                IR += 1 
        
