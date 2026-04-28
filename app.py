from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)


def parse_input_matrix(raw_text):
    rows = [row.strip() for row in raw_text.strip().splitlines() if row.strip()]
    matrix = []
    for row in rows:
        parts = row.replace(',', ' ').split()
        matrix.append([float(value) for value in parts])

    if len(matrix) == 0:
        raise ValueError('Please enter a matrix.')

    row_length = len(matrix[0])
    if any(len(r) != row_length for r in matrix):
        raise ValueError('All rows must have the same number of values.')
    if row_length != len(matrix):
        raise ValueError('Matrix must be square (same number of rows and columns).')

    return np.array(matrix)


@app.route('/', methods=['GET', 'POST'])
def index():
    matrix_text = ''
    eigenvalues = None
    eigenvectors = None
    error = None

    if request.method == 'POST':
        matrix_text = request.form.get('matrix', '')
        try:
            matrix = parse_input_matrix(matrix_text)
            values, vectors = np.linalg.eig(matrix)
            eigenvalues = [round(v,5)for v in values]
            eigenvectors = [[round(num, 5) for num in row] for row in vectors]
        except Exception as exc:
            error = str(exc)

    return render_template('index.html', matrix_text=matrix_text, eigenvalues=eigenvalues, eigenvectors=eigenvectors, error=error)


@app.route('/SVD', methods=['POST'])
def calculate_SVD():
    pass

if __name__ == '__main__':
    app.run(debug=True)