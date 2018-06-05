import os
import subprocess
import inspect
def run_bUnwarpJ():
    ij_dir = r"jars/ij-1.50e.jar"
    bUnwarpJ_dir = r"plugins/bUnwarpJ_-2.6.4-Custom.jar"
    Fiji_dir = r"C:\Program Files (x86)\Fiji.app"
    Landmarks = os.getcwd() + r"tempLandmarks.txt"
    image_SIM_resized = os.getcwd() + r"_resized.tif"
    source = r"C:\Users\biophys\Desktop\Asdf\Trabi_test\20161014_trans_1010a_rh_SIM1_TRABI_3D_complett.png"
    output1 = os.getcwd() + "\output.tif"
    output2 = os.getcwd() + "\output2.tif"
    Flag_align = r"-align " + image_SIM_resized + " NULL " + source +" NULL 0 2 0 0.1 0.1 0 0 "+ output1 + " " + output2
    Flag_Landmarks =  " -landmark 1 " + Landmarks + " "
    Flag_saveTransformation = " -save_transformation"
    command_bUnwarpJ = 'java -Xmx2g -cp "' + ij_dir + '";"' + bUnwarpJ_dir + '" bunwarpj.bUnwarpJ_ '
    command = command_bUnwarpJ + Flag_align + Flag_Landmarks + Flag_saveTransformation
    print(command)
    x = subprocess.check_output(command, cwd= Fiji_dir, shell=True)
    print(x)
#run_bUnwarpJ()

class bUnwarpJPython(object):
    def __init__(self, Fiji_path, target_image, source_image):

        self.fiji_path = Fiji_path
        self.target = target_image
        if (" " in source_image) | (" " in target_image):
            print("Names shouldn't contain whitespace")
        self.source = source_image
        self.bUnwarpJ_path = (os.getcwd()+r"\resources\jars\bUnwarpJ_-2.6.4-SNAPSHOT.jar") #self.find(r"\plugins", "bUnwarpJ")
        #limited to ij 1.5.. because of stupid name
        self.iJ_path = self.find(r"\jars", "ij-1.5")
        print(self.bUnwarpJ_path)
        print(self.iJ_path)
        self.basic_bUnwarpJ_command = 'java -Xmx4g -cp "' + self.iJ_path + '";"' + self.bUnwarpJ_path + '" bunwarpj.bUnwarpJ_ '
        self.command = self.basic_bUnwarpJ_command
        self.bonusFlag = ""
        self.Flag  = ""

    def find(self, subfolder, name):
        dirs = subprocess.check_output("dir", cwd = self.fiji_path + subfolder, shell= True)
        dir_List = dirs.split("\n")
        for dir in dir_List:
            if name in dir:
                fullname = dir.split()[-1]
                extend = fullname.split(".")[-1]
                if extend == "jar":
                    found = fullname

        try:
            found = subfolder + "/" + found
            found = found.split("\\")[1]
            return found
        except:
            print("Critical error bUnwarpJ not found!")
            raise

    def align(self, targetImgMask, sourceImgMask, min_scale_def, max_scale_def, max_subsample_fact, div_weight,
              curl_weight, image_weight, consistency_weight, output1, output2, landmarks = None, affine = None, save_transformation = False, mono = False ):

        args = [self.target, targetImgMask, self.source, sourceImgMask, min_scale_def, max_scale_def, max_subsample_fact, div_weight, curl_weight, image_weight, consistency_weight, output1, output2]
        self.Flag = " -align "
        for arg in args:
            self.Flag += str(arg) + " "
        if landmarks!=None:
            self.bonusFlag += " -landmark 0.8 " + landmarks
        if affine!=None:
            self.bonusFlag += " -affine " + affine[0] + " " * affine[1]
        if save_transformation:
            self.bonusFlag += " -save_transformation "
        if mono:
            self.bonusFlag += " -mono "

    def clear_Flags(self):
        self.Flag = ""
        self.bonusFlag = ""

    def convert_transformation_to_raw(self, tranf_matrix_path, output_path):
        self.clear_Flags()
        args = [self.target, self.source, tranf_matrix_path, output_path]
        self.Flag = " -convert_to_raw "
        for arg in args:
            self.Flag += str(arg)+ " "

    def elastic_transform(self, elastic_transformation_file, output):
        self.Flag = " -" +inspect.stack()[0][3]+ " " + elastic_transformation_file + " " + output
    def raw_transform(self, raw_transformation_file, output):
        self.Flag = " -" +inspect.stack()[0][3]+ " " + raw_transformation_file + " " + output
    def compare_elastic(self, target_transformation_file, source_transformation_file):
        self.Flag = " -" +inspect.stack()[0][3]+ " " + target_transformation_file + " " + source_transformation_file
    def compare_elastic_raw(self, elastic_transformation_file ,raw_transformation_file):
        self.Flag = " -" +inspect.stack()[0][3]+ " " + elastic_transformation_file + " " + raw_transformation_file
    def compare_raw(self, transformation_file1, transformation_file2):
        self.Flag = " -" +inspect.stack()[0][3]+ " " + transformation_file1 + " " + transformation_file2
    def compose_elastic(self, elastic_transformation_file1, elastic_transformation_file2, out_raw_transformation_file ):
        self.Flag = " -" +inspect.stack()[0][3]+ " " + elastic_transformation_file1 + " " + elastic_transformation_file2 + " " + out_raw_transformation_file
    def compose_raw_elastic(self, raw_transformation_file, elastic_transformation_file, out_raw_transformation_file):
        self.Flag = " -" +inspect.stack()[0][3]+ " " + raw_transformation_file + " " + elastic_transformation_file + " " + out_raw_transformation_file
    def adapt_transform(self, in_elastic_transformation_file, out_elastic_transformation_file, image_size_factor):
        self.Flag = " -" +inspect.stack()[0][3]+ " " + in_elastic_transformation_file + " " + out_elastic_transformation_file + " " + image_size_factor




    def run(self):
        command = self.basic_bUnwarpJ_command + self.Flag + self.bonusFlag
        out = subprocess.check_output(command, cwd = self.fiji_path, shell = True)
        print(out)


#bUnwarpJPython(r"C:\Program Files (x86)\Fiji.app")