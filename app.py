#import the libaries
import streamlit as st
import pickle
import numpy as np
import pandas as pd

st.set_page_config(layout="wide")
st.header("Book Recomander System")
st.markdown('''
### the site using colaborative filtering suggests tooks books from our catalog.
### we recommend top 50 books for every one as well''')


# import our models
popular =pickle.load(open('popular.pkl','rb'))
books =pickle.load(open('books.pkl','rb'))
pt =pickle.load(open('pt.pkl','rb'))

similarity_scores=pickle.load(open('similarity_scores.pkl','rb'))

#top 50 books

st.sidebar.title('Top 50 Books')
if st.sidebar.button('SHOW'):
    cols_per_row=5
    num_rows=10
    for row in range(num_rows):
        cols=st.columns(cols_per_row)

        for col in range(cols_per_row):

            book_idx=row*cols_per_row+col

            if book_idx<len(popular):
                with cols[col]:
                    st.image(popular.iloc[book_idx]['Image-URL-M']) # Displays the image
                    st.text (popular.iloc[book_idx]['Book-Title']) # Displays the Book Title
                    st.text(popular.iloc[book_idx]['Book-Author']) # Display the Author name
        
# function recomend Books
def recommend(book_name):
    index=np.where(pt.index==book_name)[0][0]
    similar_items=sorted(list(enumerate(similarity_scores[index])), key= lambda x : x[1], reverse=True)[1:6]
    #lets create emepty list and in that i want at populate with book information 
    #book author book title image url
    #empty list
    data=[]
    for i in similar_items:
        item=[]
        temp_df=books[books['Book-Title']==pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    return data

#this is giving the names list of books
books_list=pt.index.values
st.sidebar.title('Similiar Book Suggestions')
#drop down to select books
selected_book=st.sidebar.selectbox("Select a book from the dropdown",books_list)

if st.sidebar.button('Recommend Me'):
    book_recommend=recommend(selected_book)
    cols=st.columns(5)
    for col_idx in range(5):
        with cols[col_idx]:
            if col_idx<len(book_recommend):
                st.image(book_recommend[col_idx][2])
                st.text(book_recommend[col_idx][0])
                st.text(book_recommend[col_idx][1])


# import data 
books=pd.read_csv('Books.csv')
users=pd.read_csv('Users.csv')
ratings=pd.read_csv('Ratings.csv')

st.sidebar.title('Data Used')

if st.sidebar.button('Show'):
    st.subheader('This is the books data we used in our model')
    st.dataframe(books)
    st.subheader('This is the User ratings data we used in our model')
    st.dataframe(books)
    st.subheader('This is the books data we used in our model')
    st.dataframe(books)
    