import streamlit as st;
import pandas as pd;
import os
from io import BytesIO 


st.set_page_config(page_title="Mindset" ,layout='wide')
st.title("Mindset Growing")
st.write("Open a terminal or command prompt, navigate to the directory where your app.py is located, and run:")

uploaded_files = st.file_uploader("Upload Your File:", type=["csv","xlsx"], accept_multiple_files=True)





if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read file based on extension
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type {file_ext}")
            continue  # Skip unsupported files

        # Display file info (only reaches here for CSV/XLSX files)
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024:.2f} KB")
        st.write("**Data Preview:**")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")  # Fixed typo: st.write()



            with col2:
                if st.button(f"fill Missing values for {file.name}") :
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been filled!.")

        st.subheader("Select Columns to Convert")      
        column = st.multiselect(f"Choose Columns for {file.name}", df.columns, default= df.columns)
        df = df[column]


        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization For {file.name}") :
            st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])


        # st.subheader("Conversion Options")
        # convertion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        # if st.button(f"Convert {file.name}"):
        #     buffer = BytesIO()
        #     if convertion_type == "CSV":
        #         df.to_csv(buffer,index=False)
        #         file_name = file.name.replace(file_ext, ".csv")
        #         mime_type="text/csv"

        # elif convertion_type == "Excel":
        #  df.to_excel(buffer, index=False)
        #  file_name = file.name.replace(file_ext,".xlsx")
        #  mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        #   buffer.seek(0)

        # #  Download Button
        # st.download_button(
        #      label=f"Download {file.name} as {convertion_type}",
        #      data=buffer,
        #      file_name = file_name,
        #      mime = mime_type 

        #  )


        # st.success("All files processed")
    
        st.subheader("Conversion Options")
    convertion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

    if st.button(f"Convert {file.name}"):
        buffer = BytesIO()
        
        if convertion_type == "CSV":
            df.to_csv(buffer, index=False)
            file_name = file.name.replace(file_ext, ".csv")
            mime_type = "text/csv"
        elif convertion_type == "Excel":
            df.to_excel(buffer, index=False)
            file_name = file.name.replace(file_ext, ".xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        
        buffer.seek(0)
        
        st.download_button(
            label=f"Download {file.name} as {convertion_type}",
            data=buffer,
            file_name=file_name,
            mime=mime_type
        )
        
        st.success("File converted successfully!")