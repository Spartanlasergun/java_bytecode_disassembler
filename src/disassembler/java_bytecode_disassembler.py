import os            # filesystem manipulation
import traceback     # for system traceback in error handling operations
import shutil        # for removing directories
from os import path  # for scanning directories

class java_bytecode_disassembler:


    def __init__(self, pathway, verbose=False, fail_check=True, write=True):

        global glob_path
        glob_path = pathway    # store pathway for use across classes

        global code_count
        code_count = 0  # variable to keep track of each code attribute if one or more are present within the bytecode

        self.write = write        # if the write value is False, the disassembler does not perform its usual write operations
        self.pathway = pathway  # store the pathway for global use within the class
        self.verbose = verbose  # prints additional data to the console during disassembly for more extensive debugging


        #  fail_check is used for handling if the disassembly fails
        self.fail_check = fail_check   # if True, the filepaths of the files that failed disassembly
                                       # are written to a text file.

        # create directory to store deconstructed ".class" file data-----------------------------------------------------------
        # This section contains basic startup operations for the disassembler. A directory called 'deconst_class' is created
        # within the current working directory. It is used by the program to store the disassembled java bytecode.

        if write:   # if the write condition is True, directories are created as normal
            cur_dir = os.getcwd()  # get current working directory
            sub_dirs = [f.path for f in os.scandir(cur_dir) if f.is_dir()]  # get names of sub_directories
            dir_check = 0
            deconstructed_class = cur_dir + "/deconst_class"  # name of directory to create i.e. deconstructed class
            for dir in sub_dirs:  # check to ensure directory doesn't already exist
                if path.basename(dir) == "deconst_class":
                    dir_check = 1
            if dir_check == 0:  # if directory doesn't exist it is created
                os.mkdir(deconstructed_class)

            # A sub-directory with the name of the '.class' file is created to store processed data relating to the individual file
            # being processed.

            if path.exists(pathway):  # check to ensure the '.class' file exists
                classfile_name = path.basename(pathway)  # get the filename from the path
                if classfile_name.endswith(".class"):  # check to ensure that the filetype is '.class'
                    classfile_prefix = classfile_name.removesuffix(".class")  # remove the filetype suffix
                    self.classfile_dir = deconstructed_class + "/" + classfile_prefix  # create directory path for storing data

                    if (path.exists(self.classfile_dir)) == False:  # if the directory does not exist,
                        os.mkdir(self.classfile_dir)  # make the directory
                        self.control_box()
                    else:
                        shutil.rmtree(self.classfile_dir)  # if the directory already exists, it will be overwritten
                        os.mkdir(self.classfile_dir)
                        self.control_box()
                else:
                    print("ERROR: Not a valid '.class' file")
            else:
                print("ERROR: path to '.class' file does not exist")
        else:
            self.classfile_dir = None
            self.control_box()


    # Main Control Box for the script---------------------------------------------------------------------------------------
    # Major functions of the disassembler collapse from within this function.

    def control_box(self):

        try:
            if self.verbose:
                print("Reading raw bytecode")    # if the verbose command is passed, additonal data is printed
            self.bytecode()
            if self.verbose:
                print("Processing magic number")
            self.magic_number()
            if self.verbose:
                print("Processing major and minor version numbers")
            self.major_minor()
            if self.verbose:
                print("Processing constant pool count")
            self.constant_pool_count()
            if self.verbose:
                print("Processing constant pool")
            self.constant_pool()
            if self.verbose:
                print("Processing access flags")
            self.access_flags()
            if self.verbose:
                print("Processing this_class")
            self.this_class()
            if self.verbose:
                print("Processing super_class")
            self.super_class()
            if self.verbose:
                print("Processing interfaces_count")
            self.interfaces_count()
            if self.verbose:
                print("Processing interfaces")
            self.interfaces()
            if self.verbose:
                print("Processing fields_count")
            self.fields_count()
            if self.verbose:
                print("Processing fields")
            self.fields()
            if self.verbose:
                print("Processing methods_count")
            self.methods_count()
            if self.verbose:
                print("Processing methods")
            self.methods()
            if self.verbose:
                print("Processing attributes_count")
            self.attributes_count()
            if self.verbose:
                print("Processing attributes")
            self.attributes()
        except:
            # print error traceback
            print(traceback.format_exc())

            # write the path of to the file that failed processing for further investigation
            if self.fail_check:
                write_error = open("failed.txt", 'a')
                write_error.write(self.pathway + "\n")
                write_error.close()

    # Reading the bytecode--------------------------------------------------------------------------------------------------
    # The raw binaries for the '.class' file is read. It is converted to hexadecimal form and each byte is stored into an
    # array object.
    def bytecode(self):
        # read raw bytecode binaries
        classfile_data = open(self.pathway, 'rb')
        raw_data = classfile_data.read()
        classfile_data.close()

        # convert binaries to hexadecimal
        raw_data = bytes.hex(raw_data)

        # sort each individual byte into array
        half_byte = []
        for byte_data in raw_data:
            half_byte.append(byte_data)

        # sort each byte into global array object
        total_bytes = ((len(raw_data)) / 2)
        byte_split = []
        while total_bytes != 0:
            byte_split.append(half_byte[0] + half_byte[1])
            del half_byte[0:2]
            total_bytes = total_bytes - 1

        # The data variable is globalized to avoid building redundancies further down in the disassembly. It is used
        # by both classes within the program.
        global data
        data = byte_split

    # Magic-Number Processing-----------------------------------------------------------------------------------------------
    # All '.class' files begin with the magic number 'cafebabe'. This function identifies the data, writes it to a file and
    # removes the magic number from the main data dump (i.e. bytecode.data).
    def magic_number(self):
        global data

        magic = "cafebabe"

        # magic number is four bytes of data:
        get_magic = data[0] + data[1] + data[2] + data[3]

        if magic == get_magic:                                             # check to ensure the magic number is present
            del data[0:4]                                         # remove the magic number from the main data dump
            if self.write:      # if write operations are specified, write the data
                store_magic = open((self.classfile_dir + "/magic_number.txt"), "w")  # store magic number
                store_magic.write(get_magic)                                    # this data may be used by another python script
                store_magic.close()
        else:
            print("ERROR: magic number not found")

    # Major/Minor version numbers-------------------------------------------------------------------------------------------
    # All '.class' files contain major and minor version numbers that the JAVA virtual machine uses to understand how they
    # should be handled. This function identifies the version numbers, removes them from the data dump and store them to a
    # file.
    def major_minor(self):
        global data

        # extract and remove major and minor version numbers from the data dump
        minor_version = data[0] + data[1]
        del data[0:2]
        major_version = data[0] + data[1]
        del data[0:2]

        # convert the version numbers from hexadecimal to integer for evaluation
        minor_version = int(minor_version, 16)
        major_version = int(major_version, 16)

        # perform simple check on the version numbers and store the data
        if major_version > minor_version:                 # if major version is more than minor version
            if self.write:    # if write operations are specified, write the data
                store_major_minor = open((self.classfile_dir + "/major_minor_versions.txt"), "w")  # store major and minor version numbers
                store_major_minor.write(str(minor_version) + "\n" + str(major_version))       # this data may be used by another python script
                store_major_minor.close()
        else:
            print("ERROR: major and minor version numbers not correctly identified")

    # Constant_Pool_Count---------------------------------------------------------------------------------------------------
    # This section identifes the number of constants in the constant pool

    def constant_pool_count(self):
        global data

        self.number_of_constants = data[0] + data[1]
        self.number_of_constants = int(self.number_of_constants, 16)  # convert hexadecimal value to integer
        del data[0:2]

        if self.number_of_constants > 0:  # Verify that the Constant Pool Count is a valid integer
            if self.write:    # if write operations are specified, write the data
                store_const_count = open((self.classfile_dir + "/constant_pool_count.txt"), "w")  # store constant pool count
                store_const_count.write(str(self.number_of_constants))  # this data is used by another python script
                store_const_count.close()
        else:
            print("ERROR: Constant Pool Count not valid")

    # Constant_Pool---------------------------------------------------------------------------------------------------------

    def constant_pool(self):
        global data

        # Reading the data from the constant pool is one of the larger operations involved in
        # deconstructing the '.class' file. Like most of the other operations, it requires more
        # specialized knowledge than can be explained within regular programming comments.
        # Some of the processes in this section have extremely minimalized comments for this reason.

        # the Constant_Pool_Tags are the readable tags associated with certain integer values
        Constant_Pool_Tags = [[1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16, 17, 18, 19, 20],
                              ["Constant_Utf8", "Constant_Integer", "Constant_Float", "Constant_Long",
                               "Constant_Double", "Constant_Class", "Constant_String", "Constant_Fieldref",
                               "Constant_Methodref", "Constant_InterfaceMethodref", "Constant_NameAndType",
                               "Constant_MethodHandle", "Constant_MethodType", "CONSTANT_Dynamic", "Constant_InvokeDynamic",
                               "CONSTANT_Module", "CONSTANT_Package"]]

        Constant_Pool = [["reserved"]]  # first index of the constant pool is reserved by the JVM
        Constant_Pool_index = 0  # initialize index count
        number_of_constants = self.number_of_constants  # variable holding the number of constants for creating the loop counter

        while number_of_constants != 1:  # loop iterates over the data for each constant in the constant pool
            Constant_Type = data[0]  # the constant type is one byte of the data array
            Constant_Type = int(Constant_Type, 16)  # convert the constant type to its integer equivalent
            Constant_Pool_index = Constant_Pool_index + 1  # increment the constant pool index so that each iteration stores the data in a new index
            for item in Constant_Pool_Tags[0]:  # the 'for' loop checks for the human readable tag associated with the constant type integer
                if Constant_Type == item:
                    Constant_Type = Constant_Pool_Tags[1][Constant_Pool_Tags[0].index(item)]

            del data[0]  # clear the constant type from the data dump

            temp_array = [Constant_Type]   # this array holds data that is then append to the constant pool during each iteration

            # Each constant type needs to be handled differently
            # the if structure below verifies the type of constant and performs the necessary operations for the type that it identifies
            if Constant_Type == Constant_Pool_Tags[1][0]:     #Check for the Constant_Utf8
                length = data[0] + data[1]
                length = int(length, 16)
                del data[0:2]   # clear the length value from the data dump
                temp_array.append(length)
                utf_data = ""
                utf_string = data[0:length]
                for text in utf_string:
                    utf_data = utf_data + text
                del data[0:length]

                try:
                    utf_data = bytearray.fromhex(utf_data).decode()
                except:
                    print("\tWARNING: bytecode contains special characters; data may be obfuscated")
                temp_array.append(utf_data)
                Constant_Pool.append(temp_array)
            elif Constant_Type == Constant_Pool_Tags[1][1]:     #Check for Constant_Integer type
                int_data = data[0] + data[1] + data[2] + data[3]
                int_data = int(int_data, 16)
                del data[0:4]  # remove int_data from the data dump
                temp_array.append(int_data)
                Constant_Pool.append(temp_array)
            elif Constant_Type == Constant_Pool_Tags[1][2]:     #Check for Constant_Float type
                float_data = data[0] + data[1] + data[2] + data[3]
                float_data = float.fromhex(float_data)
                del data[0:4]   # remove float_data from the data dump
                temp_array.append(float_data)
                Constant_Pool.append(temp_array)
            elif Constant_Type == Constant_Pool_Tags[1][3]:     #Check for Constant_Long type
                bytes = 8
                long_data = ""
                while bytes != 0:
                    long_data = long_data + data[0]
                    del data[0]
                    bytes = bytes - 1
                long_data = int(long_data, 16)
                temp_array.append(long_data)
                Constant_Pool.append(temp_array)
                Constant_Pool.append("longspace")
                number_of_constants = number_of_constants - 1   # the Constant_Long type accounts for two indexes into the constant pool
            elif Constant_Type == Constant_Pool_Tags[1][4]:     #Check for Constant_Double type
                bytes = 8
                double_data = ""
                while bytes != 0:
                    double_data = double_data + data[0]
                    del data[0]
                    bytes = bytes - 1
                double_data = float.fromhex(double_data)
                temp_array.append(double_data)
                Constant_Pool.append(temp_array)
                Constant_Pool.append("doublespace")
                number_of_constants = number_of_constants - 1    # the Constant_Double type accounts for two indexes into the constant pool
            elif Constant_Type == Constant_Pool_Tags[1][5]:     #Check for the Constant_Class type
                name_index = data[0] + data[1]
                name_index = int(name_index, 16)
                del data[0:2]  # clear the name index from the data dump
                temp_array.append(name_index)
                Constant_Pool.append(temp_array)
            elif Constant_Type == Constant_Pool_Tags[1][6]:     #Check for the Constant_String
                string_index = data[0] + data[1]
                string_index = int(string_index, 16)
                del data[0:2]  # clear the string_index from the data dump
                temp_array.append(string_index)
                Constant_Pool.append(temp_array)
            elif (Constant_Type == Constant_Pool_Tags[1][7]) or (Constant_Type == Constant_Pool_Tags[1][8]) or \
                    (Constant_Type == Constant_Pool_Tags[1][9]):     #Check for the Constant_Fieldref, Constant_Methodref and Constant_InterfaceMethodref
                class_index = data[0] + data[1]
                class_index = int(class_index, 16)
                del data[0:2]   # clear the class_index from the data dump
                name_and_type_index = data[0] + data[1]
                name_and_type_index = int(name_and_type_index, 16)
                del data[0:2]   # clear the name_and_type_index from the data dump
                temp_array.append(class_index)
                temp_array.append(name_and_type_index)
                Constant_Pool.append(temp_array)
            elif Constant_Type == Constant_Pool_Tags[1][10]:     #Check for the Constant_NameAndType type
                name_index = data[0] + data[1]
                name_index = int(name_index, 16)
                del data[0:2]   # clear the name_index from the data dump
                descriptor_index = data[0] + data[1]
                descriptor_index = int(descriptor_index, 16)
                del data[0:2]  # clear the descriptor_index from the data dump
                temp_array.append(name_index)
                temp_array.append(descriptor_index)
                Constant_Pool.append(temp_array)
            elif Constant_Type == Constant_Pool_Tags[1][11]:  # Check for the Constant_MethodHandle type
                reference_kind = data[0]
                reference_kind = int(reference_kind, 16)
                del data[0]   # clear the reference_kind from the data dump
                reference_index = data[0] + data[1]
                reference_index = int(reference_index, 16)
                del data[0:2]  # clear the reference_index from the data dump
                temp_array.append(reference_kind)
                temp_array.append(reference_index)
                Constant_Pool.append(temp_array)
            elif Constant_Type == Constant_Pool_Tags[1][12]:  # Check for the Constant_MethodType type
                descriptor_index = data[0] + data[1]
                descriptor_index = int(descriptor_index, 16)
                del data[0:2]   # clear the descriptor_index from the data dump
                temp_array.append(descriptor_index)
                Constant_Pool.append(temp_array)
            elif Constant_Type == Constant_Pool_Tags[1][13]:  # Check for the Constant_Dynamic type
                bootstrap_method_attr_index = data[0] + data[1]
                bootstrap_method_attr_index = int(bootstrap_method_attr_index, 16)
                del data[0:2]  # clear the bootstrap_method_attr_index from the data dump
                name_and_type_index = data[0] + data[1]
                name_and_type_index = int(name_and_type_index, 16)
                del data[0:2]  # clear the name_and_type_index from the data dump
                temp_array.append(bootstrap_method_attr_index)
                temp_array.append(name_and_type_index)
                Constant_Pool.append(temp_array)
            elif Constant_Type == Constant_Pool_Tags[1][14]:  # Check for the Constant_InvokeDynamic type
                bootstrap_method_attr_index = data[0] + data[1]
                bootstrap_method_attr_index = int(bootstrap_method_attr_index, 16)
                del data[0:2]    # clear the bootstrap_method_attr_index from the data dump
                name_and_type_index = data[0] + data[1]
                name_and_type_index = int(name_and_type_index, 16)
                del data[0:2]  # clear the name_and_type_index from the data dump
                temp_array.append(bootstrap_method_attr_index)
                temp_array.append(name_and_type_index)
                Constant_Pool.append(temp_array)
            elif Constant_Type == Constant_Pool_Tags[1][15]:  # Check for the Constant_Module type
                name_index = data[0] + data[1]
                name_index = int(name_index, 16)
                del data[0:2]
                temp_array.append(name_index)
                Constant_Pool.append(temp_array)
            elif Constant_Type == Constant_Pool_Tags[1][16]: # Check for the Constant_Package type
                name_index = data[0] + data[1]
                name_index = int(name_index, 16)
                del data[0:2]
                temp_array.append(name_index)
                Constant_Pool.append(temp_array)
            else:
                print("ERROR: Unidentified Constant in the Constant Pool")
                print(Constant_Type)
                number_of_constants = 2
            number_of_constants = number_of_constants - 1

        self.constant_pool_data = Constant_Pool   # store the constant_pool array as a global object for use outside of this function

        if self.number_of_constants == len(Constant_Pool):
            if self.write:   # if write operations are specified, write the data
                const_pool_dir = self.classfile_dir + "/constant_pool"
                if (path.exists(const_pool_dir)) == False:
                    os.mkdir(const_pool_dir)
                const_count = 0
                for constant in Constant_Pool:
                    store_const_pool = open((const_pool_dir + "/constant_" + str(const_count) + ".txt"), "w", encoding="utf-8")  #store constant pool data
                    for item in constant:
                        store_const_pool.write(str(item) + "\n")                     #this data is used by another python script
                    store_const_pool.close()
                    const_count = const_count + 1
        else:
            print("ERROR: All of the Constants have not been correctly identified")

    # Access_Flags----------------------------------------------------------------------------------------------------------
    # This section contains the declaration for the type of access permitted to the highest level class within the bytecode.
    # Java enforces structure within each '.class' file that does not permit depth beyond a single super-class. Classes
    # outside the main superclass and beyond the depth of the main entry point are compiled separately as their own
    # unique '.class' files.


    def access_flags(self):
        global data

        access_flags = data[0] + data[1]
        del data[0:2]
        zero = access_flags[0]
        first = access_flags[1]
        second = access_flags[2]
        third = access_flags[3]

        Access_Flags = []
        if zero == "0":                                        #check for access flags in the first half-byte
            zero = None
        elif zero == "1":
            Access_Flags.append("ACC_SYNTHETIC")
        elif zero == "2":
            Access_Flags.append("ACC_ANNOTATION")
        elif zero == "4":
            Access_Flags.append("ACC_ENUM")

        if first == "0":                                       #check for access flags in the second half-byte
            first = None
        elif first == "2":
            Access_Flags.append("ACC_INTERFACE")
        elif first == "4":
            Access_Flags.append("ACC_ABSTRACT")

        if second == "0":                                      #check for access flags in the third half-byte
            second = None
        elif second == "1":
            Access_Flags.append("ACC_FINAL")
        elif second == "2":
            Access_Flags.append("ACC_SUPER")

        if third == "0":                                       #check for access flags in the fourth half-byte
            third = None
        elif third == "1":
            Access_Flags.append("ACC_PUBLIC")

        if len(Access_Flags) > 0:
            if self.write:    # if write operations are specified, write the data
                store_ACC_FLAGS = open((self.classfile_dir + "/access_flags.txt"), "w")  #store access flags data
                for item in Access_Flags:
                    store_ACC_FLAGS.write(str(item) + "\n")                         #this data is used by another python script
                store_ACC_FLAGS.close()

    # this_class------------------------------------------------------------------------------------------------------------
    # The this_class represents the class that contains the main entry point for the program.

    def this_class(self):
        global data

        this_class = data[0] + data[1]  # this_class is two bytes of the data[] array
        this_class = int(this_class, 16)  # convert this_class hex data to its integer equivalent
        del data[0:2]  # clear the this_class data from the hex dump

        # this section performs several checks to ensure that the this_class data is valid
        if (this_class > 0) and (this_class < int(self.number_of_constants)):
            if self.write:    # if write operations are specified, write the data
                if self.constant_pool_data[this_class][0] == "Constant_Class":
                    store_this_class = open((self.classfile_dir + "/this_class.txt"), "w")  # store this_class data
                    store_this_class.write(self.constant_pool_data[this_class][0] + "\n" + str(self.constant_pool_data[this_class][1]))  # this data is used by another python script
                    store_this_class.close()
        else:
            print("ERROR: the this_class value is incorrect")  # if the this_class data is invalid, the program exits here

    # super_class-------------------------------------------------------------------------------------------------------
    # The super_class represents the direct super class in relation to the main entry point of the program.

    def super_class(self):
        global data

        super_class = data[0] + data[1]   # the super_class data is two bytes long
        super_class = int(super_class, 16)  # convert the super_class data to its integer equivalent
        del data[0:2]  # remove the super_class data from the hex-dump

        # this section performs several checks to ensure that the super_class data is valid
        if (super_class >= 0) and (super_class < int(self.number_of_constants)):
            if self.constant_pool_data[super_class][0] == "Constant_Class":
                if self.write:   # if write operations are specified, write the data
                    store_super_class = open((self.classfile_dir + "/super_class.txt"), "w")  # store super_class data
                    store_super_class.write(self.constant_pool_data[super_class][0] + "\n" + str(self.constant_pool_data[super_class][1]))  # this data is used by another python script
                    store_super_class.close()
            else:
                print("ERROR: invalid index reference for the super_class")
        else:
            print("ERROR: the super_class value is incorrect")  # if the super_class data is invalid, the program exits here

    # interfaces_count--------------------------------------------------------------------------------------------------
    # the interfaces_count is an integer value that gives the number of interfaces present within the '.class' file.

    def interfaces_count(self):
        global data

        self.i_count = data[0] + data[1]  # the interfaces_count is two bytes of data
        self.i_count = int(self.i_count, 16)  # convert the interfaces_count to its integer equivalent
        del data[0:2]  # clear the interfaces_count from the hex-dump

        if self.write:   # if write operations are specified, write the data
            store_interfaces_count = open((self.classfile_dir + "/interfaces_count.txt"), "w")  # store interfaces_count data
            store_interfaces_count.write(str(self.i_count))  # this data is used by another python script
            store_interfaces_count.close()

    # interfaces--------------------------------------------------------------------------------------------------------
    # This section defines the method that is used to extract the data associated with interfaces defined within the
    # '.class' file. ('.class' files may contain zero or more interfaces.)

    def interfaces(self):
        global data

        interfaces = []  # empty array for storing interface indexes into the constant pool
        i_check = True   # variable used to evaluate the integrity of the indexes associated with interfaces
        interfaces_count = self.i_count  # inherit the interfaces count from the previous function
        while interfaces_count != 0:
            interface = data[0] + data[1]    # read the interface index
            interface = int(interface, 16)             # convert the index to integer
            del data[0:2]                         # remove the processed data from the data dump
            interfaces.append(interface)               # store data to array so that it can be written to a file
            if self.constant_pool_data[interface][0] == "Constant_Class":   # ensure that the index is valid
                interfaces_count = interfaces_count - 1                     # decrement the loop counter
            else:
                interfaces_count = 0
                i_check = False  # if the interface is invalid the loop will exit and the function will not continue
                print("ERROR: Interfaces do not match constant pool data")  # Error statement for debugging

        if i_check:   # if the interfaces are valid, the data is written to a text file
            if self.write:   # if write operations are specified, write the data
                store_interfaces = open((self.classfile_dir + "/interfaces.txt"), "w")  # store interfaces data
                if self.i_count != 0:
                    for item in interfaces:
                        store_interfaces.write(str(item) + "\n")  # this data is used by another python script
                else:
                    store_interfaces.write("No Interfaces")
                store_interfaces.close()

    # fields_counts-----------------------------------------------------------------------------------------------------
    # the fields_count is an integer value that gives the number of fields that are described within the '.class' file.

    def fields_count(self):
        global data

        # f_count is initialized as an object because it is used in the next section
        self.f_count = data[0] + data[1]  # fields_count is two bytes of data
        self.f_count = int(self.f_count, 16)  # convert fields_count to its integer equivalent
        del data[0:2]  # remove fields_count data from the hex-dump

        if self.write:  # if write operations are specified, write the data
            store_fields_count = open((self.classfile_dir + "/fields_count.txt"), "w")  # store fields_count data
            store_fields_count.write(str(self.f_count))  # this data is used by another python script
            store_fields_count.close()


    # fields------------------------------------------------------------------------------------------------------------
    # This section describes the method that is used to extract the data associated with fields within the '.class' file.

    def fields(self):
        global data

        # the fields_count is localized to this method in its own variable - f_count
        f_count = self.f_count
        # main loop of the fields method
        while f_count != 0:
            # access_flags
            flag_data = data[0] + data[1]
            f_access_flags = []
            zero = flag_data[0]    # define first half-byte of Access Flag data
            first = flag_data[1]   # define second half-byte of Access Flag data
            second = flag_data[2]  # define third half-byte of Access Flag data
            third = flag_data[3]   # define fourth half-byte of Access Flag data

            if zero == "0":  # check for access flags in the first half-byte
                zero = None
            elif zero == "1":
                f_access_flags.append("ACC_SYNTHETIC")
            elif zero == "4":
                f_access_flags.append("ACC_ENUM")

            if first != "0":  # this byte of data is always equal to zero with the fields structure
                print("ERROR: Check field access flags")

            if second == "0":  # check for access flags in the third half-byte
                second = None
            elif second == "1":
                f_access_flags.append("ACC_FINAL")
            elif second == "4":
                f_access_flags.append("ACC_VOLATILE")
            elif second == "8":
                f_access_flags.append("ACC_TRANSIENT")

            if third == "0":  # check for access flags in the fourth half-byte
                third = None
            elif third == "1":
                f_access_flags.append("ACC_PUBLIC")
            elif third == "2":
                f_access_flags.append("ACC_PRIVATE")
            elif third == "4":
                f_access_flags.append("ACC_PROTECTED")
            elif third == "8":
                f_access_flags.append("ACC_STATIC")

            if len(f_access_flags) == 0:
                f_access_flags.append("No_Access_Flags")

            del data[0:2]

            # name index
            f_name_index = data[0] + data[1]
            f_name_index = int(f_name_index, 16)
            del data[0:2]

            # descriptor index
            f_descriptor_index = data[0] + data[1]
            f_descriptor_index = int(f_descriptor_index, 16)
            del data[0:2]

            # attribute count
            f_attribute_count = data[0] + data[1]
            f_attribute_count = int(f_attribute_count, 16)
            del data[0:2]

            while f_attribute_count != 0:   # main loop for processing attributes

                # To minimize redundancies, the attribute_info structure is treated as a seperate object that can
                # be called at will to disassemble the attributes for any given section of the bytecode.

                attribute_info(self.constant_pool_data, self.classfile_dir, self.verbose, self.write)

                f_attribute_count = f_attribute_count - 1

            # decrement the main loop counter (i.e. the field count)
            f_count = f_count - 1


    def methods_count(self):
        global data

        # m_count is initialized as an object because it is used in the next section
        self.m_count = data[0] + data[1]  # methods_count is two bytes of data
        self.m_count = int(self.m_count, 16)  # convert methods_count to its integer equivalent
        del data[0:2]  # remove methods_count data from the hex-dump

        if self.write:   # if write operations are specified, write the data
            store_methods_count = open((self.classfile_dir + "/methods_count.txt"), "w")  # store methods_count data
            store_methods_count.write(str(self.m_count))  # this data is used by another python script
            store_methods_count.close()

    def methods(self):
        global data

        # the methods_count is localized to this method in its own variable - m_count
        m_count = self.m_count

        # main loop for processing each method
        while m_count != 0:
            # access_flags
            flag_data = data[0] + data[1]
            m_access_flags = []
            zero = flag_data[0]  # define first half-byte of Access Flag data
            first = flag_data[1]  # define second half-byte of Access Flag data
            second = flag_data[2]  # define third half-byte of Access Flag data
            third = flag_data[3]  # define fourth half-byte of Access Flag data

            if zero == "0":  # check for access flags in the first half-byte
                zero = None
            elif zero == "1":
                m_access_flags.append("ACC_SYNTHETIC")

            if first == "0":  # check for access flags in the third half-byte
                first = None
            elif first == "1":
                m_access_flags.append("ACC_NATIVE")
            elif first == "4":
                m_access_flags.append("ACC_ABSTRACT")
            elif first == "8":
                m_access_flags.append("ACC_STRICT")

            if second == "0":  # check for access flags in the third half-byte
                second = None
            elif second == "1":
                m_access_flags.append("ACC_FINAL")
            elif second == "2":
                m_access_flags.append("ACC_SYNCHRONIZED")
            elif second == "4":
                m_access_flags.append("ACC_BRIDGE")
            elif second == "8":
                m_access_flags.append("ACC_VARARGS")

            if third == "0":  # check for access flags in the fourth half-byte
                third = None
            elif third == "1":
                m_access_flags.append("ACC_PUBLIC")
            elif third == "2":
                m_access_flags.append("ACC_PRIVATE")
            elif third == "4":
                m_access_flags.append("ACC_PROTECTED")
            elif third == "8":
                m_access_flags.append("ACC_STATIC")

            if len(m_access_flags) == 0:
                m_access_flags.append("No_Access_Flags")

            del data[0:2]

            # name index
            m_name_index = data[0] + data[1]
            m_name_index = int(m_name_index, 16)
            del data[0:2]

            # descriptor index
            m_descriptor_index = data[0] + data[1]
            m_descriptor_index = int(m_descriptor_index, 16)
            del data[0:2]

            # attribute count
            m_attribute_count = data[0] + data[1]
            m_attribute_count = int(m_attribute_count, 16)
            del data[0:2]

            while m_attribute_count != 0:

                attribute_info(self.constant_pool_data, self.classfile_dir, self.verbose, self.write)

                m_attribute_count = m_attribute_count - 1


            m_count = m_count - 1   # decrement main loop counter

    def attributes_count(self):
        global data

        # a_count is initialized as an object because it is used in the next section
        self.a_count = data[0] + data[1]  # attributes_count is two bytes of data
        self.a_count = int(self.a_count, 16)  # convert attributes_count to its integer equivalent
        del data[0:2]  # remove attributes_count data from the hex-dump

        if self.write:   # if write operations are specified, write the data
            store_attributes_count = open((self.classfile_dir + "/attributes_count.txt"), "w")  # store attributes_count data
            store_attributes_count.write(str(self.a_count))  # this data is used by another python script
            store_attributes_count.close()

    def attributes(self):
        global data

        a_count = self.a_count
        while a_count != 0:

            attribute_info(self.constant_pool_data, self.classfile_dir, self.verbose, self.write)

            a_count = a_count - 1

        if len(data) == 0:
            print("Complete")
        else:
            print("Error: Remnant Data")

# attribute_info--------------------------------------------------------------------------------------------------------
# The attribute_info structures within the java bytecode are integrated into multiple sections, and essentially it
# is the first point at which the abstract nature and redundancy within the bytecode becomes recognizable. To avoid
# that redundancy becoming a part of the disassembler, it has to be compartmentalized into its own class where it can
# be defined in a general sense and called upon when necessary.

class attribute_info:

    # Certain attributes such as the "Deprecated" Attribute are represented solely by the attribute_name_index and
    # attribute_length. As such, they are not explicitly described by any method within this class.

    def __init__(self, constant_pool, storage, verbose, write):
        global data
        global glob_path

        # The following variables are made globally accessible within the class because of the fact that certain
        # attributes can contain nested attribute_info structures within themseleves. In those cases, the superclass
        # creates an instance of itself that is initialized with the data that was originally passed to it.
        self.storage = storage   # this variable holds the pathway that is used to write the attribute data to text files
        self.constant_pool = constant_pool

        self.write = write
        self.verbose = verbose

        # the attribute name index gives the index into the constant pool that describes the type of attribute that follows

        attribute_name_index = data[0] + data[1]
        attribute_name_index = int(attribute_name_index, 16)
        del data[0:2]

        attribute_length = data[0] + data[1] + data[2] + data[3]  # length of the attribute in bytes (excluding the name_index and the length itself)
        attribute_length = int(attribute_length, 16)
        del data[0:4]

        attribute_type = constant_pool[attribute_name_index][2]  # get the attribute type from the constant pool

        # The processing of the attribute info structures are self-contained to prevent cascading errors within the
        # disassembler.
        if attribute_type == "Signature":  # if the attribute type is "Signature" the associated method is called
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            self.attribute_signature(storage)
        elif attribute_type == "Deprecated":  # if the attribute type is "Deprecated" the attrib_length is checked
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            if attribute_length != 0:
                print("ERROR: Attribute - Deprecated - length is greater than 0 bytes")
        elif attribute_type == "ConstantValue":
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            self.attribute_constantvalue(storage)
        elif (attribute_type == "RuntimeVisibleAnnotations") or (attribute_type == "RuntimeInvisibleAnnotations"):
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            runtime_visible_annotations = attribute_info.annotations()
            runtime_visible_annotations.attribute_runtimevisibleannotations()
        elif (attribute_type == "RuntimeVisibleParameterAnnotations") or (attribute_type == "RuntimeInvisibleParameterAnnotations"):
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            RVPA = attribute_info.annotations()
            RVPA.attribute_runtimeparameterannotations()
        elif (attribute_type == "RuntimeVisibleTypeAnnotations") or (attribute_type == "RuntimeInvisibleTypeAnnotations"):
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            RVTA = attribute_info.annotations()
            RVTA.attribute_runtimetypeannotations()
        elif attribute_type == "AnnotationDefault":
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            AD = attribute_info.annotations()
            AD.attribute_annotationdefault()
        elif attribute_type == "SourceFile":
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            self.attribute_sourcefile(storage)
        elif attribute_type == "Exceptions":
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            self.attribute_exceptions(storage)
        elif attribute_type == "InnerClasses":
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            self.attribute_innerclasses(storage)
        elif attribute_type == "BootstrapMethods":
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            self.attribute_bootstrapmethods(storage)
        elif attribute_type == "Code":
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            self.attribute_code(storage)
        elif attribute_type == "LineNumberTable":
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            self.attribute_linenumbertable(storage)
        elif attribute_type == "LocalVariableTable":
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            self.attribute_localvariabletable(storage)
        elif attribute_type == "LocalVariableTypeTable":
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            self.attribute_localvariabletypetable(storage)
        elif attribute_type == "StackMapTable":
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            attribute_info.attribute_stackmaptable(storage, write)
        elif attribute_type == "EnclosingMethod":
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            self.attribute_enclosingmethod(storage)
        elif attribute_type == "Synthetic":
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
        elif attribute_type == "SourceDebugExtension":
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            self.attribute_sourcedebugextension(attribute_length, storage)
        elif attribute_type == "MethodParameters":
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            self.attribute_methodparameters(storage)
        elif attribute_type == "Module":
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            self.attribute_module(storage)
        elif attribute_type == "ModulePackages":
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            self.attribute_modulepackages(storage)
        elif attribute_type == "ModuleMainClass":
            MMC = open("module_main_class.txt", 'a')
            MMC.write(glob_path + "\n")
            MMC.close()
            del data[0:attribute_length]
        elif attribute_type == "NestHost":
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            self.attribute_nesthost(storage)
        elif attribute_type == "NestMembers":
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            self.attribute_nestmembers(storage)
        elif attribute_type == "Record":
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            self.attribute_record(storage)
        elif attribute_type == "PermittedSubclasses":
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))
            self.attribute_permittedsubclasses(storage)
        else:
            del data[0:attribute_length]
            UiD = open("UnidentifiedAttribute.txt", 'a')
            UiD.write(glob_path + "\n")
            UiD.close()
            if verbose:
                print("\t" + str(constant_pool[attribute_name_index]))

    def attribute_signature(self, pathway):
        global data
        # The signature is a fixed length attribute. It occupies a total of two bytes.

        signature_index = data[0] + data[1]
        signature_index = int(signature_index, 16)
        del data[0:2]

        if self.write:
            write_signature = open((pathway + "/signatures.txt"), 'a')
            write_signature.write(str(signature_index) + "\n")
            write_signature.close()

    def attribute_constantvalue(self, pathway):
        global data
        # The constant_value attribute is of fixed length. It occupies a total of two bytes

        constant_value_index = data[0] + data[1]
        constant_value_index = int(constant_value_index, 16)
        del data[0:2]

        if self.write:
            write_constant = open((pathway + "/constant_values.txt"), 'a')
            write_constant.write(str(constant_value_index) + "\n")
            write_constant.close()


    def attribute_sourcefile(self, pathway):
        global data
        # The sourcefile attribute is an optional fixed-length attribute. It contains the index to a string representing
        # the name of the sourcefile.

        sourcefile_index = data[0] + data[1]
        sourcefile_index = int(sourcefile_index, 16)
        del data[0:2]

        if self.write:
            write_sfileindex = open((pathway + "/sourcefile_index.txt"), 'a')
            write_sfileindex.write(str(sourcefile_index) + "\n")
            write_sfileindex.close()

    def attribute_exceptions(self, pathway):
        global data

        number_of_exceptions = data[0] + data[1]
        number_of_exceptions = int(number_of_exceptions, 16)
        del data[0:2]

        exceptions = [number_of_exceptions]

        while number_of_exceptions != 0:
            exception = data[0] + data[1]
            exception = int(exception, 16)
            del data[0:2]

            exceptions.append(exception)

            number_of_exceptions = number_of_exceptions - 1

        # write operations for attribute_exceptions
        if self.write:
            write_except = open(pathway + "/exceptions.txt", 'a')
            for item in exceptions:
                write_except.write(str(item) + "\n")
            write_except.close()


    def attribute_innerclasses(self, pathway):
        global data

        # The inner classes attribute - as the name suggests - only exists when there are inner classes. The following
        # information gives the necessary indexes for the JVM to access each inner class.

        # Note: This method may require additional testing

        number_of_classes = data[0] + data[1]
        number_of_classes = int(number_of_classes, 16)
        del data[0:2]
        inner_classes = [str(number_of_classes), "\n"]

        class_count = 1
        while number_of_classes != 0:
            inner_class_info_index = data[0] + data[1]
            inner_class_info_index = int(inner_class_info_index, 16)
            del data[0:2]
            inner_classes.append(str(inner_class_info_index) + ",")

            outer_class_info_index = data[0] + data[1]
            outer_class_info_index = int(outer_class_info_index, 16)
            del data[0:2]
            inner_classes.append(str(outer_class_info_index) + ",")

            inner_name_index = data[0] + data[1]
            inner_name_index = int(inner_name_index, 16)
            del data[0:2]
            inner_classes.append(str(inner_name_index) + ",")

            inner_class_access_flags = data[0] + data[1]
            del data[0:2]
            inner_classes.append(inner_class_access_flags)
            inner_classes.append("\n")

            class_count = class_count + 1
            number_of_classes = number_of_classes - 1

        if self.write:
            write_ic = open(pathway + "/inner_classes.txt", 'w')
            for item in inner_classes:
                write_ic.write(item)
            write_ic.close()


    def attribute_bootstrapmethods(self, pathway):
        global data

        # There is never more than one bootstrapmethods attribute in the attributes table of any given class file. The
        # following method has been tested and should run correctly in every operation.

        num_bootstrap_methods = data[0] + data[1]
        num_bootstrap_methods = int(num_bootstrap_methods, 16)
        del data[0:2]

        bootstrap_methods = [num_bootstrap_methods]

        method_count = 1
        while num_bootstrap_methods != 0:
            bootstrap_method_ref = data[0] + data[1]
            bootstrap_method_ref = int(bootstrap_method_ref, 16)
            del data[0:2]
            bootstrap_methods.append(bootstrap_method_ref)

            num_bootstrap_arguments = data[0] + data[1]
            num_bootstrap_arguments = int(num_bootstrap_arguments, 16)
            del data[0:2]
            bootstrap_methods.append(num_bootstrap_arguments)

            while num_bootstrap_arguments != 0:
                bootstrap_argument = data[0] + data[1]
                bootstrap_argument = int(bootstrap_argument, 16)
                del data[0:2]
                bootstrap_methods.append(bootstrap_argument)

                num_bootstrap_arguments = num_bootstrap_arguments - 1

            method_count = method_count + 1
            num_bootstrap_methods = num_bootstrap_methods - 1

        # write operations for bootstrap methods
        if self.write:
            write_bsp = open(pathway + "/bootstrap_methods.txt", 'w')
            for item in bootstrap_methods:
                write_bsp.write(str(item) + "\n")
            write_bsp.close()

    def attribute_enclosingmethod(self, pathway):
        global data

        class_index = data[0] + data[1]
        class_index = int(class_index, 16)
        del data[0:2]

        method_index = data[0] + data[1]
        method_index = int(method_index, 16)
        del data[0:2]

        if self.write:
            write_em = open(pathway + "/enclosing_method.txt", 'w')
            write_em.write(str(class_index) + "\n")
            write_em.write(str(method_index))
            write_em.close()

    def attribute_nesthost(self, pathway):
        global data

        host_class_index = data[0] + data[1]
        host_class_index = int(host_class_index, 16)
        del data[0:2]

        if self.write:
            write_hci = open(pathway + "/nest_host.txt", 'w')
            write_hci.write(str(host_class_index))
            write_hci.close()

    def attribute_nestmembers(self, pathway):
        global data

        number_of_classes = data[0] + data[1]
        number_of_classes = int(number_of_classes, 16)
        del data[0:2]

        nest_members = [number_of_classes]

        while number_of_classes != 0:
            classes = data[0] + data[1]
            classes = int(classes, 16)
            del data[0:2]
            nest_members.append(classes)
            number_of_classes = number_of_classes - 1

        # write operations for attribute_nestmembers
        if self.write:
            write_nm = open(pathway + "/nest_members.txt", 'w')
            for item in nest_members:
                write_nm.write(str(item) + "\n")
            write_nm.close()

    def attribute_permittedsubclasses(self, pathway):
        global data

        number_of_classes = data[0] + data[1]
        number_of_classes = int(number_of_classes, 16)
        del data[0:2]
        permitted_subclasses = [number_of_classes]

        while number_of_classes != 0:
            classes = data[0] + data[1]
            classes = int(classes, 16)
            del data[0:2]
            permitted_subclasses.append(classes)

            number_of_classes = number_of_classes - 1

        if self.write:
            write_ps = open(pathway + "/permitted_subclasses.txt", 'a')
            for item in permitted_subclasses:
                write_ps.write(str(item) + "\n")
            write_ps.close()


    def attribute_record(self, pathway):
        global data

        components_count = data[0] + data[1]
        components_count = int(components_count, 16)
        del data[0:2]
        record = [components_count]

        while components_count != 0:
            name_index = data[0] + data[1]
            name_index = int(name_index, 16)
            del data[0:2]
            record.append(name_index)

            descriptor_index = data[0] + data[1]
            descriptor_index = int(descriptor_index, 16)
            del data[0:2]
            record.append(descriptor_index)

            attributes_count = data[0] + data[1]
            attributes_count = int(attributes_count, 16)
            del data[0:2]
            record.append(attributes_count)

            while attributes_count != 0:
                attribute_info(self.constant_pool, pathway, self.verbose, self.write)
                attributes_count = attributes_count - 1

            components_count = components_count - 1

        if self.write:
            write_record = open(pathway + "/record.txt", 'w')
            for item in record:
                write_record.write(str(item) + "\n")
            write_record.close()


    def attribute_methodparameters(self, pathway):
        global data

        parameters_count = data[0]
        parameters_count = int(parameters_count, 16)
        del data[0]
        methodparameters = [parameters_count]

        while parameters_count != 0:
            name_index = data[0] + data[1]
            name_index = int(name_index, 16)
            del data[0:2]
            methodparameters.append(name_index)

            access_flags = data[0] + data[1]
            del data[0:2]
            methodparameters.append(access_flags)

            parameters_count = parameters_count - 1

        if self.write:
            write_mp = open(pathway + "/method_parameters.txt", 'w')
            for item in methodparameters:
                write_mp.write(str(item) + "\n")
            write_mp.close()

    def attribute_modulepackages(self, pathway):
        global data

        package_count = data[0] + data[1]
        package_count = int(package_count, 16)
        del data[0:2]
        modulepackages= [package_count]

        while package_count != 0:
            package_index = data[0] + data[1]
            package_index = int(package_index, 16)
            del data[0:2]
            modulepackages.append(package_index)

            package_count = package_count - 1

        if self.write:
            write_mp = open(pathway + "/module_packages.txt", 'w')
            for item in modulepackages:
                write_mp.write(str(item) + "\n")
            write_mp.close()


    def attribute_module(self, pathway):
        global data

        module_name_index = data[0] + data[1]
        module_name_index = int(module_name_index, 16)
        del data[0:2]
        module = [module_name_index]

        module_flags = data[0] + data[1]
        del data[0:2]
        module.append(module_flags)

        module_version_index = data[0] + data[1]
        module_version_index = int(module_version_index, 16)
        del data[0:2]
        module.append(module_version_index)

        requires_count = data[0] + data[1]
        requires_count = int(requires_count, 16)
        del data[0:2]
        module.append(requires_count)

        while requires_count != 0:
            requires_index = data[0] + data[1]
            requires_index = int(requires_index, 16)
            del data[0:2]
            module.append(requires_index)

            requires_flags = data[0] + data[1]
            del data[0:2]
            module.append(requires_flags)

            requires_version_index = data[0] + data[1]
            requires_version_index = int(requires_version_index, 16)
            del data[0:2]
            module.append(requires_version_index)

            requires_count = requires_count - 1

        exports_count = data[0] + data[1]
        exports_count = int(exports_count, 16)
        del data[0:2]
        module.append(exports_count)

        while exports_count != 0:
            exports_index = data[0] + data[1]
            exports_index = int(exports_index, 16)
            del data[0:2]
            module.append(exports_index)

            exports_flags = data[0] + data[1]
            del data[0:2]
            module.append(exports_flags)

            exports_to_count = data[0] + data[1]
            exports_to_count = int(exports_to_count, 16)
            del data[0:2]
            module.append(exports_to_count)

            while exports_to_count != 0:
                exports_to_index = data[0] + data[1]
                exports_to_index = int(exports_to_index, 16)
                del data[0:2]
                module.append(exports_to_index)

                exports_to_count = exports_to_count - 1

            exports_count = exports_count - 1

        opens_count = data[0] + data[1]
        opens_count = int(opens_count, 16)
        del data[0:2]
        module.append(opens_count)

        while opens_count != 0:
            opens_index = data[0] + data[1]
            opens_index = int(opens_index, 16)
            del data[0:2]
            module.append(opens_index)

            opens_flags = data[0] + data[1]
            del data[0:2]
            module.append(opens_flags)

            opens_to_count = data[0] + data[1]
            opens_to_count = int(opens_to_count, 16)
            del data[0:2]
            module.append(opens_to_count)

            while opens_to_count != 0:
                opens_to_index = data[0] + data[1]
                opens_to_index = int(opens_to_index, 16)
                del data[0:2]
                module.append(opens_to_index)

                opens_to_count = opens_to_count - 1

            opens_count = opens_count - 1

        uses_count = data[0] + data[1]
        uses_count = int(uses_count, 16)
        del data[0:2]
        module.append(uses_count)

        while uses_count != 0:
            uses_index = data[0] + data[1]
            uses_index = int(uses_index, 16)
            del data[0:2]
            module.append(uses_index)

            uses_count = uses_count - 1

        provides_count = data[0] + data[1]
        provides_count = int(provides_count, 16)
        del data[0:2]
        module.append(provides_count)

        while provides_count != 0:
            provides_index = data[0] + data[1]
            provides_index = int(provides_index, 16)
            del data[0:2]
            module.append(provides_index)

            provides_with_count = data[0] + data[1]
            provides_with_count = int(provides_with_count, 16)
            del data[0:2]
            module.append(provides_with_count)

            while provides_with_count != 0:
                provides_with_index = data[0] + data[1]
                provides_with_index = int(provides_with_index, 16)
                del data[0:2]
                module.append(provides_with_index)

                provides_with_count = provides_with_count - 1

            provides_count = provides_count - 1

        if self.write:
            write_mod = open(pathway + "/module.txt", "w")
            for item in module:
                write_mod.write(str(item) + "\n")
            write_mod.close()
    
    def attribute_sourcedebugextension(self, attribute_length, pathway):
        global data

        sde = []
        while attribute_length != 0:
            debug_extension = data[0]
            debug_extension = int(debug_extension, 16)
            del data[0]
            sde.append(debug_extension)
            attribute_length = attribute_length - 1

        if self.write:
            write_sde = open(pathway + "/source_debug_extension.txt", "w")
            for item in sde:
                write_sde.write(str(item) + "\n")
            write_sde.close()

    def attribute_code(self, pathway):
        global data

        # The code attribute can have multiple attributes of the same type attached to it. The following globals are
        # used to keep track of each of these attribute so that they can be written to a unique file.
        global linenumbertable_count
        linenumbertable_count = 0

        global localvariabletable_count
        localvariabletable_count = 0

        global lvtt_count
        lvtt_count = 0

        # The list of 2d arrays below describe the JAVA bytecode operators alongside their hexadecimal opcodes.
        # The data is used to create a human readable version of the opcode logic similar to the javap output.

        Constants = [["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "0a",
                      "0b", "0c", "0d", "0e", "0f", "10", "11", "12", "13", "14"],
                     ["nop", "aconst_null", "iconst_ml", "iconst_0", "iconst_1", "iconst_2", "iconst_3",
                      "iconst_4", "iconst_5", "lconst_0", "lconst_1", "fconst_0", "fconst_1", "fconst_2",
                      "dconst_0", "dconst_1", "bipush", "sipush", "ldc", "ldc_w", "ldc2_w"]]

        Loads = [["15", "16", "17", "18", "19", "1a", "1b", "1c", "1d", "1e", "1f", "20",
                  "21", "22", "23", "24", "25", "26", "27", "28", "29", "2a", "2b", "2c",
                  "2d", "2e", "2f", "30", "31", "32", "33", "34", "35"],
                 ["iload", "lload", "fload", "dload", "aload", "iload_0", "iload_1", "iload_2",
                  "iload_3", "lload_0", "lload_1", "lload_2", "lload_3", "fload_0", "fload_1",
                  "fload_2", "fload_3", "dload_0", "dload_1", "dload_2", "dload_3", "aload_0",
                  "aload_1", "aload_2", "aload_3", "iaload", "laload", "faload", "daload", "aaload",
                  "baload", "caload", "saload"]]

        Stores = [["36", "37", "38", "39", "3a", "3b", "3c", "3d", "3e", "3f", "40", "41",
                   "42", "43", "44", "45", "46", "47", "48", "49", "4a", "4b", "4c", "4d",
                   "4e", "4f", "50", "51", "52", "53", "54", "55", "56"],
                  ["istore", "lstore", "fstore", "dstore", "astore", "istore_0", "istore_1", "istore_2",
                   "istore_3", "lstore_0", "lstore_1", "lstore_2", "lstore_3", "fstore_0", "fstore_1",
                   "fstore_2", "fstore_3", "dstore_0", "dstore_1", "dstore_2", "dstore_3", "astore_0",
                   "astore_1", "astore_2", "astore_3", "iastore", "lastore", "fastore", "dastore", "aastore",
                   "bastore", "castore", "sastore"]]

        Stack = [["57", "58", "59", "5a", "5b", "5c", "5d", "5e", "5f"],
                 ["pop", "pop2", "dup", "dux_x1", "dup_x2", "dup2", "dup2_x1", "dup2_x2", "swap"]]

        Math = [["60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "6a", "6b",
                 "6c", "6d", "6e", "6f", "70", "71", "72", "73", "74", "75", "76", "77",
                 "78", "79", "7a", "7b", "7c", "7d", "7e", "7f", "80", "81", "82", "83",
                 "84"],
                ["iadd", "ladd", "fadd", "dadd", "isub", "lsub", "fsub", "dsub", "imul", "lmul",
                 "fmul", "dmul", "idiv", "ldiv", "fdiv", "ddiv", "irem", "lrem", "frem", "drem",
                 "ineg", "fneg", "lneg", "dneg", "ishl", "lshl", "ishr", "lshr", "iushr", "lushr",
                 "iand", "land", "ior", "lor", "ixor", "lxor", "iinc"]]

        Conversions = [["85", "86", "87", "88", "89", "8a", "8b", "8c", "8d", "8e", "8f", "90", "91", "92", "93"],
                       ["i2l", "i2f", "i2d", "l2i", "l2f", "l2d", "f2i", "f2l", "f2d", "d2i", "d2l", "d2f", "i2b",
                        "i2c", "i2s"]]

        Comparisons = [["94", "95", "96", "97", "98", "99", "9a", "9b", "9c", "9d", "9e", "9f",
                        "a0", "a1", "a2", "a3", "a4", "a5", "a6"],
                       ["lcmp", "fcmpl", "fcmpg", "dcmpl", "dcmpg", "ifeq", "ifne", "iflt", "ifge", "ifgt", "ifle",
                        "if_icmpeq", "if_icmpne", "if_icmplt", "if_icmpge", "if_icmpgt", "if_icmple",
                        "if_acmpeq", "if_acmpne"]]

        Control = [["a7", "a8", "a9", "aa", "ab", "ac", "ad", "ae", "af", "b0", "b1"],
                   ["goto", "jsr", "ret", "tableswitch", "lookupswitch", "ireturn", "lreturn", "freturn",
                    "dreturn", "areturn", "return", ]]

        References = [["b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9", "ba", "bb", "bc", "bd", "be", "bf", "c0",
                       "c1", "c2", "c3", ],
                      ["getstatic", "putstatic", "getfield", "putfield", "invokevirtual", "invokespecial",
                       "invokestatic", "invokeinterface", "invokedynamic", "new", "newarray", "anewarray",
                       "arraylength", "athrow", "checkcast", "instanceof", "monitorenter", "monitorexit"]]

        Extended = [["c4", "c5", "c6", "c7", "c8", "c9"],
                    ["wide", "multianewarray", "ifnull", "ifnonull", "goto_w", "jsr_w"]]

        Reserved = [["ca", "fe", "ff"],
                    ["breakpoint", "impdep1", "impdep2"]]


        max_stack = data[0] + data[1]   # the maximum depth of the operand stack
        max_stack = int(max_stack, 16)
        del data[0:2]

        max_locals = data[0] + data[1]  # the total number of local variable used in the method
        max_locals = int(max_locals, 16)
        del data[0:2]

        code_length = data[0] + data[1] + data[2] + data[3] # The length in bytes of the code for this method.
        code_length = int(code_length, 16)                  # Note: the code length includes the bytes for the data
        del data[0:4]                                       # associated with the code attribute itself; i.e. the "line
                                                            # number table", "local variable table" and "stack map
                                                            # table".
        store_codelength = code_length
        code = []   # array used to store bytecode opcodes
        while code_length != 0:
            # get the human-readable opcode associated with the hexadecimal value

            for opcode in Constants[0]:
                if opcode == data[0]:
                    index = Constants[0].index(opcode)
                    code.append(Constants[1][index])

            for opcode in Loads[0]:
                if opcode == data[0]:
                    index = Loads[0].index(opcode)
                    code.append(Loads[1][index])

            for opcode in Stores[0]:
                if opcode == data[0]:
                    index = Stores[0].index(opcode)
                    code.append(Stores[1][index])

            for opcode in Stack[0]:
                if opcode == data[0]:
                    index = Stack[0].index(opcode)
                    code.append(Stack[1][index])

            for opcode in Math[0]:
                if opcode == data[0]:
                    index = Math[0].index(opcode)
                    code.append(Math[1][index])

            for opcode in Conversions[0]:
                if opcode == data[0]:
                    index = Conversions[0].index(opcode)
                    code.append(Conversions[1][index])

            for opcode in Comparisons[0]:
                if opcode == data[0]:
                    index = Comparisons[0].index(opcode)
                    code.append(Comparisons[1][index])

            for opcode in Control[0]:
                if opcode == data[0]:
                    index = Control[0].index(opcode)
                    code.append(Control[1][index])

            for opcode in References[0]:
                if opcode == data[0]:
                    index = References[0].index(opcode)
                    code.append(References[1][index])

            for opcode in Extended[0]:
                if opcode == data[0]:
                    index = Extended[0].index(opcode)
                    code.append(Extended[1][index])

            for opcode in Reserved[0]:
                if opcode == data[0]:
                    index = Reserved[0].index(opcode)
                    code.append(Reserved[1][index])

            del data[0]

            code_length = code_length - 1

        exception_table_length = data[0] + data[1]
        exception_table_length = int(exception_table_length, 16)
        del data[0:2]

        store_exceptiontablelength = exception_table_length
        exception_tables = []  # array used to store exception tables
        while exception_table_length != 0:

            start_pc = data[0] + data[1]
            start_pc = int(start_pc, 16)
            del data[0:2]

            end_pc = data[0] + data[1]
            end_pc = int(end_pc, 16)
            del data[0:2]

            handler_pc = data[0] + data[1]
            handler_pc = int(handler_pc, 16)
            del data[0:2]

            catch_type = data[0] + data[1]
            catch_type = int(catch_type, 16)
            del data[0:2]

            exception_tables.append([start_pc, end_pc, handler_pc, catch_type])
            exception_table_length = exception_table_length - 1

        attributes_count = data[0] + data[1]   # the number of attributes attached to this code attribute specificaly
        attributes_count = int(attributes_count, 16)
        del data[0:2]

        if self.write:
            # create unique code directory
            global code_count
            code_count = code_count + 1
            code_dir = pathway + "/code_" + str(code_count)
            os.mkdir(code_dir)

            # write code data to file
            write_code = open(code_dir + "/code.txt", 'w')
            write_code.write(str(max_stack) + "\n")
            write_code.write(str(max_locals) + "\n")
            write_code.write(str(store_codelength) + "\n")
            for opcode in code:
                write_code.write(str(opcode) + "\n")
            write_code.write(str(store_exceptiontablelength) + "\n")
            for table in exception_tables:
                write_code.write(str(table[0]) + "," + str(table[1]) + "," + str(table[2]) + "," + str(table[3]) + "\n")
            write_code.write(str(attributes_count))
            write_code.close()
        else:
            code_dir = None

        # processed the attributes attached to this code attribute
        while attributes_count != 0:
            attribute_info(self.constant_pool, code_dir, self.verbose, self.write)
            attributes_count = attributes_count - 1

    def attribute_linenumbertable(self, pathway):
        global data

        line_number_table_length = data[0] + data[1]
        line_number_table_length = int(line_number_table_length, 16)
        del data[0:2]

        line_number_table = [line_number_table_length]
        while line_number_table_length != 0:
            start_pc = data[0] + data[1]
            start_pc = int(start_pc, 16)
            del data[0:2]

            line_number = data[0] + data[1]
            line_number = int(line_number, 16)
            del data[0:2]

            line_number_table.append([start_pc, line_number])

            line_number_table_length = line_number_table_length - 1

        if self.write:
            global linenumbertable_count

            # According to the JAVA spec, a code attribute may have multiple line number tables. A unique entry is created
            # for each of them using the global "linenumbertable_count".
            lnt_path = pathway + "/linenumbertable_" + str(linenumbertable_count) + ".txt"
            linenumbertable_count = linenumbertable_count + 1

            write_lnt = open(lnt_path, 'w')
            for item in line_number_table:
                if isinstance(item, list):
                    for stuff in item:
                        write_lnt.write(str(stuff) + ",")
                    write_lnt.write("\n")
                else:
                    write_lnt.write(str(item) + "\n")
            write_lnt.close()


    def attribute_localvariabletable(self, pathway):
        global data

        local_variable_table_length = data[0] + data[1]
        local_variable_table_length = int(local_variable_table_length, 16)
        del data[0:2]

        local_variable_table = [local_variable_table_length]

        while local_variable_table_length != 0:
            start_pc = data[0] + data[1]
            start_pc = int(start_pc, 16)
            del data[0:2]

            length = data[0] + data[1]
            length = int(length, 16)
            del data[0:2]

            name_index = data[0] + data[1]
            name_index = int(name_index, 16)
            del data[0:2]

            descriptor_index = data[0] + data[1]
            descriptor_index = int(descriptor_index, 16)
            del data[0:2]

            index = data[0] + data[1]
            index = int(index, 16)
            del data[0:2]

            local_variable_table.append([start_pc, length, name_index, descriptor_index, index])

            local_variable_table_length = local_variable_table_length - 1

        # write operations for local variable table
        if self.write:
            global localvariabletable_count  # global variable for keeping track of each local variable table and its associated Code

            lvt_path = pathway + "/localvariabletable_" + str(localvariabletable_count) + ".txt"
            write_lvt = open(lvt_path, 'w')
            localvariabletable_count = localvariabletable_count + 1

            for item in local_variable_table:
                if isinstance(item, list):
                    for stuff in item:
                        write_lvt.write(str(stuff) + ",")
                    write_lvt.write("\n")
                else:
                    write_lvt.write(str(item) + "\n")

            write_lvt.close()

    def attribute_localvariabletypetable(self, pathway):
        global data

        lvtt_length = data[0] + data[1]
        lvtt_length = int(lvtt_length, 16)
        del data[0:2]

        local_variable_type_table = [lvtt_length]

        while lvtt_length != 0:
            start_pc = data[0] + data[1]
            start_pc = int(start_pc, 16)
            del data[0:2]

            length = data[0] + data[1]
            length = int(length, 16)
            del data[0:2]

            name_index = data[0] + data[1]
            name_index = int(name_index, 16)
            del data[0:2]

            signature_index = data[0] + data[1]
            signature_index = int(signature_index, 16)
            del data[0:2]

            index = data[0] + data[1]
            index = int(index, 16)
            del data[0:2]

            local_variable_type_table.append([start_pc, length, name_index, signature_index, index])

            lvtt_length = lvtt_length - 1

        # write operations for local variable type table
        if self.write:
            global lvtt_count

            lvtt_path = pathway + "/localvariabletypetable_" + str(lvtt_count) + ".txt"
            write_lvtt = open(lvtt_path, 'w')
            lvtt_count = lvtt_count + 1

            for item in local_variable_type_table:
                if isinstance(item, list):
                    for stuff in item:
                        write_lvtt.write(str(stuff) + ",")
                    write_lvtt.write("\n")
                else:
                    write_lvtt.write(str(item) + "\n")

            write_lvtt.close()


    class attribute_stackmaptable:
        def __init__(self, pathway, write):
            global data

            # number of entries in the stack_map_table
            number_of_entries = data[0] + data[1]
            number_of_entries = int(number_of_entries, 16)
            del data[0:2]

            stack_map_table = [str(number_of_entries)]

            # Note: not all Java compilers use stack_map_tables. Typically, they are found in the newer versions

            while number_of_entries != 0:  # major loop for identifying each frame within the stack_map_table

                stack_map_frame = data[0]  # the type of stack_map_frame is given by one byte of data
                stack_map_frame = int(stack_map_frame, 16)  # convert hex to integer
                del data[0]  # remove the data from the data[] array

                # Stack-Map-Frames are identified by a unique integer between 0-255. This section identifies the type of
                # Stack-Map-Frame and processes it accordingly. Note: Certain frames contain unique structures known as
                # "verification_type_info" structures; they are processed separately in another method to minimize
                # redundancy in the code.
                if (stack_map_frame >= 0) and (stack_map_frame <= 63):
                    stack_map_table.append("same_frame\n")
                elif (stack_map_frame >= 64) and (stack_map_frame <= 127):
                    stack_map_table.append("same_locals_1_stack_item_frame\n")
                    vti = self.verification_type_info()
                    for item in vti:
                        stack_map_table.append(str(item) + "-")
                    stack_map_table.append("\n")
                elif (stack_map_frame == 247):
                    stack_map_table.append("same_locals_1_stack_item_frame_extended")
                    offset_delta = data[0] + data[1]
                    del data[0:2]
                    stack_map_table.append(offset_delta + "\n")
                    vti = self.verification_type_info()
                    for item in vti:
                        stack_map_table.append(str(item) + "-")
                    stack_map_table.append("\n")
                elif (stack_map_frame >= 248) and (stack_map_frame <= 250):
                    stack_map_table.append("chop_frame\n")
                    offset_delta = data[0] + data[1]
                    del data[0:2]
                    stack_map_table.append(offset_delta + "\n")
                elif (stack_map_frame == 251):
                    stack_map_table.append("same_frame_extended\n")
                    offset_delta = data[0] + data[1]
                    del data[0:2]
                    stack_map_table.append(offset_delta + "\n")
                elif (stack_map_frame >= 252) and (stack_map_frame <= 254):
                    stack_map_table.append("append_frame\n")
                    offset_delta = data[0] + data[1]
                    del data[0:2]
                    stack_map_table.append(str(offset_delta) + "\n")

                    number_of_locals = stack_map_frame - 251
                    while number_of_locals != 0:
                        vti = self.verification_type_info()
                        for item in vti:
                            stack_map_table.append(str(item) + "-")
                        stack_map_table.append("\n")
                        number_of_locals = number_of_locals - 1

                elif (stack_map_frame == 255):
                    stack_map_table.append("full_frame\n")
                    offset_delta = data[0] + data[1]
                    del data[0:2]
                    stack_map_table.append(str(offset_delta) + "\n")

                    number_of_locals = data[0] + data[1]
                    number_of_locals = int(number_of_locals, 16)
                    del data[0:2]
                    stack_map_table.append(str(number_of_locals) + "\n")

                    while number_of_locals != 0:
                        vti = self.verification_type_info()
                        for locals in vti:
                            stack_map_table.append(str(locals) + "-")
                        stack_map_table.append("\n")
                        number_of_locals = number_of_locals - 1

                    number_of_stack_items = data[0] + data[1]
                    number_of_stack_items = int(number_of_stack_items, 16)
                    del data[0:2]
                    stack_map_table.append(str(number_of_stack_items) + "\n")

                    while number_of_stack_items != 0:
                        vti = self.verification_type_info()
                        for stacks in vti:
                            stack_map_table.append(str(stacks) + "-")
                        stack_map_table.append("\n")
                        number_of_stack_items = number_of_stack_items - 1

                number_of_entries = number_of_entries - 1

            # Since the stack_map_table attribute is handled within its own class, the write function has to be passed
            # in maunally when the class is called. The write operations are handled below.
            if write:
                smt_path = pathway + "/stackmaptable.txt"
                write_smt = open(smt_path, 'w')
                for item in stack_map_table:
                    write_smt.write(item)
                write_smt.close()

        def verification_type_info(self):
            global data

            v_type = data[0]
            v_type = int(v_type, 16)
            del data[0]
            v_t_i = [v_type]

            if v_type == 7:
                cpool_index = data[0] + data[1]
                del data[0:2]
                v_t_i.append(cpool_index)
            elif v_type == 8:
                offset = data[0] + data[1]
                del data[0:2]
                v_t_i.append(offset)

            return v_t_i

    class annotations:

        def attribute_annotationdefault(self):
            global data

            # The annotation default attribute is the same as the element_value structure outlined in
            # the JVM classfile specifications
            default_value = attribute_info.annotations()
            default_value.element_value_structure()


        def attribute_runtimetypeannotations(self):
            global data

            type_parameter_target = ["00", "01"]
            supertype_target = "10"
            type_parameter_bound_target = ["11", "12"]
            empty_target = ["13", "14", "15"]
            formal_parameter_target = "16"
            throws_target = "17"
            localvar_target = ["40", "41"]
            catch_target = "42"
            offset_target = ["43", "44", "45", "46"]
            type_argument_target = ["47", "48", "49", "4A", "4B"]

            num_annotations = data[0] + data[1]
            num_annotations = int(num_annotations, 16)
            del data[0:2]

            while num_annotations != 0:
                target_type = data[0]
                del data[0]

                for item in type_parameter_target:
                    if item == target_type:
                        type_parameter_index = data[0]
                        type_parameter_index = int(type_parameter_index, 16)
                        del data[0]

                if target_type == supertype_target:
                    supertype_index = data[0] + data[1]
                    supertype_index = int(supertype_index, 16)
                    del data[0:2]

                for item in type_parameter_bound_target:
                    if item == target_type:
                        type_parameter_index = data[0]
                        type_parameter_index = int(type_parameter_index, 16)
                        del data[0]

                        bound_index = data[0]
                        bound_index = int(bound_index, 16)
                        del data[0]

                # the empty target contains no data

                if target_type == formal_parameter_target:
                    formal_parameter_index = data[0]
                    formal_parameter_index = int(formal_parameter_index, 16)
                    del data[0]

                if target_type == throws_target:
                    throws_type_index = data[0] + data[1]
                    throws_type_index = int(throws_type_index, 16)
                    del data[0:2]
                
                if (target_type == localvar_target[0]) or (target_type == localvar_target[1]):
                    table_length = data[0] + data[1]
                    table_length = int(table_length, 16)
                    del data[0:2]

                    while table_length != 0:
                        start_pc = data[0] + data[1]
                        start_pc = int(start_pc, 16)
                        del data[0:2]

                        length = data[0] + data[1]
                        length = int(length, 16)
                        del data[0:2]

                        index = data[0] + data[1]
                        index = int(index, 16)
                        del data[0:2]

                        table_length = table_length - 1

                if target_type == catch_target:
                    exception_table_index = data[0] + data[1]
                    exception_table_index = int(exception_table_index, 16)
                    del data[0:2]

                for item in offset_target:
                    if target_type == item:
                        offset = data[0] + data[1]
                        offset = int(offset, 16)
                        del data[0:2]

                for item in type_argument_target:
                    if target_type == item:
                        offset = data[0] + data[1]
                        offset = int(offset, 16)
                        del data[0:2]

                        type_argument_index = data[0]
                        type_argument_index = int(type_argument_index, 16)
                        del data[0]

                # type path structure
                path_length = data[0]
                path_length = int(path_length, 16)
                del data[0]

                while path_length != 0:
                    type_path_kind = data[0]
                    type_path_kind = int(type_path_kind, 16)
                    del data[0]

                    type_argument_index = data[0]
                    type_argument_index = int(type_argument_index, 16)
                    del data[0]

                    path_length = path_length - 1

                type_index = data[0] + data[1]
                type_index = int(type_index, 16)
                del data[0:2]

                num_element_value_pairs = data[0] + data[1]
                num_element_value_pairs = int(num_element_value_pairs, 16)
                del data[0:2]

                while num_element_value_pairs != 0:

                    element_name_index = data[0] + data[1]
                    element_name_index = int(element_name_index, 16)
                    del data[0:2]

                    element_value = attribute_info.annotations()
                    element_value.element_value_structure()

                    num_element_value_pairs = num_element_value_pairs - 1

                num_annotations = num_annotations - 1


        def attribute_runtimeparameterannotations(self):
            global data
            num_paramters = data[0]
            num_paramters = int(num_paramters, 16)
            del data[0]

            while num_paramters != 0:
                parameter_annotations = attribute_info.annotations()
                parameter_annotations.attribute_runtimevisibleannotations()

                num_paramters = num_paramters - 1


        def attribute_runtimevisibleannotations(self):
            global data

            num_annotations = data[0] + data[1]
            num_annotations = int(num_annotations, 16)
            del data[0:2]

            while num_annotations != 0:
                type_index = data[0] + data[1]
                type_index = int(type_index, 16)
                del data[0:2]

                num_element_value_pairs = data[0] + data[1]
                num_element_value_pairs = int(num_element_value_pairs, 16)
                del data[0:2]

                while num_element_value_pairs != 0:

                    element_name_index = data[0] + data[1]
                    element_name_index = int(element_name_index, 16)
                    del data[0:2]

                    element_value = attribute_info.annotations()
                    element_value.element_value_structure()

                    num_element_value_pairs = num_element_value_pairs - 1

                num_annotations = num_annotations - 1

        # The element value structure is not an attribute itself, but is utilized by multiple attribute types within the
        # classfile. Hence, it is defined in its own method.
        def element_value_structure(self):
            global glob_path
            global data

            consts = ["B", "C", "D", "F", "I", "J", "S", "Z", "s"]

            hex_tag = data[0]
            hex_tag = int(hex_tag, 16)
            tag = chr(hex_tag)
            del data[0]

            if tag == "e":
                type_name_index = data[0] + data[1]
                type_name_index = int(type_name_index, 16)
                del data[0:2]

                const_name_index = data[0] + data[1]
                const_name_index = int(const_name_index, 16)
                del data[0:2]

            elif tag == "c":
                class_info_index = data[0] + data[1]
                class_info_index = int(class_info_index, 16)
                del data[0:2]

            elif tag == "@":
                type_index = data[0] + data[1]
                type_index = int(type_index, 16)
                del data[0:2]

                num_element_value_pairs = data[0] + data[1]
                num_element_value_pairs = int(num_element_value_pairs, 16)
                del data[0:2]

                while num_element_value_pairs != 0:
                    element_name_index = data[0] + data[1]
                    element_name_index = int(element_name_index, 16)
                    del data[0:2]

                    nested_element_value = attribute_info.annotations()
                    nested_element_value.element_value_structure()

                    num_element_value_pairs = num_element_value_pairs - 1

            elif tag == "[":
                num_values = data[0] + data[1]
                num_values = int(num_values, 16)
                del data[0:2]

                while num_values != 0:
                    nested_info = attribute_info.annotations()
                    nested_info.element_value_structure()
                    num_values = num_values - 1

            else:
                for constant in consts:
                    if tag == constant:
                        const_value_index = data[0] + data[1]
                        const_value_index = int(const_value_index, 16)
                        del data[0:2]



#import os
#dir_path = r"RuntimeVisibleTypeAnnotations"
#classlist = []
#for cfile in os.scandir(dir_path):
#    classlist.append(cfile)

#for classfile in classlist:
#    java_bytecode_disassembler(classfile, write=False)

#java_bytecode_disassembler(r"ideaIU-2022.2.3.win\plugins\space\lib\space\circlet\code\review/QualityGateVMImpl.class", verbose=True, write=False, fail_check=False)
