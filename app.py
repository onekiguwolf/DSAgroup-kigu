import timeit
from importlib import reload
from flask import Flask, request, jsonify, render_template
from exponential_search import exponential_search, exponential_search_wrapper
from binary_search import binary_search, binary_search_wrapper
from interpolation_search import interpolation_search, interpolation_search_wrapper
from jump_search import jump_search, jump_search_wrapper
from linear_search import linear_search, linear_search_wrapper
from ternary_search import ternary_search, ternary_search_wrapper
from postfix import infix_to_postfix
from Queue_Dequeue import Queue, Deque
import hash_table
import graph

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/templates/ListPage.html')
def ListPage():
    return render_template('ListPage.html')

@app.route('/templates/Memberpage.html')
def Memberpage():
    return render_template('Memberpage.html')

@app.route('/templates/ResultsPage.html')
def ResultsPage():
    return render_template('ResultsPage.html')

queue = []
@app.route('/templates/Queue-Dequeue.html', methods=["GET", "POST"])
def queue_operations():
    Enqueue = None
    Dequeue = None
    if request.method == 'POST':
        if request.form.get('enqueue', ''):
            data = str(request.form.get('inputString', ''))
            queue.append(data)

        elif request.form.get('dequeue', ''):
            if queue:
                Dequeue = queue.pop(0)
        return render_template('Queue-Dequeue.html', Enqueue=queue, Dequeue=Dequeue)
    else:
        return render_template('Queue-Dequeue.html', Enqueue=queue, Dequeue=Dequeue)

@app.route('/templates/Postfix.html', methods=["GET", "POST"])
def Postfix():
    # Request Infix Expression
    if request.method == "POST":
        infix_str = request.form.get("infix")
        try:
            float(infix_str)
            return render_template("Postfix.html", error="Invalid input. Ensure the operators are only `*`, `(`, `)`, `+`, `-`, or `/`, and free from numbers or whitespaces.")
        except:
            result = infix_to_postfix(infix_str)
            return render_template("Postfix.html", result=result, infix_str=infix_str)
    else:
        return render_template('Postfix.html', result=None)

@app.route('/templates/hash-table.html', methods=['GET', 'POST'])
def enchanting_table():
    if request.method == "POST":
        cmd = request.form.get('hashmethod')
        numcommand = request.form.get('inputString')
        listall = request.form.get('cmdlist')
        new_list = listall.split('\r\n')
        my_array = []
        for item in new_list:
            my_array.append(item)
        
        try:
            # check if it is an integer
            int(numcommand)
        except(ValueError):
            error = 'input is not integer. Please use integers only.'
            return render_template('hash-table.html', cmd=None, numcommand=None, result=None, listall=None, error=error)
        
        #check if the number is greater than or equal to one.
        numtype = int(numcommand)
        if numtype >= 1:
            result = hash_table.process_commands(my_array, cmd)
            return render_template('hash-table.html', cmd=None, numcommand=None, result=result, listall=None, error=None)
        if numtype <= 0:
            error = 'input is less than 1. Please use an integer greater than or equal to 1.'
            return render_template('hash-table.html', cmd=None, numcommand=None, result=None, listall=None, error=error)
    else:
        return render_template('hash-table.html', cmd=None, numcommand=None, result=None, listall=None, error=None)


@app.route('/templates/Tree_Graph.html', methods=['GET', 'POST'])
def station_graph():
    if request.method == "POST":
        start = request.form.get('starting_station')
        end = request.form.get('end_station')
        result = graph.find_shortest_path(graph.mrt_lrt_graph, start, end)
        return render_template('Tree_Graph.html', result=result)
    else:
        return render_template('Tree_Graph.html', result=None)


@app.route("/templates/searchalgo-interface.html", methods=["GET", "POST"])
def dir():
    
    numbers = range(1, 1001)
    test_data = ", ".join(map(str, numbers))
    #print(test_data)
    if request.method == "POST":
        array_str = request.form.get("array")
        target_str = request.form.get("target")
        search_type = request.form.get("search_type")

        try:
            array = list(map(int, array_str.split(",")))
            target = int(target_str)
            low, high = 0, len(array) - 1

            result = -1  # Initialize result before the conditional statements

            if search_type == "exponential":
                execution_time = timeit.timeit("exponential_search_wrapper(exponential_search, array, target)", globals={**globals(), "array": array, "target": target}, number=1)  * 1000 
                result = exponential_search_wrapper(binary_search, array, target)
                # result = exponential_search(array, target)
            elif search_type == "binary":
                #arr = list(map(int, array_str.split(",")))
                execution_time = timeit.timeit("binary_search_wrapper(binary_search, array, target)", globals={**globals(), "array": array, "target": target}, number=1)  * 1000 
                result = binary_search_wrapper(binary_search, array, target)
            elif search_type == "interpolation":
                execution_time = timeit.timeit("interpolation_search_wrapper(interpolation_search, array, target)", globals={**globals(), "array": array, "target": target}, number=1)  * 1000 
                result = interpolation_search_wrapper(interpolation_search, array, target)                
                # result = interpolation_search(array, target)
            elif search_type == "jump":
                execution_time = timeit.timeit("jump_search_wrapper(jump_search, array, target)", globals={**globals(), "array": array, "target": target}, number=1)  * 1000 
                result = jump_search_wrapper(interpolation_search, array, target)  
                # result = jump_search(array, target)
            elif search_type == "linear":
                execution_time = timeit.timeit("linear_search_wrapper(linear_search, array, target)", globals={**globals(), "array": array, "target": target}, number=1)  * 1000 
                result = linear_search_wrapper(linear_search, array, target)  
                # result = linear_search(array, target)
            elif search_type == "ternary":
                execution_time = timeit.timeit("ternary_search_wrapper(ternary_search, array, target, low, high)", globals={**globals(), "array": array, "target": target,"low":low,"high":high}, number=1)  * 1000 
                result = ternary_search_wrapper(ternary_search, array, target, low, high)  
                # result = ternary_search(array, target, low, high)

            return render_template("searchalgo-interface.html", result=result, search_type=search_type, execution_time=execution_time,test_data=test_data)
        except ValueError:
            return render_template("searchalgo-interface.html", error="Invalid input. Ensure the array and target are integers.")
    

    return render_template("searchalgo-interface.html",test_data=test_data)

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()

    if not data or "array" not in data or "target" not in data:
        return jsonify({"error": "Invalid request data. Provide 'array' and 'target'."}), 400

    array = data["array"]
    target = data["target"]

    result_iterative = exponential_search(array, target)
    #result_recursive = exponential_search_recursive(array, target)

    return jsonify({
        "iterative_search_result": result_iterative,
       # "recursive_search_result": result_recursive
    })


if __name__ == '__main__':
    app.run(debug=True)
