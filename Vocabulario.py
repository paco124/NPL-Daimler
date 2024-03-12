
import os
import string
import re
from nltk.corpus import stopwords
from collections import Counter
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from spellchecker import SpellChecker

#Definimos ruta del archivo
ruta_relativa = "Vocabulario_Daimler/Vocabulario_Sin_Procesar.txt"
ruta_completa = os.path.join(os.path.dirname(__file__), ruta_relativa)

# Funion para leer archivos
def open_file(ruta_completa):
    with open(ruta_completa, "r", encoding='iso-8859-1') as archivo:
        contenido = archivo.read()
        return contenido
    
#Funcion guardar palabras en archivo
def save_list(lines, filename):
	data = '\n'.join(lines)
	file = open(filename, 'w')
	file.write(data)
	file.close()

#Se lee el archivo
contenido = open_file(ruta_completa)

#separamos las palabras y las ponemos en minusculas
tokens = contenido.lower().split()

#se eliminan signos de puntuacion
re_punc = re.compile('[%s]'% re.escape(string.punctuation))
tokens = [re_punc.sub('', w) for w in tokens if w.isalpha()]

#se quita palabras que no aportan ningun significado
stop_words = set(stopwords.words('english'))
tokens = [w for w in tokens if w not in stop_words and len(w) > 1]

vocab = Counter()
vocab.update(tokens)


print(len(vocab))
# print(vocab.most_common(200))
save_list(vocab,'Vocabulario_Procesado.txt')


#Definimos ruta del archivo
ruta_relativa = "Vocabulario_Procesado.txt"
ruta_completa = os.path.join(os.path.dirname(__file__), ruta_relativa)
contenido2 = open_file(ruta_completa)

# Inicializar lematizador y corrector ortográfico
lemmatizer = WordNetLemmatizer()
spell = SpellChecker()

words = contenido2.split()
print(len(words))

lemmatized_corrected_words = []
i = 0
for word in words:
    lemmatized_word = lemmatizer.lemmatize(word)
    corrected_word = spell.correction(lemmatized_word)
    if corrected_word is None:  # Comprobar si la corrección devuelve None
        print(f"Word '{lemmatized_word}, {i}' could not be corrected, using lemmatized version.")
        corrected_word = lemmatized_word  # Usar la palabra lematizada si no hay corrección
    i += 1
    lemmatized_corrected_words.append(corrected_word)

final_vocab = list(set(lemmatized_corrected_words))

# Guardar el vocabulario final
save_list(final_vocab, 'Vocabulario_Final.txt')

print(f"Total palabras finales: {len(final_vocab)}")
