from argparse import ArgumentParser
from parser import Parser, Command
from code import Code
from symbol_table import SymbolTable
from os import path

def parse_args() -> str:
    arg_parser = ArgumentParser(
        description="python3 assembler.py <file_name>"
    )

    arg_parser.add_argument(
        "file_name",
    )

    return arg_parser.parse_args().file_name

def main():
    file_name = parse_args()
    parser = Parser(file_name)
    code = Code()
    symbol_table = SymbolTable()

    result = ""

    while parser.has_more_commands():
        parser.advance()
        
        if parser.command_type() == Command.L_COMMAND:
            symbol_table.add_entry(parser.symbol(), parser.address)

    parser.reset()

    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == Command.A_COMMAND:
            try:
                tmp_result = bin(int(parser.symbol()))[2:].zfill(16) + "\n"
                result += tmp_result
            except ValueError:
                if symbol_table.contains(parser.symbol()):
                    address = symbol_table.get_address(parser.symbol())
                    result += bin(address)[2:].zfill(16) + "\n"
                else:
                    exit(f"Symbol table doesn't contain symbol {parser.symbol()}")
        elif parser.command_type() == Command.C_COMMAND:
            dest = code.dest(
                parser.dest()
            )
            comp = code.comp(
                parser.comp()
            )
            parser_jump = parser.jump()
            jump = "000"
            if parser_jump != None:
                jump = code.jump(
                    parser_jump
                )
            
            result += "111" + comp + dest + jump + "\n"
        else:
            pass

    file_name, _ = path.splitext(parser.file_name)

    with open(f"{file_name}.out", "w") as file_data:
        file_data.write(result)

if __name__ == "__main__":
    main()
