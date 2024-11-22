import argparse

def logOperation(logPath, operationCode, *args):
    if logPath != None:
        B, C = args
        with open(logPath, "a", encoding="utf-8") as logFile:
            logFile.write(f"A={operationCode},B={B},C={C}\n")

def serializer(cmd, fields, size):
    bits = 0
    bits |= cmd
    for value, offset in fields:
        bits |= (value << offset)
    return bits.to_bytes(size, "little")

def assembler(instructions, logPath=None):
    byteCode = []
    for operation, *args in instructions:
        if operation == "load":
            B, C = args
            byteCode += serializer(13, ((B, 4), (C, 29)), 5)
            logOperation(logPath, 13, B, C)
        if operation == "read":
            B, C = args
            byteCode += serializer(14, ((B, 4), (C, 9)), 5)
            logOperation(logPath, 14, B, C)
        if operation == "write":
            B, C = args
            byteCode += serializer(6, ((B, 4), (C, 34)), 5)
            logOperation(logPath, 6, B, C)
        if operation == "popcnt":
            B, C = args
            byteCode += serializer(7, ((B, 4), (C, 9)), 5)
            logOperation(logPath, 7, B, C)
    return byteCode

def assemble(instructions_path: str, logPath=None):
    with open(instructions_path, "r", encoding="utf-8") as f:
        instructions = [[j if j.isdigit() == False else int(j) for j in i.split()] for i in f.readlines()]
    return assembler(instructions, logPath)

def saveToBin(assebledInstructions, fileName):
    with open(fileName, "wb") as binary_file:
        binary_file.write(bytes(assebledInstructions))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assemble the instructions file to bytecode.")
    parser.add_argument("instructions_path", help="Path to the instructions file (txt)")
    parser.add_argument("binary_path", help="Path to the binary file (bin)")
    parser.add_argument("log_path", help="Path to the log file (csv)")
    args = parser.parse_args()
    result = assemble(args.instructions_path, args.log_path)
    saveToBin(result, args.binary_path)
    



