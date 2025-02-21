import subprocess
import os


def compress(self, file_paths, log):
    dcc_name = self.get_dcc_type(file_paths[0])  # 假设根据第一个文件夹确定 dcc_name
    time = self.get_time()

    # 构建压缩命令
    zip_file_path = f"C:\\Users\\work\\AppData\\Roaming\\RenderCool\\client\\scripts\\{dcc_name}{time}.zip"

    # 使用空格分隔的文件夹路径
    paths_to_compress = ' '.join([f'"{path}"' for path in file_paths])

    command = f'"{self.sevenZ_path}" a "{zip_file_path}" {paths_to_compress} -mx3 -ssw'

    # 执行压缩命令
    compress = subprocess.Popen(command, shell=True)
    compress.wait()  # 等待压缩完成
