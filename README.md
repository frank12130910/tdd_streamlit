# 收料通知单作数工具

## 1. 项目概述

将**来货数量**按照"客户 + SKU"维度自动分配到对应 PO 单据行的工具。

- 上传包含「来货数量」和「PO数量」两个工作表的 Excel
- 系统按客户 + SKU 匹配，将来货数量逐行分配到 PO 明细上
- 剩余未分配的数量汇总到「补PR-SKU清单」工作表
- 支持客户校验，防止录入非法客户名称

## 2. 环境要求

| 依赖 | 最低版本 |
|------|----------|
| Python | 3.10+ |
| pip | 22.0+ |

## 3. 技术栈

| 技术 | 用途 |
|------|------|
| [Streamlit](https://streamlit.io/) | Web 界面框架 |
| [Pandas](https://pandas.pydata.org/) | Excel 数据读取、匹配、计算 |
| [OpenPyXL](https://openpyxl.readthedocs.io/) | Excel 文件读写引擎 |

## 4. 目录结构

```
streamlit_excel_tool/
├── app.py                          # Streamlit 应用入口
├── processor.py                    # 核心处理逻辑（匹配分配算法）
├── requirements.txt                # Python 依赖清单
├── templates/
│   └── 收料通知单作数.xlsx          # Excel 模板文件
├── .devcontainer/
│   └── devcontainer.json           # GitHub Codespaces 开发容器配置
├── .vscode/
│   └── settings.json               # VS Code 编辑器配置
└── README.md                       # 项目说明文档
```

## 5. 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

或手动安装：

```bash
pip install streamlit pandas openpyxl
```

### 启动应用

```bash
# 方式一（推荐）
streamlit run app.py

# 方式二（当 streamlit 命令不可用时）
python -m streamlit run app.py
```

## 6. 浏览器访问

启动后浏览器打开：

```
http://localhost:8501
```

### 使用流程

1. 点击 **"📥 下载Excel模板"** 获取模板文件
2. 在「来货数量」Sheet 中填写到货明细（客户、SKU、来货数量）
3. 在「PO数量」Sheet 中填写 PO 明细（客户、SKU编码、数量、源单单号）
4. 回到页面，上传填好的 Excel 文件
5. 系统自动处理，点击 **"下载处理结果"** 获取结果文件

### 客户名称校验

来货数量中的「客户」字段仅允许以下值（校验不通过会报错）：

- `亚马逊`
- `亚马逊-加拿大`
- `独立站`
- `美仓`

## 7. 部署

### Streamlit Cloud（推荐）

1. 将代码上传到 GitHub 仓库
2. 访问 [share.streamlit.io](https://share.streamlit.io/)
3. 点击「New app」，选择仓库、分支和 `app.py` 作为主文件
4. 点击「Deploy」即可

### 服务器部署

```bash
# 1. 克隆仓库
git clone <your-repo-url>
cd streamlit_excel_tool

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动（生产模式）
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Nginx 反向代理（可选）

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}
```

将域名 A 记录指向服务器 IP，Nginx 会将请求转发到 8501 端口的 Streamlit 服务

# 提交代码
# 远程名	地址	说明
# origin	github.com/huangfeng97/tdd_streamlit.git	GitHub
# gitlab	106.52.171.38:8929/stelle/tdd_streamlit.git	GitLab

git push origin   # 推送到 GitHub
git push gitlab   # 推送到 GitLab
