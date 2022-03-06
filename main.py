from distutils.ccompiler import new_compiler

import os
import click

def turingCode (code):
    match code:
        case ">":
            return "((ptr == &arr[29999])?(ptr = &arr[0]):(ptr++));\n"
        case "<":
            return "((ptr == &arr[0])?(ptr = &arr[29999]):(ptr--));\n"
        case "+":
            return "++*ptr;\n"
        case "-":
            return "--*ptr;\n"
        case ".":
            return "putchar(*ptr);\n"
        case ",":
            return "*ptr = getchar();\n"
        case "[":
            return "while(*ptr)\n{\n"
        case "]":
            return "}\n"
        case _:
            return ""
        
def turingJS (code):
    match code:
        case ">":
            return "mem_ptr++;\n"
        case "<":
            return "mem_ptr--;\n"
        case "+":
            return "mem[mem_ptr] = (mem[mem_ptr] || 0) + 1;\n"
        case "-":
            return "mem[mem_ptr] = (mem[mem_ptr] || 0) - 1;\n"
        case ".":
            return "out += String.fromCharCode(mem[mem_ptr] || 0);\n"
        case ",":
            return "mem[mem_ptr] = input.charCodeAt(input_ptr) || 0;\ninput_ptr++;\n"
        case "[":
            return "while( mem[mem_ptr] ) { \n"
        case "]":
            return "}\n"
        case _:
            return ""
        
def cCode (file, fileBase, out):
    cCode = "#include <stdio.h>\nchar arr[30000]={0};\nchar *ptr=arr;\nint main()\n{\n"
    with open(file) as f:
        code = f.read()
        for c in code:
            cCode += turingCode(c)
            
    cCode += "return 0;\n}"
    isExist = os.path.exists("./build")

    if not isExist:
        click.echo("Making build directory!")
        os.makedirs("./build")

    with open(f"./build/{fileBase}.c", "w") as wf:
        wf.write(cCode)

    compiler = new_compiler()
    compiler.compile([f'./build/{fileBase}.c'])
    objExtension = ".o"
    if os.name == 'nt':
        objExtension = ".obj"
    compiler.link_executable(['./build/' + fileBase + objExtension], out)
    
def rawC (file, fileBase, out):
    cCode = "#include <stdio.h>\nchar arr[30000]={0};\nchar *ptr=arr;\nint main()\n{\n"
    with open(file) as f:
        code = f.read()
        for c in code:
            cCode += turingCode(c)
            
    cCode += "return 0;\n}"

    with open(f"{out}.c", "w") as wf:
        wf.write(cCode)
        
def rawJS (file, fileBase, out):
    jsCode = 'var mem_ptr = 0, input_ptr = 0, mem = [], out = "";\n'
    
    with open(file) as f:
        code = f.read()
        for c in code:
            jsCode += turingJS(c)
            
    jsCode += "console.log(out);\n"

    with open(f"{out}.js", "w") as wf:
        wf.write(jsCode)

@click.command()
@click.argument('file')
@click.option('--out', '-out', default=None, help='Output file')
@click.option('--target', '-target', default="bin", help='Output file')
def main(file, out, target):
    if not file.endswith(".bf"):
        click.echo("{file}, is not a valid BF file".format(file))
        return
    fileBase = file.rstrip(".bf")
    if (out is None):
        out = fileBase
    click.echo("Building...")
    if target == "bin":
        cCode(file, fileBase, out)
    if target == "c":
        rawC(file, fileBase, out)
    if target == "js":
        rawJS(file, fileBase, out)

    click.echo(f"Build done!")

if __name__ == "__main__":
    main()