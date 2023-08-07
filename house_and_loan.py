import streamlit as st
import pandas as pd
import pickle
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBRegressor

from PIL import Image

st.title('House Price and Loan Eligibility Predictor')

image = Image.open("pexels-carlos-machado-1013427.jpg")
image2 = Image.open("pexels-kindel-media-7579201.jpg")
st.image(image, width= 500)

# Load the house price prediction model
house_price_model = pickle.load(open("house_model.sav", 'rb'))

# Load the loan eligibility model
loan_model = pickle.load(open("loan_model.sav", 'rb'))


def main():

    # Add user input fields for house features
    st.header('House Price Prediction')
    OverallQual = st.sidebar.slider('Overall quality. Note 1 = very poor and 10 = Excellent', 1, 10, 1)
    YearBuilt = st.number_input('Input the year built e.g "2008" ',min_value=0,step=1)
    st.write('Year of Built  is ', YearBuilt)
    YearRemodAdd = st.number_input('input the Remodel date- Same as year of construction if no remodeled date e.g "2008"',min_value=0,step=1)
    st.write('Year of RemoAdd ', YearRemodAdd)
    TotalBsmtSF = st.number_input('input the Total Basement in square feet of basement area e,g 25.27')
    st.write('Total square feet of basement area', TotalBsmtSF)
    firstFlrSF = st.number_input('input the first floor in square feet e,g 25.27')
    st.write('first floor square feet is ', firstFlrSF)
    GrLivArea = st.number_input('input the Ground Living area e,g 25.27')
    st.write('Ground living area  is ', GrLivArea)
    FullBath = st.sidebar.slider('Full bathrooms above grade', 0, 3, 1)
    TotRmsAbvGrd = st.sidebar.slider('Total rooms above grade (does not include bathrooms)', 1, 30, 1)
    GarageCars = st.sidebar.slider('Garage cars-(Size of garage in car capacity)', 0, 30, 1)
    GarageArea = st.number_input('input the Size of garage in square feet e.g 40.05')
    st.write('garage area  is ', GarageArea)
    ms = st.selectbox('Identifies the general zoning classification of the sale).',['Residential Low Density', 'Residential Medium Density', 'Commercial', 'FLoating Village Residential', 'Residential Medium Density'])
    if (ms == 'FLoating Village Residential'):
        MSZoning = 1
    elif (ms == 'Residential High Density'):
        MSZoning = 2
    elif (ms == 'Residential Low Density'):
        MSZoning = 3
    elif (ms == 'Residential Medium Density'):
        MSZoning = 4
    else:
        MSZoning = 0
    st.success(f'user selected {ms}')
    uti = st.selectbox('Type of utilities available',['All public Utilities' , 'NoSewr	Electricity, Gas, and Water (Septic Tank)']) 
    if (uti == 'All public Utilities'):
        Utilities = 0
    else:
        Utilities = 1
    st.success(f'Utilities selected is {uti}')
    build = st.selectbox('Select Type of dwelling',['Single-family Detached' , 'Two-family Conversion; originally built as one-family dwelling','Duplex','Townhouse End Unit','Townhouse Inside Unit']) 
    if (build == 'Single-family Detached'):
        BldgType = 0
    elif (build == 'Duplex'):
        BldgType = 2
    elif (build == 'Townhouse End Unit'):
        BldgType = 4
    elif (build == 'Townhouse Inside Unit'):
        BldgType = 3
    else:
        BldgType = 1
    st.success(f'Type of dwelling is {build}')
    kq = st.selectbox('Kitchen Quality', ['Excellent','Good','Typical/Average','Fair', 'Poor'])
    if (kq == 'Excellent'):
       KitchenQual = 4
    elif (kq == 'Good'):
        KitchenQual = 3
    elif (kq == 'Typical/Average'):
        KitchenQual = 2
    elif (kq == 'Fair'):
        KitchenQual = 1
    else:
        KitchenQual = 0
    st.success(f'Kitchen Quality is {kq}')
    sc =  st.selectbox('Sale Condition', ['Normal', 'Abnormal', 'Partial-Home was not completed when last assessed', 'Adjoining Land Purchase', 'Allocation - two linked properties with separate deeds', 'Sale between Family'])
    if (sc == 'Sale between Family'):
       SaleCondition = 5
    elif (sc == 'Normal'):
        SaleCondition = 0
    elif (sc == 'Abnormal'):
        SaleCondition = 1
    elif (sc == 'Partial-Home was not completed when last assessed'):
       SaleCondition = 2
    elif (sc == 'Adjoining Land Purchase'):
       SaleCondition = 3
    else:
        SaleCondition = 4
    st.success(f'Sale Condition is {sc}')
    # Predict house price
    house_data = pd.DataFrame({
        'overall_quality' : [OverallQual] ,
        'year_built': [YearBuilt],
        'year_remodelled': [YearRemodAdd],
        'TotalBsmtSF': [TotalBsmtSF ],
        'firstFlrSF': [firstFlrSF],
        'GrLivArea': [GrLivArea],
        'FullBath': [FullBath],
        'TotRmsAbvGrd': [TotRmsAbvGrd],
        'GarageCars': [GarageCars],
        'GarageArea': [GarageArea],
        'MSZoning' : [MSZoning],
        'Utilities' : [Utilities],
        'BldgType' : [BldgType],
        'KitchenQual' : [KitchenQual],
        'SaleCondition': [SaleCondition]

    })
    st.text('housing data information')
    st.write(house_data)
    house_price_prediction = house_price_model.predict(house_data)[0]
    st.subheader(f'Predicted House Price: :blue[${house_price_prediction:.2f}]')

    # Add user input fields for loan eligibility
    st.header('Loan Eligibility Prediction')
    st.image(image2, width=500)
    ApplicantIncome = st.number_input('Annual Income')
    CoapplicantIncome = st.number_input('co applicant income')
    LoanAmount = st.number_input('How much loan do you want ')
    Loan_Amount_Term = st.number_input(' Enter Loan Amount Term in days e.g 360',step=1)
    status = st.radio("do you have a credit history:", ('yes', 'no'))
    if (status == 'yes'):
        Credit_History = 1
    else: Credit_History = 0
    gender = st.radio("what is your gender:", ('Male', 'Female'))
    if (gender == 'Male'):
        Gender = 1
    else: Gender = 0
    married = st.radio("Are you married:", ('yes', 'no'))
    if (married == 'yes'):
        Married = 1
    else:
        Married = 0
    Dependents = st.number_input('Dependents',step=1)
    education = st.radio("Are you a graduate?:", ('yes', 'no'))
    if (education == 'yes'):
        Education = 1
    else:
        Education = 0
    Property_Area = st.number_input('Property area')
    self = st.radio("Are you a self employed?:", ('yes', 'no'))
    if (self == 'yes'):
        Self_Employed = 1
    else:
        Self_Employed = 0


    # Predict loan eligibility
    loan_data = pd.DataFrame({
        'ApplicantIncome' : [ApplicantIncome],
        'CoapplicantIncome': [CoapplicantIncome],
        'LoanAmount': [LoanAmount],
       'Loan_Amount_Term': [Loan_Amount_Term],
        'Credit_History': [Credit_History],
        'Gender': [Gender],
        'Married': [Married],
        'Dependents': [Dependents],
       'Education': [Education],
        'Self_Employed': [Self_Employed],
        'Property_Area': [Property_Area]
    })
    st.text('loan data information')
    st.write(loan_data)

    st.success(f' Your requested loan amount is  ${LoanAmount:.2f} ')
    loan_eligibility_prediction = loan_model.predict(loan_data)[0]
    st.subheader(f'Loan Eligibility Prediction: {" ✅ Eligible" if loan_eligibility_prediction else "❌ Not Eligible"}')
if __name__ == '__main__':
    main()
