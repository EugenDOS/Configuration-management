import argparse

def serializer(cmd, fields, size):
    bits = 0
    bits |= cmd
    for value, offset in fields:
        bits |= (value << offset)
    return bits.to_bytes(size, "little")

def assembler(code):
    bc = []
    for operation, *args in code:
        if operation == "load":
            B, C = args
            bc += serializer(13, ((B, 4), (C, 29)), 5)
        if operation == "read":
            B, C = args
            bc += serializer(14, ((B, 4), (C, 9)), 5)
        if operation == "write":
            B, C = args
            bc += serializer(6, ((B, 4), (C, 34)), 5)
        if operation == "popcnt":
            B, C = args
            bc += serializer(7, ((B, 4), (C, 9)), 5)
    return bc

def assemble(instructions_path: str):
    with open(instructions_path, "r", encoding="utf-8") as f:
        instructions = [[j if j.isdigit() == False else int(j) for j in i.split()] for i in f.readlines()]
    fileName = instructions_path.split(".")[0]
    return assembler(instructions), fileName

def saveToBin(asseblerResult):
    assebledInstructions, fileName = asseblerResult
    with open(f"{fileName}.bin", "wb") as binary_file:
        binary_file.write(bytes(assebledInstructions))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Assemble the instructions file to bytecode.")
    parser.add_argument("instructions_path", help="Path to the instructions file")
    args = parser.parse_args()
    result = assemble(args.instructions_path)
    saveToBin(result)
    



