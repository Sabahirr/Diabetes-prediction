import streamlit as st
import pandas as pd
import pickle

st.markdown("<h6><b>Zehmet olmazsa, dil seçin. Please, select a language. Пожалуйста, выберите язык. Bitte, wählen Sie eine Sprache.</b></h6>", unsafe_allow_html=True)
language = st.selectbox(" ", ('Azərbaycan dili', 'English', 'Русский', 'Deutsch'))
st.image('diabetes.jpg', use_container_width=True)


if language == 'Azərbaycan dili':
    # Başlıq
    st.title('Şəkərli Diabet Xəstəlik Riskini Proqnozlaşdırma')

    # Parametrlərin daxil edilməsi üçün interfeys
    st.header('Parametrləri daxil edin')

    # Sütunlar
    col1, col2, col3 = st.columns(3)

    with col1:
        CholCheck = st.radio("Xolesterol testi olunubmu?", options=["Bəli", "Xeyr"], index=1)  # Default to "Xeyr"
        HighChol = st.radio("Yüksək xolesterol?", options=["Var", "Yox"])
        Stroke = st.radio('İnsult?', options=['Bəli', 'Xeyr'])
        HeartDiseaseorAttack = st.radio('Hər hansı ürək xəstəliyi və ya İnfarkt?', options=['Bəli', 'Xeyr'])
        HvyAlcoholConsump = st.radio("Spirtli içkilərdən çox istifadə edilirmi?", options=["Bəli", "Xeyr"], index=1)  # Default to "Xeyr"
        
        
    with col2:
        Fruits = st.radio('Davamlı olaraq meyvə yeyilirmi?', options=['Bəli', 'Xeyr'])
        Veggies = st.radio('Davamlı olaraq tərəvəz yeyilirmi?', options=['Bəli', 'Xeyr'])
        PhysActivity = st.radio('Fiziki aktivsinizmi?', options=['Bəli', 'Xeyr'])
        DiffWalk = st.radio('Çətinlikləmi gəzirsiniz?', options=['Bəli', 'Xeyr'])
        Sex = st.radio('Cinsiyyət', options=['Qadın', 'Kişi'])
        

    with col3:
        
        HighBP = st.radio('Yüksək qan təzyiqi?', options=['Var', 'Yox'])
        AnyHealthcare = st.radio('Hər hansı bir xəstəlik?', options=['Var', 'Yox'])
        Smoker = st.radio('Siqaret çəkirsinizmi?', options=['Bəli', 'Xeyr'])
        BMI = st.number_input('Çəki indeksi (BMI)', min_value=10, max_value=100, value=28)
        Age = st.number_input('Yaşınızı daxil edin!', min_value=0, max_value=120, value=40)


    Education = st.selectbox('Təhsil səviyyəniz', options=['Təhsilsiz', 'Natamam orta təhsil', 'Orta', 'Bakalavr', 'Magistr', 'Doktorantura'], index=2)
    Income = st.slider('Gəlir səviyyəsi', value=350, min_value=0,  max_value=10000, step=50) 
    # Başlıq hissəsini bold və böyük şriftlə göstərmək
    st.markdown("<h4><b>Fiziki sağlamlıq</b></h4>", unsafe_allow_html=True)
    st.markdown("<small>30 ballıq sistem üzrə fiziki sağlamlığınızı dəyərləndirin</small>", unsafe_allow_html=True)
    PhysHlth = st.slider('', value=20, min_value=0, max_value=30, step=1)

    st.markdown("<h4><b>Mental sağlamlıq</b></h4>", unsafe_allow_html=True)
    st.markdown("<small>30 ballıq sistem üzrə mental sağlamlığınızı dəyərləndirin</small>", unsafe_allow_html=True)
    MentHlth = st.slider('', value=21, min_value=0, max_value=30, step=1)

    st.markdown("<h4><b>Ümumi sağlamlıq vəziyyəti</b></h4>", unsafe_allow_html=True)
    st.markdown("<small>5 ballıq sistem üzrə Ümumi sağlamlığınızı dəyərləndirin</small>", unsafe_allow_html=True)
    GenHlth = st.radio("", options=[1, 2, 3, 4, 5], index=2)  # Default to 3

    NoDocbcCost = st.radio('Həkimə görünmüsünüzmü?', options=["Bəli", "Xeyr"])


    # İstifadəçidən inputlar qəbul edilir və bir DataFrame şəklində göstərilir
    input_data = {
        'HighBP': HighBP,
        'HighChol': HighChol,
        'CholCheck': CholCheck,
        'BMI': BMI,
        'Smoker': Smoker,
        'Stroke': Stroke,
        'HeartDiseaseorAttack': HeartDiseaseorAttack,
        'PhysActivity': PhysActivity,
        'Fruits': Fruits,
        'Veggies': Veggies,
        'HvyAlcoholConsump': HvyAlcoholConsump,
        'AnyHealthcare': AnyHealthcare,
        'NoDocbcCost': NoDocbcCost,
        'GenHlth': GenHlth,
        'MentHlth': MentHlth,
        'PhysHlth': PhysHlth,
        'DiffWalk': DiffWalk,
        'Sex': Sex,
        'Age': Age,
        'Education': Education,
        'Income': Income,
    }

    input_df = pd.DataFrame([input_data])

    # DataFrame-i göstər
    st.subheader('Daxil edilən məlumatlar:')
    st.write(input_df)


    binary_cols = ['Sex','HighBP','HeartDiseaseorAttack','Stroke', 'AnyHealthcare',
                    'Smoker','HvyAlcoholConsump', 'Fruits', 'Veggies','CholCheck',
                    'HighChol','PhysActivity', 'DiffWalk',  'NoDocbcCost']

    # "Bəli"ni 1, "Xeyr"i 0 ilə əvəz edir
    for col in binary_cols:
        input_df[col] = input_df[col].map({'Bəli': 1, 'Xeyr': 0, 'Var': 1, 'Yox': 0, 'Kişi':1, 'Qadın':0})


    # Age sütununu aralıqlara görə 1, 2 və 3 ilə kodlamaq
    age_bins = [0, 15, 21, 27, 33, 39, 45, 51, 57, 63, 69, 74, 80, 200]  # Aralıqlar
    age_labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]      # Hər bir aralıq üçün dəyər
    input_df['Age'] = pd.cut(input_df['Age'], bins=age_bins, labels=age_labels, include_lowest=True)

    income_bins = [0, 100, 250, 400, 550, 700, 870, 1000, 20000]  # Aralıqlar
    income_labels = [1, 2, 3, 4, 5, 6, 7, 8]      # Hər bir aralıq üçün dəyər
    input_df['Income'] = pd.cut(input_df['Income'], bins=income_bins, labels=income_labels, include_lowest=True)


    # Education sütunundakı dəyərləri dəyişmək üçün uyğun map
    education_map = {'Təhsilsiz':1, 'Natamam orta təhsil':2, 'Orta': 3,'Bakalavr': 4,'Magistr': 5,'Doktorantura': 6}
    input_df['Education'] = input_df['Education'].map(education_map)



    # Model və scaler fayllarını yükləyirik
    with open('best_model_xg.pkl', 'rb') as model_file:
        model = pickle.load(model_file)

    with open('scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)


    # 7. Make a prediction
    if st.button('Proqnoz'):
        input_scaled = scaler.transform(input_df)
        prediction = model.predict_proba(input_scaled)        # for Log model
        predict_percent = prediction[0, 1] * 100
       
        
        # Şərti nəticə təqdimatı
        if predict_percent > 75:
            card_html = f"""
            <div style="border: 2px solid #FF0000; border-radius: 10px; padding: 20px; text-align: center;">
                <h2 style="color: #FF0000;">Risk Yüksəkdir</h2>
                <p style="font-size: 24px; color: #FF6347;">⚠️ Şəkərli diabet riski yüksəkdir, mütləq həkimlə məsləhətləşin:</p>
                <h1 style="color: #FF4500;">{predict_percent:.1f}%</h1>
            </div>
            """
        elif 50 <= predict_percent <= 75:
            card_html = f"""
            <div style="border: 2px solid #FFA500; border-radius: 10px; padding: 20px; text-align: center;">
                <h2 style="color: #FFA500;">Orta Risk</h2>
                <p style="font-size: 24px; color: #FFD700;">⚠️ Şəkərli diabet riski orta səviyyədədir, ehtiyatlı olun:</p>
                <h1 style="color: #FFA500;">{predict_percent:.1f}%</h1>
            </div>
            """
        elif 25 <= predict_percent < 50:
            card_html = f"""
            <div style="border: 2px solid #4CAF50; border-radius: 10px; padding: 20px; text-align: center;">
                <h2 style="color: #4CAF50;">Aşağı Risk</h2>
                <p style="font-size: 24px; color: #66BB6A;">😊 Şəkərli diabet riski aşağıdır, sağlamlığınıza diqqət edin:</p>
                <h1 style="color: #66BB6A;">{predict_percent:.1f}%</h1>
            </div>
            """
        else:
            card_html = f"""
            <div style="border: 2px solid #008000; border-radius: 10px; padding: 20px; text-align: center;">
                <h2 style="color: #008000;">Çox Aşağı Risk</h2>
                <p style="font-size: 24px; color: #32CD32;">🎉 Şəkərli diabet riski çox aşağıdır, hər şey qaydasındadır:</p>
                <h1 style="color: #32CD32;">{predict_percent:.1f}%</h1>
            </div>
            """
        
        # Render the HTML card
        st.markdown(card_html, unsafe_allow_html=True)

elif language == 'English':
    # Title
    st.title('Diabetes Risk Prediction')

    # Interface for entering parameters
    st.header('Enter Parameters')

    # Columns
    col1, col2, col3 = st.columns(3)

    with col1:
        CholCheck = st.radio("Have you had a cholesterol test?", options=["Yes", "No"], index=1)  # Default to "No"
        HighChol = st.radio("High cholesterol?", options=["Yes", "No"])
        Stroke = st.radio('Stroke?', options=['Yes', 'No'])
        HeartDiseaseorAttack = st.radio('Any heart disease or attack?', options=['Yes', 'No'])
        HvyAlcoholConsump = st.radio("Do you consume alcohol heavily?", options=["Yes", "No"], index=1)  # Default to "No"
        
        
    with col2:
        Fruits = st.radio('Do you regularly eat fruits?', options=['Yes', 'No'])
        Veggies = st.radio('Do you regularly eat vegetables?', options=['Yes', 'No'])
        PhysActivity = st.radio('Are you physically active?', options=['Yes', 'No'])
        DiffWalk = st.radio('Do you have difficulty walking?', options=['Yes', 'No'])
        Sex = st.radio('Gender', options=['Female', 'Male'])
        

    with col3:
        HighBP = st.radio('High blood pressure?', options=['Yes', 'No'])
        AnyHealthcare = st.radio('Any health issues?', options=['Yes', 'No'])
        Smoker = st.radio('Do you smoke?', options=['Yes', 'No'])
        BMI = st.number_input('Body Mass Index (BMI)', min_value=10, max_value=100, value=28)
        Age = st.number_input('Enter your age!', min_value=0, max_value=120, value=40)


    Education = st.selectbox('Education level', options=['No education', 'Incomplete high school', 'High school', 'Bachelor', 'Master', 'Doctorate'], index=2)
    Income = st.slider('Income level', value=350, min_value=0,  max_value=10000, step=50) 
    # Display heading with bold and larger font
    st.markdown("<h4><b>Physical Health</b></h4>", unsafe_allow_html=True)
    st.markdown("<small>Rate your physical health on a scale of 30</small>", unsafe_allow_html=True)
    PhysHlth = st.slider('', value=20, min_value=0, max_value=30, step=1)

    st.markdown("<h4><b>Mental Health</b></h4>", unsafe_allow_html=True)
    st.markdown("<small>Rate your mental health on a scale of 30</small>", unsafe_allow_html=True)
    MentHlth = st.slider('', value=21, min_value=0, max_value=30, step=1)

    st.markdown("<h4><b>Overall Health Status</b></h4>", unsafe_allow_html=True)
    st.markdown("<small>Rate your overall health on a scale of 5</small>", unsafe_allow_html=True)
    GenHlth = st.radio("", options=[1, 2, 3, 4, 5], index=2)  # Default to 3

    NoDocbcCost = st.radio('Have you visited a doctor?', options=["Yes", "No"])


    # Accept input from the user and display as a DataFrame
    input_data = {
        'HighBP': HighBP,
        'HighChol': HighChol,
        'CholCheck': CholCheck,
        'BMI': BMI,
        'Smoker': Smoker,
        'Stroke': Stroke,
        'HeartDiseaseorAttack': HeartDiseaseorAttack,
        'PhysActivity': PhysActivity,
        'Fruits': Fruits,
        'Veggies': Veggies,
        'HvyAlcoholConsump': HvyAlcoholConsump,
        'AnyHealthcare': AnyHealthcare,
        'NoDocbcCost': NoDocbcCost,
        'GenHlth': GenHlth,
        'MentHlth': MentHlth,
        'PhysHlth': PhysHlth,
        'DiffWalk': DiffWalk,
        'Sex': Sex,
        'Age': Age,
        'Education': Education,
        'Income': Income,
    }

    input_df = pd.DataFrame([input_data])

    # Display the DataFrame
    st.subheader('Entered data:')
    st.write(input_df)


    binary_cols = ['Sex','HighBP','HeartDiseaseorAttack','Stroke', 'AnyHealthcare',
                    'Smoker','HvyAlcoholConsump', 'Fruits', 'Veggies','CholCheck',
                    'HighChol','PhysActivity', 'DiffWalk',  'NoDocbcCost']

    # Replace "Yes" with 1, "No" with 0
    for col in binary_cols:
        input_df[col] = input_df[col].map({'Yes': 1, 'No': 0, 'Var': 1, 'Yox': 0, 'Male':1, 'Female':0})


    # Encode the Age column into intervals of 1, 2, and 3
    age_bins = [0, 15, 21, 27, 33, 39, 45, 51, 57, 63, 69, 74, 80, 200]  # Age intervals
    age_labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]  # Values for each interval
    input_df['Age'] = pd.cut(input_df['Age'], bins=age_bins, labels=age_labels, include_lowest=True)

    income_bins = [0, 100, 250, 400, 550, 700, 870, 1000, 20000]  # Income intervals
    income_labels = [1, 2, 3, 4, 5, 6, 7, 8]  # Values for each interval
    input_df['Income'] = pd.cut(input_df['Income'], bins=income_bins, labels=income_labels, include_lowest=True)


    # Map to transform values in the Education column
    education_map = {'No education':1, 'Incomplete high school':2, 'High school': 3,'Bachelor': 4,'Master': 5,'Doctorate': 6}
    input_df['Education'] = input_df['Education'].map(education_map)



    # Load model and scaler files
    with open('best_model_xg.pkl', 'rb') as model_file:
        model = pickle.load(model_file)

    with open('scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)


    # 7. Make a prediction
    if st.button('Predict'):
        input_scaled = scaler.transform(input_df)
        prediction = model.predict_proba(input_scaled)  # for Log model
        predict_percent = prediction[0, 1] * 100
        
        # Conditional result display
        if predict_percent > 75:
            card_html = f"""
            <div style="border: 2px solid #FF0000; border-radius: 10px; padding: 20px; text-align: center;">
                <h2 style="color: #FF0000;">High Risk</h2>
                <p style="font-size: 24px; color: #FF6347;">⚠️ The risk of diabetes is high, consult a doctor immediately:</p>
                <h1 style="color: #FF4500;">{predict_percent:.1f}%</h1>
            </div>
            """
        elif 50 <= predict_percent <= 75:
            card_html = f"""
            <div style="border: 2px solid #FFA500; border-radius: 10px; padding: 20px; text-align: center;">
                <h2 style="color: #FFA500;">Moderate Risk</h2>
                <p style="font-size: 24px; color: #FFD700;">⚠️ The risk of diabetes is moderate, be cautious:</p>
                <h1 style="color: #FFA500;">{predict_percent:.1f}%</h1>
            </div>
            """
        elif 25 <= predict_percent < 50:
            card_html = f"""
            <div style="border: 2px solid #4CAF50; border-radius: 10px; padding: 20px; text-align: center;">
                <h2 style="color: #4CAF50;">Low Risk</h2>
                <p style="font-size: 24px; color: #66BB6A;">😊 The risk of diabetes is low, stay healthy:</p>
                <h1 style="color: #66BB6A;">{predict_percent:.1f}%</h1>
            </div>
            """
        else:
            card_html = f"""
            <div style="border: 2px solid #008000; border-radius: 10px; padding: 20px; text-align: center;">
                <h2 style="color: #008000;">Very Low Risk</h2>
                <p style="font-size: 24px; color: #32CD32;">🎉 The risk of diabetes is very low, everything is fine:</p>
                <h1 style="color: #32CD32;">{predict_percent:.1f}%</h1>
            </div>
            """
        

        # Render the card in Streamlit
        st.markdown(card_html, unsafe_allow_html=True)

elif language == 'Deutsch':
    # Titel
    st.title('Diabetes Risiko Vorhersage')

    # Schnittstelle zur Eingabe von Parametern
    st.header('Geben Sie Parameter ein')

    # Spalten
    col1, col2, col3 = st.columns(3)

    with col1:
        CholCheck = st.radio("Haben Sie einen Cholesterintest gemacht?", options=["Ja", "Nein"], index=1)  # Standardmäßig auf "Nein"
        HighChol = st.radio("Hoher Cholesterinspiegel?", options=["Ja", "Nein"])
        Stroke = st.radio('Schlaganfall?', options=['Ja', 'Nein'])
        HeartDiseaseorAttack = st.radio('Irgendeine Herzkrankheit oder -anfälle?', options=['Ja', 'Nein'])
        HvyAlcoholConsump = st.radio("Konsumieren Sie stark Alkohol?", options=["Ja", "Nein"], index=1)  # Standardmäßig auf "Nein"
            
    with col2:
        Fruits = st.radio('Essen Sie regelmäßig Obst?', options=['Ja', 'Nein'])
        Veggies = st.radio('Essen Sie regelmäßig Gemüse?', options=['Ja', 'Nein'])
        PhysActivity = st.radio('Sind Sie körperlich aktiv?', options=['Ja', 'Nein'])
        DiffWalk = st.radio('Haben Sie Schwierigkeiten beim Gehen?', options=['Ja', 'Nein'])
        Sex = st.radio('Geschlecht', options=['Weiblich', 'Männlich'])
            
    with col3:
        HighBP = st.radio('Hoher Blutdruck?', options=['Ja', 'Nein'])
        AnyHealthcare = st.radio('Irgendeine Gesundheitsprobleme?', options=['Ja', 'Nein'])
        Smoker = st.radio('Rauchen Sie?', options=['Ja', 'Nein'])
        BMI = st.number_input('Body-Mass-Index (BMI)', min_value=10, max_value=100, value=28)
        Age = st.number_input('Geben Sie Ihr Alter ein!', min_value=0, max_value=120, value=40)

    Education = st.selectbox('Bildungsniveau', options=['Keine Ausbildung', 'Unvollständige Sekundarschule', 'Sekundarschule', 'Bachelor', 'Master', 'Doktor'], index=2)
    Income = st.slider('Einkommensniveau', value=350, min_value=0, max_value=10000, step=50) 
    # Überschrift mit fett und größerer Schrift anzeigen
    st.markdown("<h4><b>Körperliche Gesundheit</b></h4>", unsafe_allow_html=True)
    st.markdown("<small>Bewerten Sie Ihre körperliche Gesundheit auf einer Skala von 30</small>", unsafe_allow_html=True)
    PhysHlth = st.slider('', value=20, min_value=0, max_value=30, step=1)

    st.markdown("<h4><b>Mentale Gesundheit</b></h4>", unsafe_allow_html=True)
    st.markdown("<small>Bewerten Sie Ihre mentale Gesundheit auf einer Skala von 30</small>", unsafe_allow_html=True)
    MentHlth = st.slider('', value=21, min_value=0, max_value=30, step=1)

    st.markdown("<h4><b>Gesundheitszustand insgesamt</b></h4>", unsafe_allow_html=True)
    st.markdown("<small>Bewerten Sie Ihre allgemeine Gesundheit auf einer Skala von 5</small>", unsafe_allow_html=True)
    GenHlth = st.radio("", options=[1, 2, 3, 4, 5], index=2)  # Standardmäßig auf 3

    NoDocbcCost = st.radio('Haben Sie einen Arzt besucht?', options=["Ja", "Nein"])

    # Eingabedaten vom Benutzer akzeptieren und als DataFrame anzeigen
    input_data = {
        'HighBP': HighBP,
        'HighChol': HighChol,
        'CholCheck': CholCheck,
        'BMI': BMI,
        'Smoker': Smoker,
        'Stroke': Stroke,
        'HeartDiseaseorAttack': HeartDiseaseorAttack,
        'PhysActivity': PhysActivity,
        'Fruits': Fruits,
        'Veggies': Veggies,
        'HvyAlcoholConsump': HvyAlcoholConsump,
        'AnyHealthcare': AnyHealthcare,
        'NoDocbcCost': NoDocbcCost,
        'GenHlth': GenHlth,
        'MentHlth': MentHlth,
        'PhysHlth': PhysHlth,
        'DiffWalk': DiffWalk,
        'Sex': Sex,
        'Age': Age,
        'Education': Education,
        'Income': Income,
    }

    input_df = pd.DataFrame([input_data])

    # DataFrame anzeigen
    st.subheader('Eingegebene Daten:')
    st.write(input_df)

    binary_cols = ['Sex', 'HighBP', 'HeartDiseaseorAttack', 'Stroke', 'AnyHealthcare',
                    'Smoker', 'HvyAlcoholConsump', 'Fruits', 'Veggies', 'CholCheck',
                    'HighChol', 'PhysActivity', 'DiffWalk', 'NoDocbcCost']

    # Ersetze "Ja" durch 1, "Nein" durch 0
    for col in binary_cols:
        input_df[col] = input_df[col].map({'Ja': 1, 'Nein': 0, 'Var': 1, 'Yox': 0, 'Männlich': 1, 'Weiblich': 0})

    # Kodieren der Alterskolonne in Intervalle von 1, 2 und 3
    age_bins = [0, 15, 21, 27, 33, 39, 45, 51, 57, 63, 69, 74, 80, 200]  # Altersintervalle
    age_labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]  # Werte für jedes Intervall
    input_df['Age'] = pd.cut(input_df['Age'], bins=age_bins, labels=age_labels, include_lowest=True)

    income_bins = [0, 100, 250, 400, 550, 700, 870, 1000, 20000]  # Einkommensintervalle
    income_labels = [1, 2, 3, 4, 5, 6, 7, 8]  # Werte für jedes Intervall
    input_df['Income'] = pd.cut(input_df['Income'], bins=income_bins, labels=income_labels, include_lowest=True)

    # Werte in der Bildungsspalte transformieren
    education_map = {'Keine Ausbildung': 1, 'Unvollständige Sekundarschule': 2, 'Sekundarschule': 3, 'Bachelor': 4, 'Master': 5, 'Doktor': 6}
    input_df['Education'] = input_df['Education'].map(education_map)

    # Modell- und Skalierungsdateien laden
    with open('best_model_xg.pkl', 'rb') as model_file:
        model = pickle.load(model_file)

    with open('scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)

    # 7. Vorhersage treffen
    if st.button('Vorhersagen'):
        input_scaled = scaler.transform(input_df)
        prediction = model.predict_proba(input_scaled)  # für Log-Modell
        predict_percent = prediction[0, 1] * 100
        
        # Bedingte Ergebnisanzeige
        if predict_percent > 75:
            card_html = f"""
            <div style="border: 2px solid #FF0000; border-radius: 10px; padding: 20px; text-align: center;">
                <h2 style="color: #FF0000;">Hohes Risiko</h2>
                <p style="font-size: 24px; color: #FF6347;">⚠️ Das Risiko für Diabetes ist hoch, konsultieren Sie sofort einen Arzt:</p>
                <h1 style="color: #FF4500;">{predict_percent:.1f}%</h1>
            </div>
            """
        elif 50 <= predict_percent <= 75:
            card_html = f"""
            <div style="border: 2px solid #FFA500; border-radius: 10px; padding: 20px; text-align: center;">
                <h2 style="color: #FFA500;">Mäßiges Risiko</h2>
                <p style="font-size: 24px; color: #FFD700;">⚠️ Das Risiko für Diabetes ist mäßig, seien Sie vorsichtig:</p>
                <h1 style="color: #FFA500;">{predict_percent:.1f}%</h1>
            </div>
            """
        elif 25 <= predict_percent < 50:
            card_html = f"""
            <div style="border: 2px solid #4CAF50; border-radius: 10px; padding: 20px; text-align: center;">
                <h2 style="color: #4CAF50;">Niedriges Risiko</h2>
                <p style="font-size: 24px; color: #66BB6A;">😊 Das Risiko für Diabetes ist niedrig, bleiben Sie gesund:</p>
                <h1 style="color: #66BB6A;">{predict_percent:.1f}%</h1>
            </div>
            """
        else:
            card_html = f"""
            <div style="border: 2px solid #008000; border-radius: 10px; padding: 20px; text-align: center;">
                <h2 style="color: #008000;">Sehr niedriges Risiko</h2>
                <p style="font-size: 24px; color: #32CD32;">🎉 Das Risiko für Diabetes ist sehr niedrig, alles ist in Ordnung:</p>
                <h1 style="color: #32CD32;">{predict_percent:.1f}%</h1>
            </div>
            """
            
        # Die Karte in Streamlit rendern
        st.markdown(card_html, unsafe_allow_html=True)

else:
    st.title('Прогноз риска диабета')

    # Интерфейс для ввода параметров
    st.header('Введите параметры')

    # Столбцы
    col1, col2, col3 = st.columns(3)

    with col1:
        CholCheck = st.radio("Проходили ли вы тест на холестерин?", options=["Да", "Нет"], index=1)  # По умолчанию "Нет"
        HighChol = st.radio("Высокий холестерин?", options=["Да", "Нет"])
        Stroke = st.radio('Инсульт?', options=['Да', 'Нет'])
        HeartDiseaseorAttack = st.radio('Есть ли сердечные заболевания или инфаркт?', options=['Да', 'Нет'])
        HvyAlcoholConsump = st.radio("Потребляете ли вы алкоголь в большом количестве?", options=["Да", "Нет"], index=1)  # По умолчанию "Нет"

    with col2:
        Fruits = st.radio('Регулярно ли вы едите фрукты?', options=['Да', 'Нет'])
        Veggies = st.radio('Регулярно ли вы едите овощи?', options=['Да', 'Нет'])
        PhysActivity = st.radio('Вы физически активны?', options=['Да', 'Нет'])
        DiffWalk = st.radio('Есть ли у вас трудности с ходьбой?', options=['Да', 'Нет'])
        Sex = st.radio('Пол', options=['Женский', 'Мужской'])

    with col3:
        HighBP = st.radio('Высокое кровяное давление?', options=['Да', 'Нет'])
        AnyHealthcare = st.radio('Есть ли у вас проблемы со здоровьем?', options=['Да', 'Нет'])
        Smoker = st.radio('Вы курите?', options=['Да', 'Нет'])
        BMI = st.number_input('Индекс массы тела (BMI)', min_value=10, max_value=100, value=28)
        Age = st.number_input('Введите ваш возраст!', min_value=0, max_value=120, value=40)

    Education = st.selectbox('Уровень образования', options=['Нет образования', 'Незаконченное среднее образование', 'Среднее образование', 'Бакалавр', 'Магистр', 'Доктор'], index=2)
    Income = st.slider('Уровень дохода', value=350, min_value=0, max_value=10000, step=50) 

    # Отображение заголовка с жирным и большим шрифтом
    st.markdown("<h4><b>Физическое здоровье</b></h4>", unsafe_allow_html=True)
    st.markdown("<small>Оцените ваше физическое здоровье по шкале от 30</small>", unsafe_allow_html=True)
    PhysHlth = st.slider('', value=20, min_value=0, max_value=30, step=1)

    st.markdown("<h4><b>Психическое здоровье</b></h4>", unsafe_allow_html=True)
    st.markdown("<small>Оцените ваше психическое здоровье по шкале от 30</small>", unsafe_allow_html=True)
    MentHlth = st.slider('', value=21, min_value=0, max_value=30, step=1)

    st.markdown("<h4><b>Общее состояние здоровья</b></h4>", unsafe_allow_html=True)
    st.markdown("<small>Оцените ваше общее состояние здоровья по шкале от 5</small>", unsafe_allow_html=True)
    GenHlth = st.radio("", options=[1, 2, 3, 4, 5], index=2)  # По умолчанию 3

    NoDocbcCost = st.radio('Вы посещали врача?', options=["Да", "Нет"])

    # Принять ввод от пользователя и отобразить в виде DataFrame
    input_data = {
        'HighBP': HighBP,
        'HighChol': HighChol,
        'CholCheck': CholCheck,
        'BMI': BMI,
        'Smoker': Smoker,
        'Stroke': Stroke,
        'HeartDiseaseorAttack': HeartDiseaseorAttack,
        'PhysActivity': PhysActivity,
        'Fruits': Fruits,
        'Veggies': Veggies,
        'HvyAlcoholConsump': HvyAlcoholConsump,
        'AnyHealthcare': AnyHealthcare,
        'NoDocbcCost': NoDocbcCost,
        'GenHlth': GenHlth,
        'MentHlth': MentHlth,
        'PhysHlth': PhysHlth,
        'DiffWalk': DiffWalk,
        'Sex': Sex,
        'Age': Age,
        'Education': Education,
        'Income': Income,
    }

    input_df = pd.DataFrame([input_data])

    # Отобразить DataFrame
    st.subheader('Введенные данные:')
    st.write(input_df)

    binary_cols = ['Sex','HighBP','HeartDiseaseorAttack','Stroke', 'AnyHealthcare',
                    'Smoker','HvyAlcoholConsump', 'Fruits', 'Veggies','CholCheck',
                    'HighChol','PhysActivity', 'DiffWalk',  'NoDocbcCost']

    # Заменить "Да" на 1, "Нет" на 0
    for col in binary_cols:
        input_df[col] = input_df[col].map({'Да': 1, 'Нет': 0, 'Var': 1, 'Yox': 0, 'Мужской':1, 'Женский':0})

    # Закодировать столбец возраста в интервалы 1, 2 и 3
    age_bins = [0, 15, 21, 27, 33, 39, 45, 51, 57, 63, 69, 74, 80, 200]  # Возрастные интервалы
    age_labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]  # Значения для каждого интервала
    input_df['Age'] = pd.cut(input_df['Age'], bins=age_bins, labels=age_labels, include_lowest=True)

    income_bins = [0, 100, 250, 400, 550, 700, 870, 1000, 20000]  # Интервалы дохода
    income_labels = [1, 2, 3, 4, 5, 6, 7, 8]  # Значения для каждого интервала
    input_df['Income'] = pd.cut(input_df['Income'], bins=income_bins, labels=income_labels, include_lowest=True)

    # Отображение для преобразования значений в столбце образования
    education_map = {'Нет образования':1, 'Незаконченное среднее образование':2, 'Среднее образование': 3,'Бакалавр': 4,'Магистр': 5,'Доктор': 6}
    input_df['Education'] = input_df['Education'].map(education_map)

    # Загрузить модель и файлы масштабирования
    with open('best_model_xg.pkl', 'rb') as model_file:
        model = pickle.load(model_file)

    with open('scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)

    # 7. Сделать прогноз
    if st.button('Прогнозировать'):
        input_scaled = scaler.transform(input_df)
        prediction = model.predict_proba(input_scaled)  # для лог модели
        predict_percent = prediction[0, 1] * 100

        # Условное отображение результата
        if predict_percent > 75:
            card_html = f"""
            <div style="border: 2px solid #FF0000; border-radius: 10px; padding: 20px; text-align: center;">
                <h2 style="color: #FF0000;">Высокий риск</h2>
                <p style="font-size: 24px; color: #FF6347;">⚠️ Риск диабета высок, немедленно проконсультируйтесь с врачом:</p>
                <h1 style="color: #FF4500;">{predict_percent:.1f}%</h1>
            </div>
            """
        elif 50 <= predict_percent <= 75:
            card_html = f"""
            <div style="border: 2px solid #FFA500; border-radius: 10px; padding: 20px; text-align: center;">
                <h2 style="color: #FFA500;">Умеренный риск</h2>
                <p style="font-size: 24px; color: #FFD700;">⚠️ Риск диабета умеренный, будьте осторожны:</p>
                <h1 style="color: #FFA500;">{predict_percent:.1f}%</h1>
            </div>
            """
        elif 25 <= predict_percent < 50:
            card_html = f"""
            <div style="border: 2px solid #4CAF50; border-radius: 10px; padding: 20px; text-align: center;">
                <h2 style="color: #4CAF50;">Низкий риск</h2>
                <p style="font-size: 24px; color: #66BB6A;">😊 Риск диабета низкий, оставайтесь здоровыми:</p>
                <h1 style="color: #66BB6A;">{predict_percent:.1f}%</h1>
            </div>
            """
        else:
            card_html = f"""
            <div style="border: 2px solid #008000; border-radius: 10px; padding: 20px; text-align: center;">
                <h2 style="color: #008000;">Очень низкий риск</h2>
                <p style="font-size: 24px; color: #32CD32;">🎉 Риск диабета очень низкий, все в порядке:</p>
                <h1 style="color: #32CD32;">{predict_percent:.1f}%</h1>
            </div>
            """
        
        # Отобразить карточку в Streamlit
        st.markdown(card_html, unsafe_allow_html=True)

