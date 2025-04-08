import pandas as pd
import io

EXPECTED_COLUMNS = [
    "Prontuário", "Paciente", "Local", "Início do tratamento", "Fim do tratamento",
    "Dias tratamento", "Medicamento", "Dose", "Frequência", "Unidade", "Via", "Prescrito por"
]

def validate_structure(tables):
    valid_tables = []
    issues = []
    for headers, rows in tables:
        if len(headers) != 12:
            issues.append("Header does not contain exactly 12 columns.")
            continue
        df = pd.DataFrame(rows, columns=headers)
        if df.shape[1] != 12:
            issues.append("Row does not contain 12 columns.")
            continue
        df.columns = EXPECTED_COLUMNS
        valid_tables.append(df)
    return valid_tables, issues

def generate_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
        writer.close()
    output.seek(0)
    return output

def summarize_data(df):
    return {
        "Total Rows": len(df),
        "Unique Patients": df["Paciente"].nunique(),
        "Unique Medications": df["Medicamento"].nunique(),
        "Prescribed By": df["Prescrito por"].nunique(),
        "Date Range": f"{df['Início do tratamento'].min()} to {df['Fim do tratamento'].max()}"
    }
