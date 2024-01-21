from wordcloud import WordCloud
import matplotlib.pyplot as plt

with open('words.csv', 'r', encoding='utf-8') as file:
    lines = file.readlines()

words = [line.split(';')[0] for line in lines[1:]]

text = ' '.join(words)

wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white',
    prefer_horizontal=0.9,
    max_words=100,
).generate(text)

plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')

plt.savefig('wordcloud.svg', format='svg', bbox_inches='tight')

plt.show()
