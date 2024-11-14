# Solve TSP by Concorde
### 项目简介：
&emsp;&emsp;本项目旨在解决旅行商问题（Traveling Salesman Problem, TSP），通过给定的订单、车辆和仓库信息，计算出最优的配送路线。项目使用 Python 语言开发，利用了 haversine 库来计算地理坐标之间的距离，以及 flask 框架来提供一个简单的 web 服务接口。
### 激活虚拟环境
&emsp;&emsp;`source env/bin/activate` 
### 运行flask应用
&emsp;&emsp;`python app.py`
### 通过 POST 请求 /solve 端点来解决 TSP 问题，请求体应包含 JSON 格式的输入数据
&emsp;&emsp;`curl -X POST -H "Content-Type: application/json" -d @input.json http://localhost:5000/solve`
### 文件结构
<img src="D:\sharing file\久章-TSP\structure.png"/>

### 代码说明
&emsp;&emsp;Data 类：负责读取和处理输入数据，包括订单、车辆和仓库信息。\
&emsp;&emsp;Solution 类：负责计算 TSP 问题的解决方案，并可视化结果。\
&emsp;&emsp;PyConcorde 类：封装了 Concorde TSP 求解器的接口，用于求解 TSP 问题。\
&emsp;&emsp;app.py：Flask 应用的入口点，提供了一个 web 服务接口来接收请求并返回解决方案。