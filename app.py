from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
products = pickle.load(open('products.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))

app = Flask(__name__)



@app.route('/recommend_products',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = products[products['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('prod-name')['prod-name'].values))
        item.extend(list(temp_df.drop_duplicates('prod-name')['product-type'].values))
        item.extend(list(temp_df.drop_duplicates('prod-name')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)
