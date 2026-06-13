"""
PDF Report Generator
Generates downloadable RCA reports in PDF format
"""
from typing import Dict, Any, Optional
from datetime import datetime
from io import BytesIO
from loguru import logger

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    logger.warning("reportlab not installed. PDF generation will not be available.")


class PDFGenerator:
    """
    Service for generating RCA reports in PDF format
    
    Contents:
    - Executive Summary
    - Timeline
    - Root Cause
    - Severity & Risk Score
    - Recommendations
    - Prevention Plan
    """
    
    def __init__(self):
        """Initialize PDF generator"""
        if not REPORTLAB_AVAILABLE:
            logger.error("reportlab library not available. Install with: pip install reportlab")
            self.available = False
        else:
            self.available = True
            logger.info("PDF generator initialized")
    
    def generate_rca_pdf(
        self,
        incident_id: str,
        incident_description: str,
        rca_text: str,
        severity: str,
        risk_score: float,
        confidence: float,
        affected_service: str,
        occurred_at: Optional[str] = None,
        resolved_at: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> BytesIO:
        """
        Generate PDF report for RCA
        
        Args:
            incident_id: Incident identifier
            incident_description: Incident description
            rca_text: Full RCA text (markdown)
            severity: Severity level
            risk_score: Risk score (0-100)
            confidence: Confidence level (0-100)
            affected_service: Affected service
            occurred_at: When incident occurred
            resolved_at: When incident was resolved
            metadata: Additional metadata
            
        Returns:
            BytesIO buffer containing PDF
        """
        if not self.available:
            raise RuntimeError("PDF generation not available. Install reportlab: pip install reportlab")
        
        try:
            logger.info(f"Generating PDF for incident {incident_id}")
            
            # Create PDF buffer
            buffer = BytesIO()
            
            # Create document
            doc = SimpleDocTemplate(
                buffer,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Container for the 'Flowable' objects
            elements = []
            
            # Define styles
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1a1a1a'),
                spaceAfter=30,
                alignment=TA_CENTER,
                fontName='Helvetica-Bold'
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=12,
                spaceBefore=12,
                fontName='Helvetica-Bold'
            )
            
            subheading_style = ParagraphStyle(
                'CustomSubHeading',
                parent=styles['Heading3'],
                fontSize=14,
                textColor=colors.HexColor('#34495e'),
                spaceAfter=10,
                spaceBefore=10,
                fontName='Helvetica-Bold'
            )
            
            body_style = ParagraphStyle(
                'CustomBody',
                parent=styles['BodyText'],
                fontSize=11,
                textColor=colors.HexColor('#2c3e50'),
                spaceAfter=12,
                alignment=TA_JUSTIFY,
                fontName='Helvetica'
            )
            
            # Title
            elements.append(Paragraph("Root Cause Analysis Report", title_style))
            elements.append(Spacer(1, 0.2 * inch))
            
            # Incident Information Box
            incident_data = [
                ['Incident ID:', incident_id],
                ['Severity:', self._format_severity(severity)],
                ['Risk Score:', f"{risk_score:.1f}/100 (Confidence: {confidence:.0f}%)"],
                ['Affected Service:', affected_service],
            ]
            
            if occurred_at:
                incident_data.append(['Occurred At:', occurred_at])
            if resolved_at:
                incident_data.append(['Resolved At:', resolved_at])
            
            incident_table = Table(incident_data, colWidths=[2*inch, 4*inch])
            incident_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#bdc3c7')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            
            elements.append(incident_table)
            elements.append(Spacer(1, 0.3 * inch))
            
            # Incident Description
            elements.append(Paragraph("Incident Description", heading_style))
            elements.append(Paragraph(incident_description, body_style))
            elements.append(Spacer(1, 0.2 * inch))
            
            # Parse and add RCA content
            self._add_rca_content(elements, rca_text, heading_style, subheading_style, body_style)
            
            # Footer with generation date
            elements.append(Spacer(1, 0.3 * inch))
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#7f8c8d'),
                alignment=TA_CENTER
            )
            elements.append(Paragraph(
                f"Report generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}",
                footer_style
            ))
            elements.append(Paragraph(
                "SmartOps AI - Incident Intelligence Platform",
                footer_style
            ))
            
            # Build PDF
            doc.build(elements)
            
            # Reset buffer position
            buffer.seek(0)
            
            logger.info(f"PDF generated successfully for {incident_id}")
            return buffer
            
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def _format_severity(self, severity: str) -> str:
        """Format severity with color indicator"""
        severity_map = {
            'Critical': '🔴 Critical',
            'High': '🟠 High',
            'Medium': '🟡 Medium',
            'Low': '🟢 Low'
        }
        return severity_map.get(severity, severity)
    
    def _add_rca_content(self, elements, rca_text, heading_style, subheading_style, body_style):
        """
        Parse RCA markdown text and add to PDF
        
        Args:
            elements: List of PDF elements
            rca_text: RCA text in markdown format
            heading_style: Heading style
            subheading_style: Subheading style
            body_style: Body text style
        """
        from html import escape
        lines = rca_text.split('\n')
        current_section = []
        in_code_block = False
        code_block_lines = []
        
        for line in lines:
            stripped_line = line.strip()
            
            # Check for code block boundary
            if stripped_line.startswith('```'):
                if in_code_block:
                    # End of code block - process and add to elements
                    in_code_block = False
                    
                    formatted_lines = []
                    for cl in code_block_lines:
                        # Replace tabs with spaces
                        cl_processed = cl.replace('\t', '    ')
                        # Count leading spaces to preserve indentation
                        leading_spaces = len(cl_processed) - len(cl_processed.lstrip(' '))
                        if leading_spaces > 0:
                            escaped_line = '&nbsp;' * leading_spaces + escape(cl_processed[leading_spaces:])
                        else:
                            escaped_line = escape(cl_processed)
                        formatted_lines.append(escaped_line)
                    
                    code_html = "<br/>".join(formatted_lines)
                    
                    # Monospace code block styling
                    code_paragraph_style = ParagraphStyle(
                        'CodeBlockStyle',
                        fontName='Courier',
                        fontSize=8.5,
                        leading=10.5,
                        textColor=colors.HexColor('#2c3e50')
                    )
                    
                    p = Paragraph(code_html, code_paragraph_style)
                    t = Table([[p]], colWidths=[6.5 * inch])
                    t.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
                        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#e9ecef')),
                        ('LEFTPADDING', (0, 0), (-1, -1), 8),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                        ('TOPPADDING', (0, 0), (-1, -1), 8),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ]))
                    elements.append(t)
                    elements.append(Spacer(1, 0.15 * inch))
                    code_block_lines = []
                else:
                    # Start of code block
                    in_code_block = True
                    code_block_lines = []
                    
                    # Flush any current paragraph text before starting code block
                    if current_section:
                        section_text = ' '.join(current_section)
                        if section_text:
                            elements.append(Paragraph(self._clean_markdown(section_text), body_style))
                        current_section = []
                continue
            
            if in_code_block:
                code_block_lines.append(line)
                continue
                
            line = line.strip()
            if not line:
                if current_section:
                    # Add accumulated section content
                    section_text = ' '.join(current_section)
                    if section_text:
                        elements.append(Paragraph(self._clean_markdown(section_text), body_style))
                    current_section = []
                continue
            
            # Check for headings
            if line.startswith('## '):
                # Flush current section
                if current_section:
                    section_text = ' '.join(current_section)
                    if section_text:
                        elements.append(Paragraph(self._clean_markdown(section_text), body_style))
                    current_section = []
                
                # Add heading
                heading_text = line.replace('## ', '').strip()
                elements.append(Spacer(1, 0.15 * inch))
                elements.append(Paragraph(heading_text, heading_style))
                
            elif line.startswith('### '):
                # Flush current section
                if current_section:
                    section_text = ' '.join(current_section)
                    if section_text:
                        elements.append(Paragraph(self._clean_markdown(section_text), body_style))
                    current_section = []
                
                # Add subheading
                subheading_text = line.replace('### ', '').strip()
                elements.append(Paragraph(subheading_text, subheading_style))
                
            elif line.startswith('# '):
                # Main heading (H1)
                if current_section:
                    section_text = ' '.join(current_section)
                    if section_text:
                        elements.append(Paragraph(self._clean_markdown(section_text), body_style))
                    current_section = []
                
                heading_text = line.replace('# ', '').strip()
                elements.append(Spacer(1, 0.2 * inch))
                elements.append(Paragraph(heading_text, heading_style))
                
            elif line.startswith('- ') or line.startswith('* '):
                # Bullet point
                if current_section:
                    section_text = ' '.join(current_section)
                    if section_text:
                        elements.append(Paragraph(self._clean_markdown(section_text), body_style))
                    current_section = []
                
                bullet_text = line[2:].strip()
                elements.append(Paragraph(f"• {self._clean_markdown(bullet_text)}", body_style))
                
            elif line[0].isdigit() and line[1:3] in ['. ', ') ']:
                # Numbered list
                if current_section:
                    section_text = ' '.join(current_section)
                    if section_text:
                        elements.append(Paragraph(self._clean_markdown(section_text), body_style))
                    current_section = []
                
                elements.append(Paragraph(self._clean_markdown(line), body_style))
                
            else:
                # Regular paragraph text
                current_section.append(line)
        
        # Add any remaining section
        if current_section:
            section_text = ' '.join(current_section)
            if section_text:
                elements.append(Paragraph(self._clean_markdown(section_text), body_style))
    
    def _clean_markdown(self, text: str) -> str:
        """
        Clean markdown formatting for PDF
        
        Args:
            text: Markdown text
            
        Returns:
            Cleaned text safe for reportlab
        """
        import re
        from html import escape
        
        # First escape any existing HTML
        text = escape(text)
        
        # Now convert markdown to HTML tags
        # Bold: **text** or __text__
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'__(.+?)__', r'<b>\1</b>', text)
        
        # Italic: *text* or _text_ (but not in the middle of words)
        text = re.sub(r'(?<!\w)\*(.+?)\*(?!\w)', r'<i>\1</i>', text)
        text = re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'<i>\1</i>', text)
        
        # Code: `code` - just use monospace, no special font tag to avoid parsing issues
        text = re.sub(r'`([^`]+)`', r'\1', text)
        
        return text
    
    def generate_summary_pdf(
        self,
        incidents: list,
        title: str = "Incident Summary Report"
    ) -> BytesIO:
        """
        Generate summary PDF for multiple incidents
        
        Args:
            incidents: List of incident dictionaries
            title: Report title
            
        Returns:
            BytesIO buffer containing PDF
        """
        if not self.available:
            raise RuntimeError("PDF generation not available. Install reportlab: pip install reportlab")
        
        try:
            logger.info(f"Generating summary PDF for {len(incidents)} incidents")
            
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'Title',
                parent=styles['Heading1'],
                fontSize=20,
                alignment=TA_CENTER,
                spaceAfter=30
            )
            elements.append(Paragraph(title, title_style))
            elements.append(Spacer(1, 0.3 * inch))
            
            # Summary table
            table_data = [['Incident ID', 'Description', 'Severity', 'Risk Score', 'Status']]
            
            for incident in incidents:
                table_data.append([
                    incident.get('incident_id', 'N/A'),
                    incident.get('description', 'N/A')[:50] + '...',
                    incident.get('severity', 'N/A'),
                    f"{incident.get('risk_score', 0):.1f}",
                    incident.get('status', 'N/A')
                ])
            
            table = Table(table_data, colWidths=[1.2*inch, 2.5*inch, 0.8*inch, 0.8*inch, 0.8*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
            ]))
            
            elements.append(table)
            
            # Footer
            elements.append(Spacer(1, 0.5 * inch))
            footer_text = f"Generated on {datetime.now().strftime('%B %d, %Y')}"
            elements.append(Paragraph(footer_text, styles['Normal']))
            
            doc.build(elements)
            buffer.seek(0)
            
            logger.info("Summary PDF generated successfully")
            return buffer
            
        except Exception as e:
            logger.error(f"Error generating summary PDF: {e}")
            raise
    
    def is_available(self) -> bool:
        """Check if PDF generation is available"""
        return self.available
    
    def get_service_info(self) -> Dict[str, Any]:
        """
        Get PDF generator service information
        
        Returns:
            Service metadata
        """
        return {
            "service": "PDF Generator",
            "status": "operational" if self.available else "unavailable",
            "library": "reportlab" if REPORTLAB_AVAILABLE else "not installed",
            "capabilities": [
                "RCA report PDF generation",
                "Summary report generation",
                "Professional formatting",
                "Multi-page support",
                "Table formatting",
                "Markdown to PDF conversion"
            ] if self.available else [],
            "formats": ["PDF"] if self.available else [],
            "page_size": "Letter (8.5 x 11 inches)"
        }
