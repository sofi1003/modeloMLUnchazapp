import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


# Cargar los datos desde el archivo CSV

data = pd.read_csv(r'C:\Users\sofia\OneDrive\Documentos\ejemploML\datos.csv')


train_data, test_data = train_test_split(data, test_size=0.2, random_state=0)


tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(data['categoriasDeLosNegocios'])


cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)


def get_recommendations(idCliente, ranking_minimo=4, top_n=5):
   
    user_ratings = data[(data['idCliente'] == idCliente) & (data['rankingNegocio'] >= ranking_minimo)]
    
    
    user_categories = list(user_ratings['categoriasDeLosNegocios'])
    
    
    category_scores = {}
    for category in user_categories:
        category_mask = (data['categoriasDeLosNegocios'] == category) & (data['rankingNegocio'] >= ranking_minimo)
        category_ratings = data[category_mask]
        category_scores[category] = category_ratings['rankingNegocio'].mean()
    
    
    sorted_categories = sorted(category_scores.items(), key=lambda x: x[1], reverse=True)
    
    
    recommended_businesses = []
    for category, _ in sorted_categories:
        category_mask = (data['categoriasDeLosNegocios'] == category)
        category_businesses = data[category_mask]
        
   
        new_businesses = category_businesses[~category_businesses['idNegocio'].isin(user_ratings['idNegocio'])]
        
        recommended_businesses.extend(new_businesses['idNegocio'].tolist())
    

    unique_recommendations = list(set(recommended_businesses))
    
    return unique_recommendations[:top_n]


def actualizar_datos_csv():
    import csv
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import db

    siONo = False

    cred = credentials.Certificate(r"C:\Users\sofia\OneDrive\Documentos\ejemploML\tuto.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://unchazapp-6ecc0-default-rtdb.firebaseio.com/'
    })

    ref = db.reference('/calificaciones')

    data = []
    data.append(['idCliente', 'categoriasDeLosNegocios', 'idNegocio', 'rankingNegocio'])

    for key, value in ref.get().items():
        calificacion = value.get('calificacion', '')
        categoria = value.get('categoria', '')
        keyNegocio = value.get('keyNegocio', '')
        keyUser = value.get('keyUser', '')
        data.append([keyUser, categoria, keyNegocio, calificacion])

    try:
        with open(r'C:\Users\sofia\OneDrive\Documentos\ejemploML\datos.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
            siONo = True
        print('Los datos se han exportado correctamente a datos2.csv')
    except Exception as e:
        siONo = False
        print('Error al exportar datos a datos2.csv:', str(e))

    return siONo







