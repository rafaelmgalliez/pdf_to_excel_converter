import streamlit as st
import pandas as pd
from parser import parse_pdf
from utils import validate_structure, generate_excel, summarize_data

# Configuração da interface
st.set_page_config(page_title="📄 Conversor de PDF Médico para Excel", layout="wide")

# Seletor de idioma
lang = st.sidebar.selectbox("🌐 Escolher idioma / Choose language", ["Português", "English"])
is_pt = lang == "Português"

# Textos multilíngues
T = {
    "title": {
        True: "📄 Conversor de PDF Médico ➜ Excel",
        False: "📄 Medical PDF ➜ Excel Converter"
    },
    "instruction": {
        True: "Envie um ou mais arquivos PDF com estrutura de 12 colunas e converta para Excel validado.",
        False: "Upload one or more structured 12-column medical PDFs and convert them into validated Excel files."
    },
    "uploader": {
        True: "📤 Enviar PDF(s)",
        False: "📤 Upload PDF(s)"
    },
    "processing": {
        True: "🔍 Processando",
        False: "🔍 Processing"
    },
    "download_header": {
        True: "📥 Baixar Excel (todos os PDFs combinados)",
        False: "📥 Download Excel (All PDFs Combined)"
    },
    "download_button": {
        True: "⬇️ Baixar Arquivo Excel",
        False: "⬇️ Download Excel File"
    },
    "results": {
        True: "📊 Resultados para",
        False: "📊 Results for"
    },
    "parsing_success": {
        True: "✅ Parsing realizado com sucesso.",
        False: "✅ Parsing completed successfully."
    },
    "structure_valid": {
        True: "✅ Estrutura validada com 12 colunas.",
        False: "✅ Structure validated with 12 columns."
    },
    "structure_issues": {
        True: "⚠️ Problemas estruturais:",
        False: "⚠️ Structural issues:"
    },
    "parsing_errors": {
        True: "❌ Problemas de parsing detectados:",
        False: "❌ Parsing issues detected:"
    },
    "editable_table": {
        True: "### ✏️ Tabela editável (primeiras 50 linhas)",
        False: "### ✏️ Editable Table (first 50 rows)"
    },
    "summary": {
        True: "### 🧠 Resumo dos dados extraídos",
        False: "### 🧠 Summary of extracted data"
    },
    "debug": {
        True: "### 🖼️ Visualização das páginas do PDF (debug)",
        False: "### 🖼️ PDF Page Debug Preview"
    }
}

# Título e instruções
st.title(T["title"][is_pt])
st.markdown(T["instruction"][is_pt])
uploaded_files = st.file_uploader(T["uploader"][is_pt], type=["pdf"], accept_multiple_files=True)

if uploaded_files:
    combined_dataframes = []
    debug_info = []

    for uploaded_file in uploaded_files:
        with st.spinner(f"{T['processing'][is_pt]}: {uploaded_file.name}"):
            tables, debug_images, parse_errors = parse_pdf(uploaded_file)

        valid_tables, structure_issues = validate_structure(tables)

        if valid_tables:
            final_df = pd.concat(valid_tables, ignore_index=True)
            combined_dataframes.append(final_df)
            debug_info.append((uploaded_file.name, final_df, parse_errors, structure_issues, debug_images))

    # Mostrar botão de download no TOPO
    if combined_dataframes:
        export_df = pd.concat(combined_dataframes, ignore_index=True)
        excel_file = generate_excel(export_df)

        st.subheader(T["download_header"][is_pt])
        st.download_button(
            T["download_button"][is_pt],
            data=excel_file,
            file_name="parsed_reports.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # Mostrar dados de cada arquivo individual
    for file_name, final_df, parse_errors, structure_issues, debug_images in debug_info:
        st.divider()
        st.subheader(f"{T['results'][is_pt]}: {file_name}")

        if parse_errors:
            st.error(T["parsing_errors"][is_pt])
            for err in parse_errors:
                st.text(f"• {err}")
        else:
            st.success(T["parsing_success"][is_pt])

        if structure_issues:
            st.warning(T["structure_issues"][is_pt])
            for issue in structure_issues:
                st.text(f"• {issue}")
        else:
            st.success(T["structure_valid"][is_pt])

        st.markdown(T["editable_table"][is_pt])
        st.data_editor(final_df.head(50), use_container_width=True, num_rows="dynamic")

        st.markdown(T["summary"][is_pt])
        summary = summarize_data(final_df)
        st.json(summary)

        st.markdown(T["debug"][is_pt])
        for i, img in enumerate(debug_images):
            st.image(img, caption=f"Página {i+1}" if is_pt else f"Page {i+1}", use_container_width=True)

