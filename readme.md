# proyecto_twitter_tech_sentiment_analysis
Análisis de sentimiento sobre dispositivos tecnológicos usando la twitter API

Introducción

Este es un proyecto de redes neuronales para analisis de lenguaje antural NLP y analisis de sentimiento de texto publicado en twitter al respecto de opiniones sobre dispositivos electronicos. El proyecto se encuentra programado en python 3.8 y hace uso de la API de Twitter para extraer los datos de Twitter y de tensor flow para llevar a cabo el modelo de NLP.

Dataset: Opiniones de twitter sobre dispositivos electronicos
Autor: Luis Alberto Flores Rodríguez
Dirección: Ciudad de México

### Data set overview  
La información contiene tweets en español sobre opiniones de usuarios respecto a dispositivos electronicos comerciales
La información fue capturada desde 6 de Junio del 2022 hasta el 14 de junio del 2022 y fueron ingestados haciendo peticiones a la API de Twitter [https://developer.twitter.com/en/docs/twitter-api](https://developer.twitter.com/en/docs/twitter-api) 

### INSTRUMENT DESCRIPTION:
Brief text (i.e. 1-2 paragraphs) describing the instrument with references
Figures (or links), if applicable
Table of specifications (i.e. accuracy, precision, frequency, resolution, etc.)

### DATA COLLECTION AND PROCESSING:
Los datos fueron recolectados utilizando la API de twitter por medio del paquete tweepy de python [https://www.tweepy.org/](https://www.tweepy.org/) y colocados en un arreglo csv. Se
aplicó un filtro para obtener tweets en español y filtros para obtener tweets que inclueran nombres de marcas comunes de tecnologia, con el fin de obtener tweets con tematica de dispositivos electronicos comerciales.

De igual forma, se aplican otros filtros a los twweets ya ingestados; Filtro descartan los re tweets y filtros para eliminar del texto del pipes "|", el punto y coma ";", los tabs "\t", saltos de linea "\n" con el fin de limpiar la información

Description of data collection
Description of derived parameters and processing techniques used
Description of quality control procedures
Data intercomparisons, if applicable

### DATA FORMAT
El archivo se encuentra en formato .csv separado por pipes '|' y esta codificado en latin-1
los nombres de las columnas son timestamp|twitter_id|usuario|tweet|num_comentarios|sentimiento|funcionamiento|atencion_cliente

```
timestamp:int:ej
twitter_id:int
usuario:string
tweet:string
num_comentarios:int
sentimiento:int
funcionamiento:int
atencion_cliente:int
```

| id_str  |  created_at | screen_name  | text  | followers_count  | sentiment | funcionality | client_attention |
|---|---|---|---|---|---|---|---|
1536525314502528001|Tue Jun 14 01:45:56 +0000 2022|ilovminne_|me cambie y ahora no se cómo entrar a mis cuentas de fanplus te odio X me arruinaste la vida|51|0|1|0|

Data file structure and file naming conventions (e.g. column delimited ASCII, NetCDF, GIF, JPEG, etc.)
Data format and layout (i.e. description of header/data records, sample records)
List of parameters with units, sampling intervals, frequency, range
Data version number and date
Description of flags, codes used in the data, and definitions (i.e. good, questionable, missing, estimated, etc.)

### DATA PREPROCESSING FOR THE MODEL
Una vez filtrados e ingestados los tweets, se procede a ser una limpieza del texto con el fin de ser insumo para el modelo de procesamiento de lenguaje natural. Para esto se procede a aplicar las siguientes transformaciones al texto:

* Cambiar palabras de mayúsculas a minúsculas
* Se han eliminado las '@' de @USUARIO con el fin de facilitar el etiquetado morfológico
* Quitar los links 
* Quitar los emojis
* Se han reemplazado quitado los números
* Quitar los signos de puntuación y quitar espacios (tabuladores, etc)

### DATA REMARKS:
PI's assessment of the data (i.e. disclaimers, instrument problems, quality issues, etc.)
Missing data periods
Software compatibility (i.e. list of existing software to view/manipulate the data)

### REFERENCES:
List of documents cited in this data set description
