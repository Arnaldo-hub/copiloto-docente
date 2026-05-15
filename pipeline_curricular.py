import os

print("🚀 INICIANDO PIPELINE CURRICULAR")

# =========================================
# PDF → TXT
# =========================================

print("📄 Extrayendo PDFs...")

os.system(

    "python pdf_a_txt.py"

)

# =========================================
# TXT → JSON
# =========================================

print("🧠 Normalizando currículo...")

os.system(

    "python normalizador_curricular.py"

)

print("✅ PIPELINE FINALIZADO")
