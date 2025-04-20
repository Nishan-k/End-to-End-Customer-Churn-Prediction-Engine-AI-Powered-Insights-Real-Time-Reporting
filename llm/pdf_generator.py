from fpdf import FPDF
import tempfile
import streamlit as st
import os

# def save_report_as_pdf(report_text):
#     try:
#         if not report_text:
#             st.error("Report content is empty!")
#             return None
            
#         if not isinstance(report_text, str):
#             report_text = str(report_text)

#         pdf = FPDF()
#         pdf.add_page()
        
        
#         cleaned_lines = []
#         current_section = ""
        
#         for line in report_text.split('\n'):
#             line = line.replace('**', '').replace('#', '').strip()
            
#             if not line:  
#                 continue
                
            
#             if line.lower().startswith("prediction"):
#                 current_section = "PREDICTION"
#                 cleaned_lines.append(('SECTION_HEADER', "PREDICTION"))
#             elif line.lower().startswith("top drivers"):
#                 current_section = "TOP_DRIVERS"
#                 cleaned_lines.append(('SECTION_HEADER', "TOP DRIVERS"))
#             elif line.lower().startswith("recommendations"):
#                 current_section = "RECOMMENDATIONS"
#                 cleaned_lines.append(('SECTION_HEADER', "RECOMMENDATIONS"))
#             elif line.strip().endswith(":"):
#                 cleaned_lines.append(('SUBHEADER', line.replace(':', '').strip()))
#             elif current_section == "TOP_DRIVERS" and line[0].isdigit():
#                 parts = line.split('-', 1)
#                 if len(parts) > 1:
#                     cleaned_lines.append(('DRIVER_HEADER', parts[0].strip()))
#                     cleaned_lines.append(('DRIVER_DETAIL', parts[1].strip()))
#             else:
#                 cleaned_lines.append(('TEXT', line))

       
#         for line_type, content in cleaned_lines:
#             if line_type == 'SECTION_HEADER':
#                 pdf.set_font('Arial', 'B', 14)
#                 pdf.set_text_color(0, 0, 128)  
#                 pdf.cell(200, 10, txt=content, ln=1)
#                 pdf.ln(4)
#                 pdf.set_text_color(0, 0, 0)  
#             elif line_type == 'SUBHEADER':
#                 pdf.set_font('Arial', 'B', 12)
#                 pdf.cell(200, 8, txt=content, ln=1)
#                 pdf.set_font('Arial', '', 12)
#             elif line_type == 'DRIVER_HEADER':
#                 pdf.set_font('Arial', 'B', 12)
#                 pdf.cell(200, 8, txt=content, ln=1)
#             elif line_type == 'DRIVER_DETAIL':
#                 pdf.set_font('Arial', '', 11)
#                 pdf.multi_cell(0, 6, txt=content)
#                 pdf.ln(4)
#             else:
#                 pdf.set_font('Arial', '', 11)
#                 pdf.multi_cell(0, 6, txt=content)
#                 pdf.ln(4)

        
#         temp_dir = tempfile.gettempdir()
#         pdf_path = os.path.join(temp_dir, "customer_churn_report.pdf")
        
#         pdf.output(pdf_path)
        
       
#         if not os.path.exists(pdf_path):
#             st.error("PDF file was not created!")
#             return None
            
#         return pdf_path
        
#     except Exception as e:
#         st.error(f"PDF generation failed: {e}")
#         return None


def save_report_as_pdf(report_text):
    try:
        if not report_text:
            st.error("Report content is empty!")
            return None
            
        if not isinstance(report_text, str):
            report_text = str(report_text)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(200, 10, txt="Customer Churn Risk Report", ln=1, align='C')
        pdf.ln(10)
        
        # Split report into sections
        sections = {}
        current_section = "INTRO"
        sections[current_section] = []
        
        for line in report_text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Check for section headers (case insensitive)
            lower_line = line.lower()
            if "prediction" in lower_line and not sections.get("PREDICTION"):
                current_section = "PREDICTION"
                sections[current_section] = []
            elif any(x in lower_line for x in ["top drivers", "key factors", "main factors"]):
                current_section = "TOP_DRIVERS"
                sections[current_section] = []
            elif "recommendation" in lower_line:
                current_section = "RECOMMENDATIONS"
                sections[current_section] = []
            elif "business interpretation" in lower_line:
                current_section = "BUSINESS_INTERPRETATION"
                sections[current_section] = []
            else:
                sections[current_section].append(line)
        
        # Write sections to PDF
        for section, lines in sections.items():
            if section == "INTRO":
                continue  # Skip intro or handle differently if needed
                
            # Write section header
            pdf.set_font('Arial', 'B', 14)
            pdf.set_text_color(0, 0, 128)
            pdf.cell(200, 10, txt=section.replace("_", " "), ln=1)
            pdf.ln(4)
            pdf.set_text_color(0, 0, 0)
            
            # Write section content
            pdf.set_font('Arial', '', 11)
            for line in lines:
                # Check if line is a subheader (ends with colon or is short)
                if line.endswith(':') or (len(line) < 50 and not line[0].isdigit()):
                    pdf.set_font('Arial', 'B', 12)
                    pdf.cell(200, 8, txt=line, ln=1)
                    pdf.set_font('Arial', '', 11)
                else:
                    pdf.multi_cell(0, 6, txt=line)
                    pdf.ln(2)
            
            pdf.ln(5)
        
        # Create and save PDF
        temp_dir = tempfile.gettempdir()
        pdf_path = os.path.join(temp_dir, "customer_churn_report.pdf")
        pdf.output(pdf_path)
        
        if not os.path.exists(pdf_path):
            st.error("PDF file was not created!")
            return None
            
        return pdf_path
        
    except Exception as e:
        st.error(f"PDF generation failed: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return None