from flask import Flask, request, jsonify
from prueba3 import actualizar_datos_csv, get_recommendations

app = Flask(__name__)


@app.route('/recomendar', methods=['GET', 'POST'])
def recomendar():
    if request.method == 'POST':
        try:
            input_data = request.get_json()  # Se Obtienen los datos enviados desde Android Studio
            print(input_data)
            if 'cliente_id' in input_data:
                cliente_id = input_data['cliente_id']
                recomendaciones = get_recommendations(cliente_id)  # Llama a la función de recomendación

                
                print(f"ID del cliente: {cliente_id}, Recomendaciones: {recomendaciones}")

                return jsonify({'recomendaciones': recomendaciones})
            else:
                return jsonify({'error': 'Datos de entrada incorrectos'})
        except Exception as e:
            return jsonify({'error': str(e)})
    elif request.method == 'GET':
        return "Esta es una respuesta para solicitudes GET. Puedes enviar datos JSON en una solicitud POST."

if __name__ == '__main__':
    if actualizar_datos_csv():
        app.run(host='0.0.0.0', port=5000)


    
    
