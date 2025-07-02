import os
import tempfile

def is_immutable():
    # 执行 deepin-immutable-writable
    return os.system("deepin-immutable-writable status > /dev/null 2>&1") == 0
    

def is_dir_writable(dir_path,sudo=False):
    """
    检测目录是否可写
    通过尝试创建和删除临时文件来测试
    :param dir_path: 要检测的目录路径
    :return: True如果可写，False如果不可写
    """
    try:
        # 生成临时文件名
        test_file = os.path.join(dir_path, tempfile.mktemp(dir='', prefix='.tmp_writable_test_'))
        
        # 测试写入
        write_cmd = f'{"sudo " if sudo else ""}touch "{test_file}"'
        if os.system(write_cmd) != 0:
            return False
            
        # 测试删除
        rm_cmd = f'{"sudo " if sudo else ""}rm -f "{test_file}"'
        if os.system(rm_cmd) != 0:
            return False
            
        return True
    except Exception:
        return False

if __name__ == "__main__":
    # 测试目录是否可写
    test_dir = "/root"  # 替换为你要测试的目录
    if is_dir_writable(test_dir):
        print(f"{test_dir} 是可写的")
    else:
        print(f"{test_dir} 不是可写的")
    if is_dir_writable(test_dir, sudo=True):
        print(f"{test_dir} 是可写的 (使用 sudo)")
    else:
        print(f"{test_dir} 不是可写的 (使用 sudo)")