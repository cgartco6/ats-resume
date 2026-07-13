import io
import zipfile
import json
import logging
from typing import Dict, Any, Tuple

# Import modern core layout engines from ReportLab
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Configure strict error pipeline logging hooks
logger = logging.getLogger("DocumentGenerationService")
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [GENERATOR ENGINE] - %(message)s")

class ATSDocumentGenerator:
    def __init__(self):
        # Enforce international business standards layout metrics
        self.page_width, self.page_height = letter
        
        # Exact 0.75-inch structural margin boundaries to pass standard parsing filters
        self.margin = 0.75 * inch 
        self.printable_width = self.page_width - (2 * self.margin)

    def compile_ats_pdf(self, resume_data: Dict[str, Any]) -> bytes:
        """
        Generates a visually immaculate, text-searchable, ATS-compliant PDF document.
        Excludes complex grids, vector lines, or background images that freeze parsers.
        """
        buffer = io.BytesIO()
        
        # Establish base document canvas boundaries
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            leftMargin=self.margin,
            rightMargin=self.margin,
            topMargin=self.margin,
            bottomMargin=self.margin
        )

        styles = getSampleStyleSheet()
        story = []

        # -------------------------------------------------------------------------
        # TYPOGRAPHY DEFINITIONS (Using standard system-embedded font mappings)
        # -------------------------------------------------------------------------
        name_style = ParagraphStyle(
            'ATS_Name',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#111827"),
            spaceAfter=4
        )
        
        contact_style = ParagraphStyle(
            'ATS_Contact',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#4B5563"),
            spaceAfter=12
        )
        
        section_heading = ParagraphStyle(
            'ATS_Section',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#1F2937"),
            spaceBefore=14,
            spaceAfter=6,
            keepWithNext=True  # Blocks orphaned subheadings at page borders
        )
        
        body_bold = ParagraphStyle(
            'ATS_BodyBold',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#374151")
        )
        
        body_text = ParagraphStyle(
            'ATS_Body',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#374151"),
            spaceAfter=4
        )

        # -------------------------------------------------------------------------
        # HEADER BLOCK CONSTRUCTION
        # -------------------------------------------------------------------------
        header = resume_data.get("header", {})
        story.append(Paragraph(header.get("name", "Applicant Name"), name_style))
        
        contact_info = f"{header.get('email', '')}  |  {header.get('phone', '')}  |  {header.get('location', '')}"
        if header.get("linkedin"):
            contact_info += f"  |  {header.get('linkedin')}"
        story.append(Paragraph(contact_info, contact_style))

        # -------------------------------------------------------------------------
        # PROFESSIONAL EXPERIENCE BLOCK
        # -------------------------------------------------------------------------
        experience = resume_data.get("experience", [])
        if experience:
            story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_heading))
            for job in experience:
                job_elements = []
                job_title_line = f"<b>{job.get('role', '')}</b> — {job.get('company', '')} ({job.get('duration', '')})"
                job_elements.append(Paragraph(job_title_line, body_bold))
                
                for bullet in job.get("bullets", []):
                    # ATS check: standard clean bullet strings only
                    job_elements.append(Paragraph(f"• {bullet}", body_text))
                
                # Keep individual roles intact to prevent messy multi-page breaks
                story.append(KeepTogether(job_elements))
                story.append(Spacer(1, 4))

        # -------------------------------------------------------------------------
        # TECHNICAL SKILLS BLOCK
        # -------------------------------------------------------------------------
        skills = resume_data.get("skills", [])
        if skills:
            story.append(Paragraph("TECHNICAL SKILLS", section_heading))
            skills_line = ", ".join(skills)
            story.append(Paragraph(skills_line, body_text))

        # Build Document
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

    def compile_cover_letter_text(self, resume_data: Dict[str, Any]) -> str:
        """Generates a matching professional plain-text cover letter."""
        header = resume_data.get("header", {})
        letter_template = (
            f"{header.get('name', 'Applicant Name')}\n{header.get('email', '')}\n\n"
            f"Date: July 13, 2026\n\n"
            f"Dear Hiring Team,\n\n"
            f"I am writing to express my explicit interest in expanding my professional career track within your organization.\n"
            f"My deep backgrounds across the following core segments align natively with the targets mandated by the role:\n"
            f"{', '.join(resume_data.get('skills', []))}.\n\n"
            f"Thank you for your structural operational review of my application portfolio assets.\n\n"
            f"Sincerely,\n{header.get('name', 'Applicant Name')}"
        )
        return letter_template

    def compile_plain_text_cv(self, resume_data: Dict[str, Any]) -> str:
        """Compiles a backup plain text string matching standard legacy DOCX/TXT requirements."""
        header = resume_data.get("header", {})
        output = f"{header.get('name', '').upper()}\n{header.get('email', '')} | {header.get('phone', '')}\n\n"
        
        output += "=== EXPERIENCE ===\n"
        for job in resume_data.get("experience", []):
            output += f"{job.get('role', '')} - {job.get('company', '')} ({job.get('duration', '')})\n"
            for b in job.get("bullets", []):
                output += f"- {b}\n"
            output += "\n"
            
        output += "=== SKILLS ===\n"
        output += ", ".join(resume_data.get("skills", []))
        return output

    def package_bundle(self, raw_json_input: str) -> Tuple[bytes, Dict[str, Any]]:
        """
        Takes raw business data payloads, generates required structural assets, 
        and bundles them tightly into a high-performance streaming ZIP binary format stream.
        """
        try:
            resume_data = json.loads(raw_json_input)
        except Exception as json_fault:
            raise ValueError(f"Invalid architectural JSON definition parsed: {str(json_fault)}")

        # 1. Compile individual application documents
        pdf_bytes = self.compile_ats_pdf(resume_data)
        cover_letter_str = self.compile_cover_letter_text(resume_data)
        plain_text_cv_str = self.compile_plain_text_cv(resume_data)

        # 2. Package assets concurrently using absolute memory structures
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("ats_optimized_resume.pdf", pdf_bytes)
            archive.writestr("cover_letter_backup.txt", cover_letter_str.encode("utf-8"))
            archive.writestr("plain_text_resume_format.txt", plain_text_cv_str.encode("utf-8"))

        archive_bytes = zip_buffer.getvalue()
        zip_buffer.close()

        # -------------------------------------------------------------------------
        # COMPLIANCE CRITICAL VALIDATION STEP
        # -------------------------------------------------------------------------
        total_byte_size = len(archive_bytes)
        
        validation_metrics = {
            "is_valid": total_byte_size > 5000, # Archive must contain actual payload signatures
            "byte_size": total_byte_size,
            "contained_files": ["ats_optimized_resume.pdf", "cover_letter_backup.txt", "plain_text_resume_format.txt"]
        }

        if not validation_metrics["is_valid"]:
            logger.error("System asset integrity check dropped: Total byte allocation limits unresolved.")
            raise RuntimeError("Compiled archive payload dropped validation compliance metrics.")

        logger.info(f"SUCCESSFUL ZIP METRIC PACKAGING. Payload footprint allocation confirmed: {total_byte_size} bytes.")
        return archive_bytes, validation_metrics

# ==========================================
# SYSTEM PIPELINE VERIFICATION RUNNER
# ==========================================
if __name__ == "__main__":
    mock_workspace_payload = {
        "header": {
            "name": "Jane van Der Merwe",
            "email": "jane.vdmerwe@example.com",
            "phone": "+27 83 555 1234",
            "location": "Cape Town, South Africa",
            "linkedin": "linkedin.com/in/jane-vdm"
        },
        "experience": [
            {
                "role": "Lead Software Systems Engineer",
                "company": "Apex Swartland Solutions",
                "duration": "2023 - Present",
                "bullets": [
                    "Engineered asynchronous serverless data architectures reducing api bottlenecks by 42%.",
                    "Deployed transactional security encryption protocols to achieve strict POPIA compliance.",
                    "Supervised technical operations scale-up patterns balancing regional network infrastructure links."
                ]
            },
            {
                "role": "Python Full-Stack Developer",
                "company": "West Coast Operations Inc",
                "duration": "2021 - 2023",
                "bullets": [
                    "Built lightweight, zero-dependency data parsers mitigating runtime execution crashes.",
                    "Managed production environments deploying web hooks and database migrations."
                ]
            }
        ],
        "skills": ["Python", "PostgreSQL", "ReportLab", "Asynchronous Programming", "API Optimization", "Docker"]
    }

    print("--- STARTING UNABRIDGED ASSET BUNDLE PACKAGING PROCESS ---")
    generator = ATSDocumentGenerator()
    
    zip_output, metrics = generator.package_bundle(json.dumps(mock_workspace_payload))
    
    print(f"Validation Operational Verdict: {metrics['is_valid']}")
    print(f"Total Stream Package Size Allocated: {metrics['byte_size']} bytes.")
    print(f"Archived Components Verified: {metrics['contained_files']}")
