import tkinter as tk
from tkinter import ttk

class AppTheme:
    def __init__(self):
        self.style = ttk.Style()
        
        # 基础颜色
        self.primary_color = "#4a6fa5"  # 主色调
        self.secondary_color = "#6c757d"  # 次要色调
        self.success_color = "#28a745"  # 成功/确认操作
        self.danger_color = "#dc3545"   # 危险/删除操作
        self.light_bg = "#f8f9fa"      # 浅色背景
        self.dark_bg = "#343a40"       # 深色背景
        self.text_color = "#212529"    # 主要文字颜色
        
        # 配置主题
        self.configure_theme()
    
    def configure_theme(self):
        """配置ttk主题样式"""
        # 设置整体主题
        self.style.theme_create("deepin_theme", parent="clam")
        self.style.theme_use("deepin_theme")
        
        # 配置Frame样式
        self.style.configure("TFrame", 
                           background=self.light_bg)
        
        # 配置LabelFrame样式
        self.style.configure("TLabelframe", 
                           background=self.light_bg,
                           bordercolor=self.secondary_color)
        self.style.configure("TLabelframe.Label", 
                           font=('Microsoft YaHei', 10, 'bold'),
                           foreground=self.primary_color)
        
        # 配置Treeview样式
        self.style.configure("Treeview",
                           background="white",
                           foreground=self.text_color,
                           fieldbackground="white",
                           rowheight=25,
                           font=('Microsoft YaHei', 9))
        self.style.configure("Treeview.Heading",
                           font=('Microsoft YaHei', 10, 'bold'),
                           background=self.primary_color,
                           foreground="white",
                           relief="flat")
        self.style.map("Treeview.Heading",
                      background=[('active', self.secondary_color)])
        
        # 配置Button样式
        self.style.element_create('RoundedButton.border', 'from', 'clam')
        self.style.layout('TButton', [
            ('Button.border', {'sticky': 'nswe', 'border': '8', 'children': [
                ('Button.focus', {'sticky': 'nswe', 'children': [
                    ('Button.padding', {'sticky': 'nswe', 'children': [
                        ('Button.label', {'sticky': 'nswe'})
                    ]})
                ]})
            ]})
        ])
        self.style.configure("TButton",
                           font=('Microsoft YaHei', 9),
                           padding=(12, 6),
                           relief="flat",
                           borderwidth=0,
                           focusthickness=0,
                           focuscolor='none',
                           background=self.secondary_color,
                           foreground='white',
                           anchor="center")
        self.style.map("TButton",
                      foreground=[('disabled', self.secondary_color),
                                 ('active', 'white'),
                                 ('pressed', 'white')],
                      background=[('disabled', self.light_bg),
                                 ('active', self.primary_color),
                                 ('pressed', self.dark_bg),
                                 ('!disabled', self.secondary_color)],
                      bordercolor=[('pressed', self.primary_color),
                                  ('active', self.primary_color)])
        
        # 特殊按钮样式
        self.style.configure("danger.TButton",
                           background=self.danger_color,
                           foreground='white')
        self.style.map("danger.TButton",
                      background=[('pressed', self.dark_bg),
                                 ('active', '#c82333')])
        
        self.style.configure("success.TButton",
                           background=self.success_color,
                           foreground='white')
        self.style.map("success.TButton",
                      background=[('pressed', self.dark_bg),
                                 ('active', '#218838')])