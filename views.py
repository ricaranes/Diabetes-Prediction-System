
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import pickle
import numpy as np
import logging

# Configurar o logging
logging.basicConfig(level=logging.INFO)

# Substitua 'caminho/para/seu/modelo.pickle' pelo caminho real do seu arquivo pickle
MODEL_FILE_PATH = '/Users/macbook/Desktop/Diabetes Prediction/Project 2 - Diabetes Data/model_2.pkl'

# Carregar o modelo do arquivo pickle uma única vez ao iniciar a aplicação
model = None
try:
    with open(MODEL_FILE_PATH, 'rb') as model_file:
        model = pickle.load(model_file)
except Exception as e:
    # Log de erro caso o modelo não possa ser carregado
    logging.error(f"Error loading the model: {e}")

def home(request):
    # Seu código para renderizar a página inicial
    return render(request, 'diabe/home.html')

def predict(request):
    # Seu código para renderizar a página de previsão
    return render(request, 'diabe/predict.html')

def result(request):
    if request.method == 'POST':
        try:
            # Certifique-se de que o modelo foi carregado corretamente
            if model is None:
                raise ValueError("The model is not loaded.")

            # Capturar os valores enviados e converter para o tipo correto
            input_values = [
                float(request.POST.get('Pregnancies', 0)),
                float(request.POST.get('Glucose', 0)),
                float(request.POST.get('BloodPressure', 0)),
                float(request.POST.get('SkinThickness', 0)),
                float(request.POST.get('Insulin', 0)),
                float(request.POST.get('BMI', 0)),
                float(request.POST.get('DiabetesPedigreeFunction', 0)),
                float(request.POST.get('Age', 0)),
            ]

            # Log dos valores de entrada para depuração
            logging.info(f"Input values: {input_values}")

            # Converter os valores de entrada para o formato que o modelo espera (e.g., numpy array)
            input_data = np.array([input_values])

            # Fazer a previsão
            predicted_class = model.predict(input_data)[0]

            # Determinar o resultado da previsão
            result = "Positive" if predicted_class == 1 else "Negative"

            # Log do resultado da previsão
            logging.info(f"Prediction result: {result}")

            # Responder com o resultado
            return JsonResponse({'result': result})
        except Exception as e:
            # Log de erro para depuração
            logging.error(f"Error in prediction: {e}")
            # Responder com uma mensagem de erro
            return HttpResponse(f"Error: {e}", status=500)
    else:
        # Se não for um POST request, redirecionar para a página de previsão
        return HttpResponse("This endpoint only supports POST requests.", status=405)
