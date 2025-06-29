#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import subprocess
import os
import sys
class DeepinImmutableManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Deepin 磐石系统管理工具")
        self.root.geometry("600x450")
        self.sudo_valid = False
        self.sudo_password = None
        
        self.create_widgets()
        self.update_status()
    
    def create_widgets(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 状态显示区域
        status_frame = ttk.LabelFrame(main_frame, text="系统磐石状态", padding="10")
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_text = tk.Text(status_frame, height=8, wrap=tk.WORD)
        self.status_text.pack(fill=tk.X)
        
        # 目录状态区域
        dir_frame = ttk.LabelFrame(main_frame, text="关键目录写入状态", padding="10")
        dir_frame.pack(fill=tk.X, pady=5)
        
        self.dir_text = tk.Text(dir_frame, height=6, wrap=tk.WORD)
        self.dir_text.pack(fill=tk.X)
        
        # 按钮区域
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="解除磐石系统", command=self.disable_protection).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(btn_frame, text="恢复磐石系统", command=self.enable_protection).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(btn_frame, text="查询状态", command=self.update_status).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        ttk.Button(btn_frame, text="重启电脑", command=self.reboot).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(btn_frame, text="退出", command=self.root.quit).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
    
    def get_sudo_password(self):
        """显示密码输入对话框"""
        password = tk.simpledialog.askstring("密码", "请输入sudo密码:",
                                            show='*', parent=self.root)
        if password:
            self.sudo_password = password + '\n'
            return True
        return False
    
    def run_command(self, *cmd, need_sudo=False):
        """执行单条或多条命令
        参数:
            cmd: 字符串(单条命令)或列表(多条命令)
            need_sudo: 是否需要sudo权限
        返回:
            最后一条命令的输出或None(出错时)
        """
        try:
            if isinstance(cmd, str):
                # 处理单条命令
                if need_sudo:
                    if not self.sudo_valid:
                        if not self.get_sudo_password():
                            return None
                        proc = subprocess.run(['sudo', '-S', '-v'],
                                            input=self.sudo_password,
                                            text=True,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
                        if proc.returncode == 0:
                            self.sudo_valid = True
                        else:
                            messagebox.showerror("错误", "密码验证失败")
                            return None
                    cmd = ['bash', '-c', f"sudo {cmd}"]
                else:
                    cmd = cmd.split()
                result = subprocess.run(cmd, check=True,
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      text=True)
                return result.stdout
            else:
                # 处理多条命令
                if need_sudo:
                    if not self.sudo_valid:
                        if not self.get_sudo_password():
                            return None
                        proc = subprocess.run(['sudo', '-S', '-v'],
                                            input=self.sudo_password,
                                            text=True,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
                        if proc.returncode == 0:
                            self.sudo_valid = True
                        else:
                            messagebox.showerror("错误", "密码验证失败")
                            return None
                    joined_cmds = " && ".join(cmd)
                    cmd = ['bash', '-c', f"sudo bash -c '{joined_cmds}'"]
                    result = subprocess.run(cmd, check=True,
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE,
                                          text=True)
                    return result.stdout
                else:
                    output = None
                    for single_cmd in cmd:
                        single_cmd = single_cmd.split()
                        result = subprocess.run(single_cmd, check=True,
                                              stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE,
                                              text=True)
                        output = result.stdout
                    return output
        except subprocess.CalledProcessError as e:
            messagebox.showerror("错误", f"命令执行失败: {e.stderr}")
            return None
    
    def check_writable(self, directory):
        """检测目录是否可写(普通权限)"""
        if os.access(directory, os.W_OK):
            return f"{directory}: 可写"
        else:
            return f"{directory}: 只读"
            
    def check_sudo_writable(self, directory):
        """检测目录是否可写(sudo权限)"""
        cmd = f"sudo test -w {directory} && echo '可写' || echo '只读'"
        result = self.run_command(cmd, need_sudo=True)
        if result:
            return f"{directory}(sudo): {result.strip()}"
        return f"{directory}(sudo): 检测失败"
    
    def update_status(self):
        # 更新系统状态
        self.status_text.config(state='normal')
        self.status_text.delete(1.0, tk.END)
        status = self.run_command("deepin-immutable-writable status")
        if status:
            status = status.replace('Enable', '是否已关闭磐石') \
                         .replace('Booted', '启动状态') \
                         .replace('Whitelist', '白名单') \
                         .replace('ClearAfterReboot', '重启后清除') \
                         .replace('CleanData', '清理数据') \
                         .replace('OverlayDirs', '挂载目录') \
                         .replace('OverlayAllDirs', '挂载所有目录') \
                         .replace('false', '否') \
                         .replace('true', '是')\
                         .replace('Status:\n', '') \
                         .replace('\n\n', '') \
                         .replace(',', '')
            self.status_text.insert(tk.END, status)
        
        # 更新目录状态
        self.dir_text.config(state='normal')
        self.dir_text.delete(1.0, tk.END)
        for directory in ['/usr', '/etc', '/opt', '/boot', '/var']:
            text = self.check_writable(directory)
            self.dir_text.insert(tk.END, text + '\n')
            text = self.check_sudo_writable(directory)
            self.dir_text.insert(tk.END, text + '\n')
        self.status_text.config(state='disabled')
        self.dir_text.config(state='disabled')
    
    def disable_protection(self):
        if messagebox.askyesno("确认", "确定要解除磐石系统吗？"):
            o = self.run_command("deepin-immutable-writable enable -a -y", "mount -o remount,rw --make-shared /usr", need_sudo=True)
            if o:
                self.update_status()
                self.reboot("操作完成，请重启系统使更改生效！")
    
    def enable_protection(self):
        if messagebox.askyesno("确认", "确定要恢复磐石系统吗？"):
            o = self.run_command("deepin-immutable-writable disable -y", need_sudo=True)
            if o:
                self.update_status()
                self.reboot("操作完成，请重启系统使更改生效！")
    
    def reboot(self,msg="确定要重启电脑吗？"):
        if messagebox.askyesno("确认", msg):
            self.run_command("reboot", need_sudo=True)


if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('clam')  # 使用现代化主题
    
    app = DeepinImmutableManager(root)
    root.mainloop()