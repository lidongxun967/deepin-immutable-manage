#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk

class MessageBox:
    """自定义消息框，适配sv_ttk主题"""
    def __init__(self, parent=None):
        self.parent = parent
        self.result = None
        
    def _create_dialog(self, title, message, icon=None, buttons=None):
        """创建对话框基础框架"""
        dialog = tk.Toplevel(self.parent)
        dialog.title(title)
        dialog.resizable(False, False)
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # 主框架
        main_frame = ttk.Frame(dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 图标和消息
        icon_frame = ttk.Frame(main_frame)
        icon_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        if icon:
            icon_label = ttk.Label(icon_frame, image=icon)
            icon_label.pack()
        
        
        # 消息标签
        msg_label = ttk.Label(main_frame, text=message, wraplength=300)
        msg_label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # 按钮区域（新行，撑满宽度）
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        for i, (text, value) in enumerate(buttons):
            btn = ttk.Button(btn_frame, text=text,
                           command=lambda v=value: self._on_button(dialog, v))
            btn.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        dialog.wait_window(dialog)
        return self.result
    
    def _on_button(self, dialog, value):
        """按钮点击事件"""
        self.result = value
        dialog.attributes('-topmost', False)
        dialog.destroy()
        
    def _on_close(self, dialog):
        """窗口关闭事件"""
        dialog.attributes('-topmost', False)
        dialog.destroy()
        self.result = None
    
    @classmethod
    def showinfo(cls, title, message, parent=None):
        """显示信息对话框"""
        box = cls(parent)
        return box._create_dialog(title, message, buttons=[("确定", True)])
    
    @classmethod
    def showwarning(cls, title, message, parent=None):
        """显示警告对话框"""
        box = cls(parent)
        return box._create_dialog(title, message, buttons=[("确定", True)])
    
    @classmethod
    def showerror(cls, title, message, parent=None):
        """显示错误对话框"""
        box = cls(parent)
        return box._create_dialog(title, message, buttons=[("确定", True)])
    
    @classmethod
    def askyesno(cls, title, message, parent=None):
        """显示是/否对话框"""
        box = cls(parent)
        return box._create_dialog(title, message, 
                                buttons=[("是", True), ("否", False)])
    
    @classmethod
    def askokcancel(cls, title, message, parent=None):
        """显示确定/取消对话框"""
        box = cls(parent)
        return box._create_dialog(title, message, 
                                buttons=[("确定", True), ("取消", False)])

class SimpleDialog:
    """自定义简单对话框，适配sv_ttk主题"""
    def __init__(self, parent=None):
        self.parent = parent
        self.result = None
        
    def askstring(self, title, prompt, **kwargs):
        """显示字符串输入对话框"""
        dialog = tk.Toplevel(self.parent)
        dialog.title(title)
        dialog.resizable(False, False)
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # 强制窗口置顶并保持
        dialog.lift()
        
        # 计算并设置窗口居中位置
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'+{x}+{y}')
        
        dialog.focus_force()  # 强制获取焦点
        
        # 窗口关闭时恢复属性
        dialog.protocol("WM_DELETE_WINDOW", lambda: self._on_close(dialog))
        dialog.focus_force()  # 强制获取焦点
        dialog.lift()  # 再次确保置顶
        
        # 主框架
        main_frame = ttk.Frame(dialog, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 提示文本
        ttk.Label(main_frame, text=prompt).pack(anchor=tk.W)
        
        # 输入框
        entry_var = tk.StringVar()
        if 'initialvalue' in kwargs:
            entry_var.set(kwargs['initialvalue'])
            
        entry = ttk.Entry(main_frame, textvariable=entry_var, 
                         show=kwargs.get('show', None))
        entry.pack(fill=tk.X, pady=5)
        entry.focus_set()
        
        # 绑定回车键事件
        entry.bind('<Return>', lambda e: self._on_ok(dialog, entry_var))
        
        # 按钮区域
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(btn_frame, text="确定", 
                  command=lambda: self._on_ok(dialog, entry_var)).pack(
                      side=tk.LEFT, padx=5, expand=True)
        ttk.Button(btn_frame, text="取消", 
                  command=lambda: self._on_cancel(dialog)).pack(
                      side=tk.LEFT, padx=5, expand=True)
        
        dialog.wait_window(dialog)
        return self.result
    
    def _on_ok(self, dialog, entry_var):
        """确定按钮点击事件"""
        self.result = entry_var.get()
        dialog.destroy()
    
    def _on_cancel(self, dialog):
        """取消按钮点击事件"""
        self.result = None
        dialog.destroy()
        
    def _on_close(self, dialog):
        """窗口关闭事件"""
        dialog.destroy()
        self.result = None

if __name__ == '__main__':
    root = tk.Tk()
    root.title("测试")
    root.geometry("300x200")
    root.resizable(False, False)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    # 测试MessageBox
    # MessageBox.showinfo("测试", "测试信息")
    # MessageBox.showwarning("测试", "测试信息")
    # MessageBox.showerror("测试", "测试信息")
    # result = MessageBox.askyesno("测试", "测试信息")
    # result = MessageBox.askokcancel("测试", "测试信息")
    
    # 测试SimpleDialog
    dialog = SimpleDialog(root)
    result = dialog.askstring("测试", "测试信息")
    print(result)
    
    root.mainloop()