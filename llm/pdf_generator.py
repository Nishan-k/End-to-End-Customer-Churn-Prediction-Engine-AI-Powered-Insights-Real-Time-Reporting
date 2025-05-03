from fpdf import FPDF
import tempfile
import streamlit as st
import os
import re

class UTF8PDF(FPDF):
    """Custom PDF class with UTF-8 support"""
    def __init__(self):
        # Use A4 format with adequate margins (left, top, right) in mm
        super().__init__(orientation='P', unit='mm', format='A4')
        # Set generous margins to prevent text being cut off
        self.set_margins(15, 15, 15)  # left, top, right margins in mm
        # Add DejaVu font which has good Unicode support
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        self.add_font('DejaVu', 'B', 'DejaVuSansCondensed-Bold.ttf', uni=True)

def save_report_as_pdf(report_text, pdf_filename):
    try:
        if not report_text:
            st.error("Report content is empty!")
            return None
            
        if not isinstance(report_text, str):
            report_text = str(report_text)

        # Sanitize special characters that might cause encoding issues
        report_text = sanitize_text_for_pdf(report_text)
            
        # Create PDF with UTF-8 support
        try:
            # Try to use custom UTF8PDF with DejaVu fonts if available
            pdf = UTF8PDF()
            use_dejavu = True
        except Exception as font_error:
            # Fallback to standard PDF with Arial font
            st.warning(f"Using standard fonts due to: {font_error}")
            pdf = FPDF(orientation='P', unit='mm', format='A4')
            pdf.set_margins(15, 15, 15)  # Set generous margins (left, top, right)
            use_dejavu = False
            
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

        # Set default font family based on availability
        font_family = 'DejaVu' if use_dejavu else 'Arial'
       
        for line_type, content in cleaned_lines:
            if line_type == 'SECTION_HEADER':
                pdf.set_font(font_family, 'B', 14)
                pdf.set_text_color(0, 0, 128)
                # Use cell with borders=0 for UTF-8 safety
                pdf.cell(0, 10, txt=content, ln=1, border=0)
                pdf.ln(4)
                pdf.set_text_color(0, 0, 0)
            elif line_type == 'SUBHEADER':
                pdf.set_font(font_family, 'B', 12)
                pdf.cell(0, 8, txt=content, ln=1, border=0)
                pdf.set_font(font_family, '', 12)
            elif line_type == 'DRIVER_HEADER':
                pdf.set_font(font_family, 'B', 12)
                pdf.cell(0, 8, txt=content, ln=1, border=0)
            elif line_type == 'DRIVER_DETAIL':
                pdf.set_font(font_family, '', 11)
                # Use multi_cell with width slightly less than page width to ensure text doesn't get cut off
                pdf.multi_cell(0, 6, txt=content, align='L')
                pdf.ln(2)
            else:
                pdf.set_font(font_family, '', 11)
                pdf.multi_cell(0, 6, txt=content)
                pdf.ln(4)

        # Create temp directory if it doesn't exist
        temp_dir = tempfile.gettempdir()
        pdf_path = os.path.join(temp_dir, pdf_filename)
        
        # Try to save the PDF, handling potential encoding issues
        try:
            pdf.output(pdf_path)
        except UnicodeEncodeError:
            # If UTF-8 fails, try a more aggressive character replacement approach
            st.warning("Handling special characters in PDF generation")
            fallback_save_pdf(pdf, cleaned_lines, pdf_path, font_family)
        
        if not os.path.exists(pdf_path):
            st.error("PDF file was not created!")
            return None
            
        return pdf_path
        
    except Exception as e:
        st.error(f"PDF generation failed: {e}")
        return None

def sanitize_text_for_pdf(text):
    """Replace problematic Unicode characters with ASCII equivalents"""
    # Common replacements for problematic characters
    replacements = {
        '\u2013': '-',  # en dash
        '\u2014': '--',  # em dash
        '\u2018': "'",   # left single quote
        '\u2019': "'",   # right single quote
        '\u201c': '"',   # left double quote
        '\u201d': '"',   # right double quote
        '\u2022': '*',   # bullet
        '\u2026': '...', # ellipsis
        '\u00a9': '(c)', # copyright
        '\u00ae': '(R)', # registered trademark
        '\u2122': 'TM',  # trademark
    }
    
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    
    # Replace other non-ASCII characters with their closest ASCII equivalent or '?'
    return ''.join(c if ord(c) < 128 else '?' for c in text)

def fallback_save_pdf(pdf, cleaned_lines, pdf_path, font_family='Arial'):
    """Fallback method to save PDF with aggressive character sanitization"""
    pdf = FPDF(orientation='P', unit='mm', format='A4')  # Create a new PDF object
    pdf.set_margins(15, 15, 15)  # Set generous margins (left, top, right)
    pdf.add_page()
    
    for line_type, content in cleaned_lines:
        # Aggressively sanitize content
        content = re.sub(r'[^\x00-\x7F]+', '?', content)
        
        if line_type == 'SECTION_HEADER':
            pdf.set_font('Arial', 'B', 14)
            pdf.set_text_color(0, 0, 128)
            pdf.cell(0, 10, txt=content, ln=1)
            pdf.ln(4)
            pdf.set_text_color(0, 0, 0)
        elif line_type == 'SUBHEADER':
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, txt=content, ln=1)
            pdf.set_font('Arial', '', 12)
        elif line_type == 'DRIVER_HEADER':
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 8, txt=content, ln=1)
        elif line_type == 'DRIVER_DETAIL':
            pdf.set_font('Arial', '', 11)
            pdf.multi_cell(0, 6, txt=content)
            pdf.ln(4)
        else:
            pdf.set_font('Arial', '', 11)
            pdf.multi_cell(0, 6, txt=content)
            pdf.ln(4)
    
    pdf.output(pdf_path)



# from fpdf import FPDF
# import tempfile
# import streamlit as st
# import os
# import re

# class UTF8PDF(FPDF):
#     """Custom PDF class with UTF-8 support"""
#     def __init__(self):
#         super().__init__()
#         # Add DejaVu font which has good Unicode support
#         self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
#         self.add_font('DejaVu', 'B', 'DejaVuSansCondensed-Bold.ttf', uni=True)

# def save_report_as_pdf(report_text, pdf_filename):
#     try:
#         if not report_text:
#             st.error("Report content is empty!")
#             return None
            
#         if not isinstance(report_text, str):
#             report_text = str(report_text)

#         # Sanitize special characters that might cause encoding issues
#         report_text = sanitize_text_for_pdf(report_text)
            
#         # Create PDF with UTF-8 support
#         try:
#             # Try to use custom UTF8PDF with DejaVu fonts if available
#             pdf = UTF8PDF()
#             use_dejavu = True
#         except Exception as font_error:
#             # Fallback to standard PDF with Arial font
#             st.warning(f"Using standard fonts due to: {font_error}")
#             pdf = FPDF()
#             use_dejavu = False
            
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

#         # Set default font family based on availability
#         font_family = 'DejaVu' if use_dejavu else 'Arial'
       
#         for line_type, content in cleaned_lines:
#             if line_type == 'SECTION_HEADER':
#                 pdf.set_font(font_family, 'B', 14)
#                 pdf.set_text_color(0, 0, 128)
#                 # Use cell with borders=0 for UTF-8 safety
#                 pdf.cell(0, 10, txt=content, ln=1, border=0)
#                 pdf.ln(4)
#                 pdf.set_text_color(0, 0, 0)
#             elif line_type == 'SUBHEADER':
#                 pdf.set_font(font_family, 'B', 12)
#                 pdf.cell(0, 8, txt=content, ln=1, border=0)
#                 pdf.set_font(font_family, '', 12)
#             elif line_type == 'DRIVER_HEADER':
#                 pdf.set_font(font_family, 'B', 12)
#                 pdf.cell(0, 8, txt=content, ln=1, border=0)
#             elif line_type == 'DRIVER_DETAIL':
#                 pdf.set_font(font_family, '', 11)
#                 pdf.multi_cell(0, 6, txt=content)
#                 pdf.ln(4)
#             else:
#                 pdf.set_font(font_family, '', 11)
#                 pdf.multi_cell(0, 6, txt=content)
#                 pdf.ln(4)

#         # Create temp directory if it doesn't exist
#         temp_dir = tempfile.gettempdir()
#         pdf_path = os.path.join(temp_dir, pdf_filename)
        
#         # Try to save the PDF, handling potential encoding issues
#         try:
#             pdf.output(pdf_path)
#         except UnicodeEncodeError:
#             # If UTF-8 fails, try a more aggressive character replacement approach
#             st.warning("Handling special characters in PDF generation")
#             fallback_save_pdf(pdf, cleaned_lines, pdf_path, font_family)
        
#         if not os.path.exists(pdf_path):
#             st.error("PDF file was not created!")
#             return None
            
#         return pdf_path
        
#     except Exception as e:
#         st.error(f"PDF generation failed: {e}")
#         return None

# def sanitize_text_for_pdf(text):
#     """Replace problematic Unicode characters with ASCII equivalents"""
#     # Common replacements for problematic characters
#     replacements = {
#         '\u2013': '-',  # en dash
#         '\u2014': '--',  # em dash
#         '\u2018': "'",   # left single quote
#         '\u2019': "'",   # right single quote
#         '\u201c': '"',   # left double quote
#         '\u201d': '"',   # right double quote
#         '\u2022': '*',   # bullet
#         '\u2026': '...', # ellipsis
#         '\u00a9': '(c)', # copyright
#         '\u00ae': '(R)', # registered trademark
#         '\u2122': 'TM',  # trademark
#     }
    
#     for char, replacement in replacements.items():
#         text = text.replace(char, replacement)
    
#     # Replace other non-ASCII characters with their closest ASCII equivalent or '?'
#     return ''.join(c if ord(c) < 128 else '?' for c in text)

# def fallback_save_pdf(pdf, cleaned_lines, pdf_path, font_family='Arial'):
#     """Fallback method to save PDF with aggressive character sanitization"""
#     pdf = FPDF()  # Create a new PDF object
#     pdf.add_page()
    
#     for line_type, content in cleaned_lines:
#         # Aggressively sanitize content
#         content = re.sub(r'[^\x00-\x7F]+', '?', content)
        
#         if line_type == 'SECTION_HEADER':
#             pdf.set_font('Arial', 'B', 14)
#             pdf.set_text_color(0, 0, 128)
#             pdf.cell(0, 10, txt=content, ln=1)
#             pdf.ln(4)
#             pdf.set_text_color(0, 0, 0)
#         elif line_type == 'SUBHEADER':
#             pdf.set_font('Arial', 'B', 12)
#             pdf.cell(0, 8, txt=content, ln=1)
#             pdf.set_font('Arial', '', 12)
#         elif line_type == 'DRIVER_HEADER':
#             pdf.set_font('Arial', 'B', 12)
#             pdf.cell(0, 8, txt=content, ln=1)
#         elif line_type == 'DRIVER_DETAIL':
#             pdf.set_font('Arial', '', 11)
#             pdf.multi_cell(0, 6, txt=content)
#             pdf.ln(4)
#         else:
#             pdf.set_font('Arial', '', 11)
#             pdf.multi_cell(0, 6, txt=content)
#             pdf.ln(4)
    
#     pdf.output(pdf_path)













# from fpdf import FPDF
# import tempfile
# import streamlit as st
# import os

# def save_report_as_pdf(report_text, pdf_filename):
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
#         pdf_path = os.path.join(temp_dir, pdf_filename)
        
#         pdf.output(pdf_path)
        
        
       
#         if not os.path.exists(pdf_path):
#             st.error("PDF file was not created!")
#             return None
            
#         return pdf_path
        
#     except Exception as e:
#         st.error(f"PDF generation failed: {e}")
#         return None


