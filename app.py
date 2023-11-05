import streamlit as st
import pandas as pd
import pygwalker as pyg
import streamlit.components.v1 as components
import pygsheets
import os
import fitz  # PyMuPDF
from PIL import Image

from googleapiclient.discovery import build  # Import the build function
from google.oauth2 import service_account



# Adjust the width of the Streamlit page
st.set_page_config(
    page_title="Data Visualization App",
    layout="wide"
)

# Sidebar for navigation
st.sidebar.title("Leilões de Imóveis")
page = st.sidebar.radio("Go to", ["Calendário", "Tabela de Imóveis", "Lista Imóveis (db_gsheet)"])


if page == "Calendário":
    import streamlit as st

    def calendarCaixaDownload():
        st.title("Calendário de Leilões Caixa")

        pdf_url = "https://www.caixa.gov.br/Downloads/habitacao-documentos-gerais/calendario-leiloes-imoveis-caixa.pdf"

        st.markdown(
            f"""
            [https://www.caixa.gov.br/Downloads/habitacao-documentos-gerais/calendario-leiloes-imoveis-caixa.pdf]({pdf_url})
            """,
            unsafe_allow_html=True,
        )
    
    def load_pdf(file_path):
        pdf_document = fitz.open(file_path)
        return pdf_document


    def calendarCaixaPDFViwer():
       
        st.title("PDF Viewer App")
    
        pdf_path = "data/calendario-leiloes-imoveis-caixa.pdf"  # Replace 'my_file.pdf' with your PDF file name
        
        pdf_document = load_pdf(pdf_path)
        page_number = st.number_input(label="Enter page number", min_value=1, max_value=len(pdf_document), value=1) - 1
        page = pdf_document.load_page(page_number)
        pixmap = page.get_pixmap()
        img = Image.frombuffer("RGB", [pixmap.width, pixmap.height], pixmap.samples, "raw", "RGB", 0, 1)
        st.image(img, caption=f"Page {page_number + 1}/{len(pdf_document)}", use_column_width=True)

    if __name__ == "__main__":
        calendarCaixaDownload()
        calendarCaixaPDFViwer()




elif page == "Tabela de Imóveis":
    st.title("Analyze Data with PyGWalker")

    # get a list of files in the data directory
    data_files = os.listdir('data')
    # create a selectbox to choose a file
    file = st.selectbox('Select a file', data_files)
    # read the data from the xlsx file and store it in a dataframe
    df = pd.read_excel(os.path.join('data', file))
    # drop "URL" column
    df = df.drop(columns=['URL'])

    
    # Now df contains the data read from 'data/output.csv'
    st.write(df)

    # Generate the HTML using Pygwalker
    pyg_html = pyg.to_html(df)

    # Embed the HTML into the Streamlit app
    components.html(pyg_html, height=1000, scrolling=True)

elif page == "Lista Imóveis (db_gsheet)":
    
    def load_data():
        # Authorization
        gc = pygsheets.authorize(service_file='db-gsheet-streamlit-919212249958.json')

        # Open spreadsheet and then worksheet
        sh = gc.open('Planilha Automatiza de Imóveis de Leilão - NèstiQ')
        wks = sh.sheet1

        # Update value in merged cell B7:C7 to "São Paulo"
        wks.update_value('B7', 'Distrito Federal')
       
        # Get the data as a DataFrame
        data = wks.get_as_df()

        # Drop first 3 columns
        data = data.iloc[:, 3:]

        # Drop lines with empty "Número do Imóvel"
        data = data[data['Número do Imóvel'].notnull()]

        # Drop lines with empty "Número do Imóvel"
        data = data[data['Número do Imóvel'] != '']

        return data

    def main():
        st.title("Google Sheet Data")

        st.write("Loading data from Google Sheet...")
        data = load_data()

        # refresh button to reload data
        if st.button("Refresh Data"):
            data = load_data()

        st.write("Displaying the DataFrame:")
        st.write(data)

    if __name__ == "__main__":
        main()




