# app.py
from flask import Flask, request, jsonify, send_from_directory
from data.data import Data
from conco import pyconcorde
from solution import Solution

app = Flask(__name__)


@app.route('/solve', methods=['POST'])
def solve_tsp():
    """
    Solve the TSP problem using the Concorde solver and return the result as JSON.

    This endpoint expects a JSON payload containing the data for the TSP problem.
    It returns a JSON response with the solution route and total distance.
    """
    data = Data()
    data.read_json(request.json)  # 传入请求的JSON数据
    data.read_order()
    data.add_depot()
    data.calculate_distance()
    p = pyconcorde(data)
    p.solve()
    print("total_distance:", p.dis)

    # 创建任务字典
    task = {
        'route': p.route + ["end"],
        'distance': p.dis,
        'vehicle_id': data.vehicle_list[0].vehicleId
    }

    # 生成解决方案并保存到文件
    s = Solution(data, [p.route], [task])
    s.visualize()
    result = s.write_file()

    return jsonify(result)


@app.route('/images/<path:filename>')
def serve_image(filename):
    """
    Serve an image file from the output directory.

    Args:
    filename (str): The name of the image file to serve.
    """
    # 这里的路径根据实际情况调整
    return send_from_directory('../output', filename)


@app.route('/')
def index():
    """
    Serve the index HTML page.
    """
    return app.send_static_file('front_end.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

