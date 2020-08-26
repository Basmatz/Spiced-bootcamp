from GerVADER.vaderSentimentGER import SentimentIntensityAnalyzer


analyser = SentimentIntensityAnalyzer()

analyser.polarity_scores('alles ist großartig!')

analyser.polarity_scores('alles ist grossartig!')

analyser.polarity_scores('alles ist kacke!')

analyser.polarity_scores('wow du intelligenzbestie')

analyser.polarity_scores('wow du intelligenz bestie')
