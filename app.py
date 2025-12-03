import streamlit as st
from fpdf import FPDF

# ---------- STYLE COLORS FROM HTML ----------
PRIMARY_GREEN = (27, 94, 32)     # #1b5e20
ACCENT_GREEN = (76, 175, 80)     # #4caf50
LIGHT_GREEN = (232, 245, 233)    # #e8f5e9
BLACK = (26, 26, 26)             # #1a1a1a
DARK_GRAY = (66, 66, 66)         # #424242


# ---------- PDF HELPER -----------

class IntakePDF(FPDF):
    def header(self):
        # Dark green band with white title (like HTML header/top border)
        self.set_fill_color(*PRIMARY_GREEN)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, "Project Intake: Finance & Legal", ln=1, fill=True)
        self.set_font("Helvetica", "", 11)
        self.cell(0, 7, "Digital Transformation Request Form", ln=1)
        # thin line below
        self.set_draw_color(*LIGHT_GREEN)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)
        # Reset text color for body
        self.set_text_color(*BLACK)

    def section_title(self, title):
        # Light-green band with section title
        self.ln(4)
        self.set_fill_color(*LIGHT_GREEN)
        self.set_text_color(*PRIMARY_GREEN)
        self.set_font("Helvetica", "B", 12)
        # ensure we start from left margin
        self.set_x(self.l_margin)
        self.cell(self.w - self.l_margin - self.r_margin, 8, title, ln=1, fill=True)
        # underline section with a subtle line
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.2)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)
        self.set_text_color(*BLACK)

    def guide_box(self, title, text):
        """
        Render a "guide-box" similar to the HTML: light green background,
        bold label, then smaller explanatory text.
        """
        box_width = self.w - self.l_margin - self.r_margin

        self.set_fill_color(*LIGHT_GREEN)
        self.set_text_color(*PRIMARY_GREEN)
        self.set_font("Helvetica", "B", 10)

        self.set_x(self.l_margin)
        self.multi_cell(box_width, 5, title, border=0, fill=True)

        self.set_font("Helvetica", "", 9)
        self.set_x(self.l_margin)
        self.multi_cell(box_width, 5, text, border=0, fill=True)

        self.ln(3)
        self.set_text_color(*BLACK)

    def question(self, label, answer):
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(*PRIMARY_GREEN)
        self.set_x(self.l_margin)
        self.multi_cell(self.w - self.l_margin - self.r_margin, 6, label)

        self.set_font("Helvetica", "", 11)
        self.set_text_color(*BLACK)
        text = answer if (answer is not None) else ""

        if text.strip():
            self.set_x(self.l_margin + 2)
            self.multi_cell(self.w - self.l_margin - self.r_margin - 2, 6, text)
        else:
            self.ln(6)
        self.ln(2)


def create_pdf(data, attachments):
    """
    Build the final PDF using the full template and styled similar to the HTML.
    Generic questions are always printed; tech-specific ones only for selected type.
    """
    pdf = IntakePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    tech_type_label = data.get("tech_type_label", "")

    # ---- Section 1: Problem Space ----
    pdf.section_title("1. The Problem Space")
    pdf.guide_box(
        "Why are we asking this?",
        "Before we choose a technology (AI, App, etc.), we must understand the pain point. "
        "Don't worry about the solution yet. Focus on what isn't working today."
    )
    pdf.question("Project Title / Brief Description", data.get("project_title"))
    pdf.question('The "Pain Point" Statement', data.get("pain_point"))
    pdf.question("Volume & Frequency", data.get("volume_frequency"))
    pdf.question("Impacted Teams / Stakeholders", data.get("stakeholders"))
    pdf.question("Regions / Legal Entities Affected", data.get("regions"))
    pdf.question("Expected Outcome / Success Criteria", data.get("success_criteria"))
    pdf.question("Target Timeline / Deadline", data.get("timeline"))

    # ---- Section 2: As-Is Workflow ----
    pdf.section_title('2. The "As-Is" Workflow')
    pdf.guide_box(
        "The \"Vacation Test\"",
        "If you went on vacation tomorrow, list the exact steps a colleague would need to take "
        "to do this task manually. Be specific about where data comes from."
    )
    pdf.question("Current Step-by-Step Process", data.get("current_process"))
    pdf.question("What tools/systems are used today?", data.get("current_tools"))
    pdf.question("Upstream Inputs & Data Sources", data.get("upstream_inputs"))
    pdf.question("Outputs / Recipients", data.get("outputs"))
    pdf.question("Known Pain Points / Failure Modes", data.get("pain_points_detail"))

    # ---- Section 3: Solution & Compliance ----
    pdf.section_title("3. Solution & Compliance")
    pdf.guide_box(
        "Data Governance is Critical",
        "In Finance and Legal, we handle sensitive data. Please be precise about what kind of "
        "technology you think you need and who has access."
    )

    pdf.question("Envisioned Solution Type", tech_type_label)

    # Only include tech details for the chosen type
    if tech_type_label.startswith("Power BI"):
        pdf.question("[Reporting / Dashboards (Power BI)] Key Metrics & KPIs", data.get("pbi_kpis"))
        pdf.question("[Reporting / Dashboards (Power BI)] Grain / Level of Detail", data.get("pbi_grain"))
        pdf.question("[Reporting / Dashboards (Power BI)] Source Systems & Data Availability", data.get("pbi_sources"))

    elif tech_type_label.startswith("Power Automate"):
        pdf.question("[Automation (Power Automate)] Trigger of the Automation", data.get("auto_trigger"))
        pdf.question("[Automation (Power Automate)] Systems & Data to Move", data.get("auto_systems"))
        pdf.question("[Automation (Power Automate)] Exception Handling & Approvals", data.get("auto_exceptions"))

    elif tech_type_label.startswith("AI / Machine Learning"):
        pdf.question("[AI / Machine Learning] Documents / Data to Analyze", data.get("ai_documents"))
        pdf.question("[AI / Machine Learning] Desired Outputs / Predictions", data.get("ai_outputs"))
        pdf.question("[AI / Machine Learning] Accuracy Requirements & Risk Considerations", data.get("ai_risk"))

    elif tech_type_label.startswith("Power Apps"):
        pdf.question("[App Development (Power Apps)] Who Will Use the App?", data.get("app_users"))
        pdf.question("[App Development (Power Apps)] Data to Capture (Fields on the Form)", data.get("app_fields"))
        pdf.question("[App Development (Power Apps)] Integrations & Required Actions", data.get("app_integrations"))
    # "Not sure yet" -> no specific details

    # Compliance
    pdf.question(
        "Contains Personal Data (PII) - Names, Addresses, Salaries?",
        "Yes" if data.get("contains_pii") else "No"
    )
    pdf.question(
        "Contains Material Non-Public Info (Insider Trading Risk)?",
        "Yes" if data.get("contains_mnpi") else "No"
    )
    pdf.question(
        "Contains Strictly Confidential Legal Privilege?",
        "Yes" if data.get("contains_privilege") else "No"
    )
    pdf.question("Access Control Considerations", data.get("access_control"))

    # ---- Section 4: Attachments & Submission ----
    pdf.section_title("4. Attachments & Submission")
    pdf.guide_box(
        "A Picture is Worth 1000 Words",
        "Please attach screenshots of the current Excel sheet, the SAP screen, or a drawing "
        "of the process."
    )

    if attachments:
        filenames = "\n".join("- " + f.name for f in attachments)
    else:
        filenames = ""
    pdf.question("Uploaded Attachment Names (dummy/redacted files only)", filenames)

    pdf.question(
        "List of Attachments (Screenshots, Excel Samples, Process Maps)",
        data.get("attachments_description")
    )
    pdf.question("Business ROI Estimate (Optional)", data.get("roi_estimate"))
    pdf.question("Additional Comments / Risks / Assumptions", data.get("additional_comments"))

    pdf_bytes = bytes(pdf.output(dest="S"))
    return pdf_bytes


# ---------- STREAMLIT APP -----------

st.set_page_config(
    page_title="Finance & Legal Project Intake",
    page_icon="📄",
    layout="centered"
)

st.markdown(
    """
    <style>
    .main {background-color: #f5f5f5;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div style="border-top: 6px solid #{PRIMARY_GREEN[0]:02x}{PRIMARY_GREEN[1]:02x}{PRIMARY_GREEN[2]:02x};
                background-color: #ffffff; padding: 20px 25px; border-radius: 6px;">
        <h1 style="color: #{PRIMARY_GREEN[0]:02x}{PRIMARY_GREEN[1]:02x}{PRIMARY_GREEN[2]:02x}; 
                   margin-bottom: 0;">
            Project Intake: Finance & Legal
        </h1>
        <p style="color: #424242; margin-top: 4px;">
            Digital Transformation Request Form
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.info(
    "Fill in the sections below. Tech-specific questions will only appear once you choose "
    "a use case type. When you're done, click **Generate PDF** to download the full document."
)

# --- TYPE SELECTOR (OUTSIDE THE FORM!) ---
tech_type = st.radio(
    "What type of solution do you envision?",
    (
        "Power BI (Reporting / Dashboards)",
        "Power Automate (Automation / Workflow)",
        "AI / Machine Learning",
        "Power Apps (App / Front-end)",
        "Not sure yet"
    ),
    index=4  # default to "Not sure yet"
)
tech_type_label = tech_type

# ---------- FORM WITH TABS ----------
with st.form("intake_form"):

    tabs = st.tabs([
        "1️⃣ Problem Space",
        "2️⃣ As-Is Workflow",
        "3️⃣ Solution & Compliance",
        "4️⃣ Attachments & Submission"
    ])

    # -------- TAB 1: Problem Space --------
    with tabs[0]:
        st.subheader("1. The Problem Space")

        project_title = st.text_input("Project Title / Brief Description")
        pain_point = st.text_area(
            'The "Pain Point" Statement',
            help='Template: "We currently spend [X] hours doing [Task], which results in [Negative Outcome]."'
        )
        volume_frequency = st.text_input(
            "Volume & Frequency",
            placeholder="e.g., 500 contracts per month, or Daily reporting"
        )
        stakeholders = st.text_area("Impacted Teams / Stakeholders")
        regions = st.text_area("Regions / Legal Entities Affected")
        success_criteria = st.text_area("Expected Outcome / Success Criteria")
        timeline = st.text_input(
            "Target Timeline / Deadline",
            placeholder="e.g., MVP by Q3, full roll-out by year-end"
        )

    # -------- TAB 2: As-Is Workflow --------
    with tabs[1]:
        st.subheader('2. The "As-Is" Workflow')

        current_process = st.text_area(
            "Current Step-by-Step Process",
            height=220,
            placeholder="1. I open the email from the client.\n2. I download the PDF attachment."
                        "\n3. I open SAP and type in the invoice number.\n4. ..."
        )
        current_tools = st.text_input("What tools/systems are used today?")
        upstream_inputs = st.text_area("Upstream Inputs & Data Sources")
        outputs = st.text_area("Outputs / Recipients")
        pain_points_detail = st.text_area("Known Pain Points / Failure Modes")

    # -------- TAB 3: Solution & Compliance --------
    with tabs[2]:
        st.subheader("3. Solution & Compliance")

        st.markdown(f"**Selected solution type:** {tech_type_label}")
        st.markdown("### Tech-Specific Details")

        # Default all to empty; only fill for active type
        pbi_kpis = pbi_grain = pbi_sources = ""
        auto_trigger = auto_systems = auto_exceptions = ""
        ai_documents = ai_outputs = ai_risk = ""
        app_users = app_fields = app_integrations = ""

        if tech_type.startswith("Power BI"):
            st.markdown("**Power BI (Reporting / Dashboards)**")
            pbi_kpis = st.text_area("Key Metrics & KPIs")
            pbi_grain = st.text_area("Grain / Level of Detail")
            pbi_sources = st.text_area("Source Systems & Data Availability")

        elif tech_type.startswith("Power Automate"):
            st.markdown("**Power Automate (Automation / Workflow)**")
            auto_trigger = st.text_area("Trigger of the Automation")
            auto_systems = st.text_area("Systems & Data to Move")
            auto_exceptions = st.text_area("Exception Handling & Approvals")

        elif tech_type.startswith("AI / Machine Learning"):
            st.markdown("**AI / Machine Learning**")
            ai_documents = st.text_area("Documents / Data to Analyze")
            ai_outputs = st.text_area("Desired Outputs / Predictions")
            ai_risk = st.text_area("Accuracy Requirements & Risk Considerations")

        elif tech_type.startswith("Power Apps"):
            st.markdown("**Power Apps (App / Front-end)**")
            app_users = st.text_area("Who Will Use the App?")
            app_fields = st.text_area("Data to Capture (Fields on the Form)")
            app_integrations = st.text_area("Integrations & Required Actions")

        else:
            st.caption("Select a type above (outside the form) to see tailored questions for that use case.")

        st.markdown("---")

        st.markdown("### Compliance Check (Required)")

        contains_pii = st.checkbox(
            "Contains Personal Data (PII) - Names, Addresses, Salaries",
            value=False
        )
        contains_mnpi = st.checkbox(
            "Contains Material Non-Public Info (Insider Trading Risk)",
            value=False
        )
        contains_privilege = st.checkbox(
            "Contains Strictly Confidential Legal Privilege",
            value=False
        )

        access_control = st.text_area(
            "Access Control Considerations",
            placeholder="Who should be able to see, edit, approve or export this data or "
                        "report? Any segregation-of-duties requirements?"
        )

    # -------- TAB 4: Attachments & Submission --------
    with tabs[3]:
        st.subheader("4. Attachments & Submission")

        uploaded_files = st.file_uploader(
            "Upload Attachments (names will be listed in the PDF; files themselves are not embedded).",
            accept_multiple_files=True
        )

        attachments_description = st.text_area(
            "List of Attachments (Screenshots, Excel Samples, Process Maps)",
            placeholder="Describe what you are providing..."
        )

        roi_estimate = st.text_input(
            "Business ROI Estimate (Optional)",
            placeholder="e.g., This will save 10 hours/week @ $50/hr..."
        )

        additional_comments = st.text_area(
            "Additional Comments / Risks / Assumptions",
            placeholder="Anything else the Digital / Finance / Legal team should know before scoping..."
        )

    submitted = st.form_submit_button("✅ Generate PDF")

if submitted:
    data = {
        # Step 1
        "project_title": project_title,
        "pain_point": pain_point,
        "volume_frequency": volume_frequency,
        "stakeholders": stakeholders,
        "regions": regions,
        "success_criteria": success_criteria,
        "timeline": timeline,

        # Step 2
        "current_process": current_process,
        "current_tools": current_tools,
        "upstream_inputs": upstream_inputs,
        "outputs": outputs,
        "pain_points_detail": pain_points_detail,

        # Step 3
        "tech_type_label": tech_type_label,
        "pbi_kpis": pbi_kpis,
        "pbi_grain": pbi_grain,
        "pbi_sources": pbi_sources,
        "auto_trigger": auto_trigger,
        "auto_systems": auto_systems,
        "auto_exceptions": auto_exceptions,
        "ai_documents": ai_documents,
        "ai_outputs": ai_outputs,
        "ai_risk": ai_risk,
        "app_users": app_users,
        "app_fields": app_fields,
        "app_integrations": app_integrations,
        "contains_pii": contains_pii,
        "contains_mnpi": contains_mnpi,
        "contains_privilege": contains_privilege,
        "access_control": access_control,

        # Step 4
        "attachments_description": attachments_description,
        "roi_estimate": roi_estimate,
        "additional_comments": additional_comments,
    }

    pdf_bytes = create_pdf(data, uploaded_files)

    st.success("Your PDF has been generated. You can download it below.")
    st.download_button(
        label="⬇️ Download Intake PDF",
        data=pdf_bytes,
        file_name="finance_legal_intake.pdf",
        mime="application/pdf"
    )
