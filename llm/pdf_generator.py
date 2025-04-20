from fpdf import FPDF
import tempfile
import streamlit as st
import os

def save_report_as_pdf(report_text, pdf_filename):
    try:
        if not report_text:
            st.error("Report content is empty!")
            return None
            
        if not isinstance(report_text, str):
            report_text = str(report_text)

        pdf = FPDF()
        pdf.add_page()
        
        
        cleaned_lines = []
        current_section = ""
        
        for line in report_text.split('\n'):
            line = line.replace('**', '').replace('#', '').strip()
            
            if not line:  
                continue
                
            
            if line.lower().startswith("prediction"):
                current_section = "PREDICTION"
                cleaned_lines.append(('SECTION_HEADER', "PREDICTION"))
            elif line.lower().startswith("top drivers"):
                current_section = "TOP_DRIVERS"
                cleaned_lines.append(('SECTION_HEADER', "TOP DRIVERS"))
            elif line.lower().startswith("recommendations"):
                current_section = "RECOMMENDATIONS"
                cleaned_lines.append(('SECTION_HEADER', "RECOMMENDATIONS"))
            elif line.strip().endswith(":"):
                cleaned_lines.append(('SUBHEADER', line.replace(':', '').strip()))
            elif current_section == "TOP_DRIVERS" and line[0].isdigit():
                parts = line.split('-', 1)
                if len(parts) > 1:
                    cleaned_lines.append(('DRIVER_HEADER', parts[0].strip()))
                    cleaned_lines.append(('DRIVER_DETAIL', parts[1].strip()))
            else:
                cleaned_lines.append(('TEXT', line))

       
        for line_type, content in cleaned_lines:
            if line_type == 'SECTION_HEADER':
                pdf.set_font('Arial', 'B', 14)
                pdf.set_text_color(0, 0, 128)  
                pdf.cell(200, 10, txt=content, ln=1)
                pdf.ln(4)
                pdf.set_text_color(0, 0, 0)  
            elif line_type == 'SUBHEADER':
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(200, 8, txt=content, ln=1)
                pdf.set_font('Arial', '', 12)
            elif line_type == 'DRIVER_HEADER':
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(200, 8, txt=content, ln=1)
            elif line_type == 'DRIVER_DETAIL':
                pdf.set_font('Arial', '', 11)
                pdf.multi_cell(0, 6, txt=content)
                pdf.ln(4)
            else:
                pdf.set_font('Arial', '', 11)
                pdf.multi_cell(0, 6, txt=content)
                pdf.ln(4)

        
        temp_dir = tempfile.gettempdir()
        pdf_path = os.path.join(temp_dir, pdf_filename)
        
        pdf.output(pdf_path)
        
        
       
        if not os.path.exists(pdf_path):
            st.error("PDF file was not created!")
            return None
            
        return pdf_path
        
    except Exception as e:
        st.error(f"PDF generation failed: {e}")
        return None


