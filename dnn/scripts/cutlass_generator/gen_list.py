from generator import (
    GenerateGemmOperations,
    GenerateGemvOperations,
    GenerateConv2dOperations,
    GenerateDeconvOperations,
    GenerateDwconv2dFpropOperations,
    GenerateDwconv2dDgradOperations,
    GenerateDwconv2dWgradOperations,
)


class GenArg:
    def __init__(self, gen_op, gen_type):
        self.operations = gen_op
        self.type = gen_type


def write_op_list(f, gen_op, gen_type):
    if gen_op == "gemm":
        operations = GenerateGemmOperations(GenArg(gen_op, gen_type))
    elif gen_op == "gemv":
        operations = GenerateGemvOperations(GenArg(gen_op, gen_type))
    elif gen_op == "conv2d":
        operations = GenerateConv2dOperations(GenArg(gen_op, gen_type))
    elif gen_op == "deconv":
        operations = GenerateDeconvOperations(GenArg(gen_op, gen_type))
    elif gen_op == "dwconv2d_fprop":
        operations = GenerateDwconv2dFpropOperations(GenArg(gen_op, gen_type))
    elif gen_op == "dwconv2d_dgrad":
        operations = GenerateDwconv2dDgradOperations(GenArg(gen_op, gen_type))
    elif gen_op == "dwconv2d_wgrad":
        operations = GenerateDwconv2dWgradOperations(GenArg(gen_op, gen_type))
    for op in operations:
        f.write('    "%s.cu",\n' % op.procedural_name())
    if gen_op != "gemv":
        f.write('    "all_%s_%s_operations.cu",\n' % (gen_op, gen_type))

# Write down a list of merged filenames
def write_merge_file_name(f, gen_op, gen_type):
    f.write('    "{}_{}_1.cu",\n'.format(gen_op,gen_type))
    f.write('    "{}_{}_2.cu",\n'.format(gen_op,gen_type))
    if gen_op != "gemv":
        f.write('    "all_{}_{}_operations.cu",\n'.format(gen_op,gen_type))

if __name__ == "__main__":
    with open("list.bzl", "w") as f:
        f.write("# Generated by dnn/scripts/cutlass_generator/gen_list.py\n\n")
        f.write("cutlass_gen_list = [\n")

        write_merge_file_name(f, "gemm", "simt")
        write_merge_file_name(f, "gemm", "tensorop1688")
        write_merge_file_name(f, "gemm", "tensorop884")
        write_merge_file_name(f, "gemv", "simt")
        write_merge_file_name(f, "deconv", "simt")
        write_merge_file_name(f, "deconv", "tensorop8816")
        write_merge_file_name(f, "conv2d", "simt")
        write_merge_file_name(f, "conv2d", "tensorop8816")
        write_merge_file_name(f, "conv2d", "tensorop8832")
        write_merge_file_name(f, "dwconv2d_fprop", "simt")
        write_merge_file_name(f, "dwconv2d_fprop", "tensorop884")
        write_merge_file_name(f, "dwconv2d_dgrad", "simt")
        write_merge_file_name(f, "dwconv2d_dgrad", "tensorop884")
        write_merge_file_name(f, "dwconv2d_wgrad", "simt")
        write_merge_file_name(f, "dwconv2d_wgrad", "tensorop884")
        f.write("]")
