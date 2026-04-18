import streamlit as st 
import pandas as pd 
import time 


## Text based utilities
st.title('Startup Dashboard')
st.header("I am learning Streamlit")
st.subheader('And i am loving it.')

st.write('This is a normal text')

st.markdown("""
            ### My favourite movies
            - Race 3
            - Humshakals
            - Housefull
            """)

st.code("""
        def add(a, b):
            return a + b
        x = add(2, 3)
        """)

st.latex(r''' a^2 + b^2 = c^2 ''')


# Display Elements

df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie', 'David'],
    'Age': [25, 30, 35, 40],
    'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
})

st.dataframe(df)

st.metric(label="Temperature", value="25 °C", delta="1.2 °C")

st.json({
    "name": "Alice",
    "age": 25,
    "city": "New York"
})

# Display Media
st.image('https://www.python.org/static/community_logos/python-logo.png', caption='Python Logo')
st.audio('https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3')
st.video('https://www.youtube.com/watch?v=1z5-O7-5AXk&list=PLKnIA16_RmvbAlyx4_rdtR66B7EHX5k3z')


# Creating Layouts
st.sidebar.title('Sidebar ka Title')

col1, col2 = st.columns(2)

with col1:
    st.image('https://www.python.org/static/community_logos/python-logo.png', caption='Python Logo in Column 1')

with col2:
    st.image('https://www.python.org/static/community_logos/python-logo.png', caption='Python Logo in Column 2')

# Showing status
st.success("This is a success message.")
st.warning("This is a warning message.")
st.error("This is an error message.")
st.info("This is an info message.")

bar = st.progress(0)

for i in range(1, 101):
    time.sleep(0.1)
    bar.progress(i)
    break

# Taking user input 
# text input -> number input -> date input -> time input -> color input -> file uploader
name = st.text_input("Enter your name")
age = st.number_input("Enter your age", min_value=0, max_value=100)
date = st.date_input("Select a date")
time = st.time_input("Select a time")
color = st.color_picker("Pick a color")
uploaded_file = st.file_uploader("Choose a file")
if st.button("Submit"):
    st.write(f"Name: {name}, Age: {age}, Date: {date}, Time: {time}, Color: {color}")
    if uploaded_file is not None:
        st.write("File uploaded successfully!")
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.describe())

# Buttons and Interactivity
if st.button("Click me"):
    st.write("Button clicked!")
if st.checkbox("Show/Hide"):
    st.write("Checkbox is checked!")
option = st.selectbox("Select an option", ["Option 1", "Option 2", "Option 3"])
st.write(f"You selected: {option}")



